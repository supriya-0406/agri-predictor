import os

# 1. generate_data.py (STRICT 6 features + 2 targets for tools)
gen_code = """import pandas as pd
import numpy as np
import os
os.makedirs('data', exist_ok=True)
os.makedirs('models', exist_ok=True)
np.random.seed(42)

TOOL_LOGIC = {
    'tractor':     {'land_preparation': 2.5, 'sowing': 2.0, 'weeding': 0.5, 'irrigation': 0.8, 'harvesting': 0.3, 'post_harvest': 0.2, 'base_hours': (80, 250)},
    'plough':      {'land_preparation': 3.0, 'sowing': 1.5, 'weeding': 0.2, 'irrigation': 0.1, 'harvesting': 0.1, 'post_harvest': 0.1, 'base_hours': (40, 120)},
    'harrows':     {'land_preparation': 2.5, 'sowing': 1.2, 'weeding': 0.3, 'irrigation': 0.1, 'harvesting': 0.1, 'post_harvest': 0.1, 'base_hours': (30, 100)},
    'cultivator':  {'land_preparation': 2.0, 'sowing': 1.5, 'weeding': 1.8, 'irrigation': 0.2, 'harvesting': 0.1, 'post_harvest': 0.1, 'base_hours': (40, 130)},
    'seed_drill':  {'land_preparation': 0.1, 'sowing': 3.5, 'weeding': 0.1, 'irrigation': 0.1, 'harvesting': 0.0, 'post_harvest': 0.0, 'base_hours': (15, 60)},
    'sprayer':     {'land_preparation': 0.2, 'sowing': 1.5, 'weeding': 2.5, 'irrigation': 1.0, 'harvesting': 0.1, 'post_harvest': 0.1, 'base_hours': (20, 80)},
    'pump':        {'land_preparation': 0.5, 'sowing': 1.5, 'weeding': 1.2, 'irrigation': 4.0, 'harvesting': 0.2, 'post_harvest': 0.1, 'base_hours': (100, 400)},
    'sickle':      {'land_preparation': 0.0, 'sowing': 0.0, 'weeding': 0.1, 'irrigation': 0.0, 'harvesting': 3.5, 'post_harvest': 2.0, 'base_hours': (30, 100)},
    'harvester':   {'land_preparation': 0.0, 'sowing': 0.0, 'weeding': 0.0, 'irrigation': 0.0, 'harvesting': 4.0, 'post_harvest': 1.5, 'base_hours': (60, 200)}
}
INDIAN_SEASONS = {
    'kharif': {'rainfall': (800, 1800), 'temp': (22, 34), 'tool_multiplier': 1.3},
    'rabi': {'rainfall': (200, 600), 'temp': (10, 25), 'tool_multiplier': 1.0},
    'zaid': {'rainfall': (50, 200), 'temp': (28, 40), 'tool_multiplier': 0.8}
}
REGIONS = {
    'north': {'rain_base': 600, 'temp_base': 22}, 'south': {'rain_base': 1100, 'temp_base': 28},
    'east': {'rain_base': 1400, 'temp_base': 26}, 'west': {'rain_base': 900, 'temp_base': 27},
    'central': {'rain_base': 1000, 'temp_base': 24}
}

n_tools = 5000
# EXACT 8 COLUMNS: 6 features + 2 targets (NO crop_type)
tools_df = pd.DataFrame({
    'tool_type': np.random.choice(list(TOOL_LOGIC.keys()), n_tools),
    'season': np.random.choice(['kharif', 'rabi', 'zaid'], n_tools, p=[0.45, 0.40, 0.15]),
    'region': np.random.choice(list(REGIONS.keys()), n_tools),
    'crop_cycle': np.random.choice(['land_preparation', 'sowing', 'weeding', 'irrigation', 'harvesting', 'post_harvest'], n_tools),
    'rainfall_mm': np.zeros(n_tools), 'temperature_c': np.zeros(n_tools),
    'demand_hours': np.zeros(n_tools), 'maintenance_cycle_days': np.zeros(n_tools, dtype=int)
})

for idx, row in tools_df.iterrows():
    tool, cycle, season, region = row['tool_type'], row['crop_cycle'], row['season'], row['region']
    logic = TOOL_LOGIC[tool]
    season_info = INDIAN_SEASONS[season]
    region_info = REGIONS[region]
    
    tools_df.at[idx, 'rainfall_mm'] = float(np.clip(region_info['rain_base']*0.3 + np.mean(season_info['rainfall'])*0.7 + np.random.normal(0, 100), season_info['rainfall'][0], season_info['rainfall'][1]))
    tools_df.at[idx, 'temperature_c'] = float(np.clip(region_info['temp_base']*0.4 + np.mean(season_info['temp'])*0.6 + np.random.normal(0, 3), season_info['temp'][0], season_info['temp'][1]))
    
    base_min, base_max = logic['base_hours']
    base_demand = np.random.uniform(base_min, base_max)
    cycle_mult = logic.get(cycle, 0.1)
    season_mult = season_info['tool_multiplier']
    final_demand = base_demand * cycle_mult * season_mult + np.random.normal(0, 10)
    tools_df.at[idx, 'demand_hours'] = float(max(0, round(final_demand, 2)))
    
    usage_factor = tools_df.at[idx, 'demand_hours'] / 100
    base_maint = 60 if tool in ['sickle', 'sprayer'] else 120
    tools_df.at[idx, 'maintenance_cycle_days'] = int(np.clip(base_maint / max(0.5, usage_factor) + np.random.normal(0, 10), 15, 180))

tools_df.to_csv('data/tools_data.csv', index=False)
print("✅ tools_data.csv generated (8 columns: 6 features + 2 targets)")

# Breeding Data (10 features + 4 targets)
n_breeds = 3000
indian_breeds = {'cow': ['sahiwal', 'gir', 'red_sindhi'], 'buffalo': ['murrah', 'niliravi', 'jaffarabadi'], 'goat': ['jamunapari', 'beetal', 'sirohi'], 'sheep': ['deccani', 'mandya', 'mecheri']}
breeding_df = pd.DataFrame({
    'species': np.random.choice(list(indian_breeds.keys()), n_breeds),
    'breed': [np.random.choice(indian_breeds[s]) for s in np.random.choice(list(indian_breeds.keys()), n_breeds)],
    'male_age': np.random.uniform(2, 10, n_breeds), 'female_age': np.random.uniform(1.5, 8, n_breeds),
    'male_weight_kg': np.random.uniform(200, 800, n_breeds), 'female_weight_kg': np.random.uniform(150, 600, n_breeds),
    'female_milk_yield_lpd': np.random.uniform(5, 30, n_breeds), 'health_score': np.random.uniform(60, 100, n_breeds),
    'genetic_diversity_idx': np.random.uniform(0.2, 0.95, n_breeds), 'region': np.random.choice(list(REGIONS.keys()), n_breeds),
    'offspring_weight_kg': 0.0, 'offspring_milk_potential': 0.0, 'disease_resistance': 0.0, 'success_prob': 0.0
})
for idx, row in breeding_df.iterrows():
    breeding_df.at[idx, 'offspring_weight_kg'] = float(breeding_df.at[idx, 'male_weight_kg']*0.3 + breeding_df.at[idx, 'female_weight_kg']*0.4 + np.random.normal(0, 15))
    breeding_df.at[idx, 'offspring_milk_potential'] = float(breeding_df.at[idx, 'female_milk_yield_lpd']*0.7 + np.random.normal(0, 2))
    breeding_df.at[idx, 'disease_resistance'] = float(np.clip(breeding_df.at[idx, 'health_score']*0.5 + breeding_df.at[idx, 'genetic_diversity_idx']*30 + np.random.normal(0, 5), 50, 100))
    breeding_df.at[idx, 'success_prob'] = float(np.clip((breeding_df.at[idx, 'health_score']/100) * breeding_df.at[idx, 'genetic_diversity_idx'] + np.random.normal(0, 0.05), 0.3, 0.95))
breeding_df.to_csv('data/breeding_data.csv', index=False)
print("✅ breeding_data.csv generated (14 columns: 10 features + 4 targets)")

# Seed Data (8 features + 2 targets)
n_seeds = 4000
seeds_df = pd.DataFrame({
    'crop_type': np.random.choice(['wheat', 'rice', 'maize', 'cotton', 'soybean', 'mustard', 'tomato'], n_seeds),
    'season': np.random.choice(['kharif', 'rabi', 'zaid'], n_seeds), 'region': np.random.choice(list(REGIONS.keys()), n_seeds),
    'soil_ph': np.random.uniform(4.5, 8.5, n_seeds), 'rainfall_mm': np.random.uniform(300, 2500, n_seeds),
    'temperature_c': np.random.uniform(10, 40, n_seeds), 'humidity_pct': np.random.uniform(30, 90, n_seeds),
    'soil_organic_c': np.random.uniform(0.5, 3.0, n_seeds), 'expected_yield_t_ha': 0.0, 'seasonal_suitability': 0.0
})
for idx, row in seeds_df.iterrows():
    base_yield = {'wheat': 4.5, 'rice': 5.2, 'maize': 3.8, 'cotton': 1.2, 'soybean': 2.1, 'mustard': 1.8, 'tomato': 25}.get(row['crop_type'], 3.0)
    suit = np.clip((1 - abs((row['soil_ph']-6.5)/2))*0.3 + (row['rainfall_mm']/2000)*0.25 + (1 - abs((row['temperature_c']-22)/15))*0.25 + np.random.normal(0.85, 0.1), 0, 1)
    seeds_df.at[idx, 'expected_yield_t_ha'] = float(np.clip(base_yield * suit + np.random.normal(0, 1.5), 0.5, 35))
    seeds_df.at[idx, 'seasonal_suitability'] = float(suit)
seeds_df.to_csv('data/seeds_data.csv', index=False)
print("✅ seeds_data.csv generated (10 columns: 8 features + 2 targets)")
print("\\n🇮🇳 All datasets generated with STRICT column alignment!")
"""

# 2. train_models.py (Auto-detects columns, impossible to fail)
train_code = """import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.multioutput import MultiOutputRegressor
import warnings
warnings.filterwarnings('ignore')

def auto_train(csv_path, target_cols, model_name):
    print(f"\\n🔄 Training {model_name}...")
    df = pd.read_csv(csv_path)
    print(f"📊 Found columns: {list(df.columns)}")
    
    y = df[target_cols]
    X = df.drop(columns=target_cols)
    
    # Drop non-essential columns if they exist
    cols_to_drop = ['Unnamed: 0', 'index', 'crop_type'] # EXPLICITLY DROP crop_type if it sneaks in
    X = X.drop(columns=[c for c in cols_to_drop if c in X.columns])
    
    encoders = {}
    for col in X.columns:
        if X[col].dtype == 'object':
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
            encoders[f'le_{col}'] = le
    
    print(f"✅ Using {len(X.columns)} features: {list(X.columns)}")
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    base_model = XGBRegressor(n_estimators=200, max_depth=6, learning_rate=0.1, random_state=42)
    if len(target_cols) > 1:
        model = MultiOutputRegressor(base_model)
        model.fit(X_train, y_train)
    else:
        model = base_model
        y_train_flat = y_train.iloc[:, 0] if isinstance(y_train, pd.DataFrame) else y_train
        model.fit(X_train, y_train_flat)
        
    joblib.dump(model, f"models/{model_name}.pkl")
    joblib.dump({'encoders': encoders, 'feature_cols': list(X.columns)}, f"models/{model_name}_encoders.pkl")
    print(f"✅ {model_name} trained and saved successfully!")

auto_train('data/tools_data.csv', ['demand_hours', 'maintenance_cycle_days'], 'tool_demand')
auto_train('data/breeding_data.csv', ['offspring_weight_kg', 'offspring_milk_potential', 'disease_resistance', 'success_prob'], 'breeding_predictor')
auto_train('data/seeds_data.csv', ['expected_yield_t_ha', 'seasonal_suitability'], 'seed_advisor')
print("\\n🎯 ALL MODELS TRAINED SUCCESSFULLY!")
"""

# 3. src/predictor.py (Dynamically builds DataFrame based on saved model metadata)
pred_code = """import joblib
import pandas as pd
import os

class AgriPredictor:
    def __init__(self):
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        try:
            self.tool_model = joblib.load(os.path.join(base_path, 'models/tool_demand.pkl'))
            self.tool_meta = joblib.load(os.path.join(base_path, 'models/tool_demand_encoders.pkl'))
            self.tool_encoders = self.tool_meta.get('encoders', {})
            self.tool_features = self.tool_meta.get('feature_cols', [])
            
            self.breed_model = joblib.load(os.path.join(base_path, 'models/breeding_predictor.pkl'))
            self.breed_meta = joblib.load(os.path.join(base_path, 'models/breeding_predictor_encoders.pkl'))
            self.breed_encoders = self.breed_meta.get('encoders', {})
            self.breed_features = self.breed_meta.get('feature_cols', [])
            
            self.seed_model = joblib.load(os.path.join(base_path, 'models/seed_advisor.pkl'))
            self.seed_meta = joblib.load(os.path.join(base_path, 'models/seed_advisor_encoders.pkl'))
            self.seed_encoders = self.seed_meta.get('encoders', {})
            self.seed_features = self.seed_meta.get('feature_cols', [])
        except Exception as e:
            print(f"⚠️ Model load warning: {e}")
            self.tool_model = self.breed_model = self.seed_model = None

    def predict_tool(self, tool_name, region, season, rainfall, temp, crop_cycle):
        tool_name = str(tool_name).lower().strip()
        region = str(region).lower().strip()
        season = str(season).lower().strip()
        crop_cycle = str(crop_cycle).lower().strip()
        
        if self.tool_model is None:
            return {"error": "Model not loaded"}
        
        try:
            encoded_vals = {}
            mapping = {
                'tool_type': tool_name, 'season': season, 'region': region, 'crop_cycle': crop_cycle,
                'rainfall_mm': float(rainfall), 'temperature_c': float(temp)
            }
            for col, val in mapping.items():
                if col in self.tool_features:
                    if isinstance(val, str):
                        le = self.tool_encoders.get(f'le_{col}')
                        encoded_vals[col] = le.transform([val])[0] if le else 0
                    else:
                        encoded_vals[col] = val
            
            X = pd.DataFrame([encoded_vals], columns=self.tool_features)
            preds = self.tool_model.predict(X)[0]
            demand = float(preds[0])
            maint = int(float(preds[1]))
            
            if crop_cycle == 'harvesting' and tool_name in ['sickle', 'harvester']:
                rec = f"🔥 PEAK HARVEST DEMAND: Ensure {tool_name} is serviced." if demand > 80 else f"✅ Moderate harvest demand for {tool_name}."
            elif crop_cycle in ['sowing', 'land_preparation'] and tool_name in ['tractor', 'plough', 'seed_drill']:
                rec = f"🔥 HIGH SOWING DEMAND: Schedule pre-season maintenance for {tool_name}." if demand > 100 else f"✅ Normal sowing demand for {tool_name}."
            else:
                rec = f"✅ Low usage for {tool_name} during {crop_cycle}." if demand < 60 else f"⚡ Above-average usage expected for {tool_name}."
            
            return {
                "tool": tool_name, "crop_cycle": crop_cycle, "season": season,
                "predicted_demand_hours": round(demand, 2),
                "optimal_maintenance_days": maint,
                "usage_recommendation": rec
            }
        except Exception as e:
            return {"error": str(e)}

    def predict_breeding(self, species, breed, m_age, f_age, m_wt, f_wt, f_milk, health, genetics, region='north'):
        species = str(species).lower().strip()
        breed = str(breed).lower().strip()
        region = str(region).lower().strip()
        if self.breed_model is None:
            return {"error": "Model not loaded"}
        try:
            encoded_vals = {}
            mapping = {
                'species': species, 'breed': breed, 'region': region,
                'male_age': float(m_age), 'female_age': float(f_age), 
                'male_weight_kg': float(m_wt), 'female_weight_kg': float(f_wt), 
                'female_milk_yield_lpd': float(f_milk), 'health_score': float(health), 
                'genetic_diversity_idx': float(genetics)
            }
            for col, val in mapping.items():
                if col in self.breed_features:
                    if isinstance(val, str):
                        le = self.breed_encoders.get(f'le_{col}')
                        encoded_vals[col] = le.transform([val])[0] if le else 0
                    else:
                        encoded_vals[col] = val
            
            X = pd.DataFrame([encoded_vals], columns=self.breed_features)
            preds = self.breed_model.predict(X)[0]
            return {
                "species": species, "breed": breed, "region": region,
                "offspring_weight_kg": round(float(preds[0]), 2),
                "offspring_milk_potential_lpd": round(float(preds[1]), 2),
                "disease_resistance_score": round(float(preds[2]), 2),
                "breeding_success_prob": round(float(preds[3])*100, 1),
                "recommendation": "Excellent genetic match." if float(preds[3]) > 0.75 else "Moderate compatibility."
            }
        except Exception as e:
            return {"error": str(e)}

    def predict_seed(self, crop, ph, rainfall, temp, humidity, season, organic_c, region='north'):
        crop = str(crop).lower().strip()
        season = str(season).lower().strip()
        region = str(region).lower().strip()
        if self.seed_model is None:
            return {"error": "Model not loaded"}
        try:
            encoded_vals = {}
            mapping = {
                'crop_type': crop, 'season': season, 'region': region,
                'soil_ph': float(ph), 'rainfall_mm': float(rainfall), 
                'temperature_c': float(temp), 'humidity_pct': float(humidity), 
                'soil_organic_c': float(organic_c)
            }
            for col, val in mapping.items():
                if col in self.seed_features:
                    if isinstance(val, str):
                        le = self.seed_encoders.get(f'le_{col}')
                        encoded_vals[col] = le.transform([val])[0] if le else 0
                    else:
                        encoded_vals[col] = val
            
            X = pd.DataFrame([encoded_vals], columns=self.seed_features)
            preds = self.seed_model.predict(X)[0]
            suit = float(preds[1]) * 100
            return {
                "crop": crop, "season": season, "region": region,
                "expected_yield_t_ha": round(float(preds[0]), 2),
                "seasonal_suitability_score": round(suit, 1),
                "planting_window": "Optimal window for sowing." if suit > 75 else "Wait for better conditions.",
                "soil_treatment": "Maintain pH 6.0-7.0 and add organic matter."
            }
        except Exception as e:
            return {"error": str(e)}
"""

with open('generate_data.py', 'w', encoding='utf-8') as f:
    f.write(gen_code)
with open('train_models.py', 'w', encoding='utf-8') as f:
    f.write(train_code)
with open('src/predictor.py', 'w', encoding='utf-8') as f:
    f.write(pred_code)

print("✅ All 3 files rewritten with PERFECT column alignment!")
print("🚀 Now run: python generate_data.py && python train_models.py")
