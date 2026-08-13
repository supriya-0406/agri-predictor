import os

# ============================================
# 1. generate_data.py - English Season Names
# ============================================
gen_code = r"""import pandas as pd
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

# 🌍 NORMAL ENGLISH SEASON NAMES (lowercase for consistency)
SEASONS = {
    'rainy_season':  {'rainfall': (800, 1800), 'temp': (22, 34), 'tool_multiplier': 1.3},
    'winter_season': {'rainfall': (200, 600),  'temp': (10, 25), 'tool_multiplier': 1.0},
    'summer_season': {'rainfall': (50, 200),   'temp': (28, 40), 'tool_multiplier': 0.8}
}

REGIONS = {
    'north': {'rain_base': 600, 'temp_base': 22}, 'south': {'rain_base': 1100, 'temp_base': 28},
    'east':  {'rain_base': 1400, 'temp_base': 26}, 'west': {'rain_base': 900, 'temp_base': 27},
    'central': {'rain_base': 1000, 'temp_base': 24}
}

n_tools = 5000
tools_df = pd.DataFrame({
    'tool_type': np.random.choice(list(TOOL_LOGIC.keys()), n_tools),
    'season': np.random.choice(list(SEASONS.keys()), n_tools, p=[0.45, 0.40, 0.15]),
    'region': np.random.choice(list(REGIONS.keys()), n_tools),
    'crop_cycle': np.random.choice(['land_preparation', 'sowing', 'weeding', 'irrigation', 'harvesting', 'post_harvest'], n_tools),
    'rainfall_mm': np.zeros(n_tools), 'temperature_c': np.zeros(n_tools),
    'demand_hours': np.zeros(n_tools), 'maintenance_cycle_days': np.zeros(n_tools, dtype=int)
})

for idx, row in tools_df.iterrows():
    tool, cycle, season, region = row['tool_type'], row['crop_cycle'], row['season'], row['region']
    logic = TOOL_LOGIC[tool]
    season_info = SEASONS[season]
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
print("✅ tools_data.csv generated with English season names!")

# Breeding Data
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
print("✅ breeding_data.csv generated!")

# Seed Data
n_seeds = 4000
seeds_df = pd.DataFrame({
    'crop_type': np.random.choice(['wheat', 'rice', 'maize', 'cotton', 'soybean', 'mustard', 'tomato'], n_seeds),
    'season': np.random.choice(list(SEASONS.keys()), n_seeds), 'region': np.random.choice(list(REGIONS.keys()), n_seeds),
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
print("✅ seeds_data.csv generated!")
print("\n🌍 All datasets generated with English season names!")
"""

# ============================================
# 2. src/vision.py - Smart Label Mapping
# ============================================
vision_code = r"""from transformers import pipeline
from PIL import Image
import os

# 🔑 SMART LABEL MAPPING: Maps CLIP output to exact training labels
TOOL_LABEL_MAP = {
    'tractor': 'tractor', 'trucks': 'tractor', 'truck': 'tractor', 'vehicle': 'tractor',
    'plough': 'plough', 'plow': 'plough', 'ploughs': 'plough',
    'harrows': 'harrows', 'harrow': 'harrows',
    'cultivator': 'cultivator', 'cultivators': 'cultivator', 'tiller': 'cultivator',
    'seed drill': 'seed_drill', 'seed_drill': 'seed_drill', 'drill': 'seed_drill',
    'sprayer': 'sprayer', 'sprayers': 'sprayer',
    'pump': 'pump', 'water pump': 'pump', 'pumps': 'pump',
    'sickle': 'sickle', 'sickles': 'sickle', 'blade': 'sickle', 'knife': 'sickle',
    'harvester': 'harvester', 'harvesters': 'harvester', 'combine': 'harvester',
    'rice': 'harvester', 'wheat': 'harvester', 'crop': 'harvester', 'field': 'harvester'
}

ANIMAL_LABEL_MAP = {
    'cow': 'cow', 'cattle': 'cow', 'bull': 'cow', 'cows': 'cow', 'ox': 'cow',
    'buffalo': 'buffalo', 'buffaloes': 'buffalo', 'water buffalo': 'buffalo',
    'goat': 'goat', 'goats': 'goat', 'kid': 'goat',
    'sheep': 'sheep', 'lambs': 'sheep', 'ram': 'sheep', 'ewe': 'sheep'
}

SEED_LABEL_MAP = {
    'wheat': 'wheat', 'wheat seeds': 'wheat', 'wheat grain': 'wheat',
    'rice': 'rice', 'rice seeds': 'rice', 'paddy': 'rice',
    'maize': 'maize', 'corn': 'maize', 'maize seeds': 'maize',
    'cotton': 'cotton', 'cotton seeds': 'cotton', 'cotton plant': 'cotton',
    'soybean': 'soybean', 'soybeans': 'soybean', 'soy': 'soybean',
    'mustard': 'mustard', 'mustard seeds': 'mustard',
    'tomato': 'tomato', 'tomato plant': 'tomato', 'tomatoes': 'tomato'
}

class AgriVision:
    def __init__(self):
        try:
            self.classifier = pipeline("zero-shot-classification", model="openai/clip-vit-base-patch32", device=-1)
            self.loaded = True
            print("✅ Vision AI loaded successfully")
        except Exception as e:
            print(f"⚠️ Vision AI failed to load: {e}")
            self.loaded = False
    
    def _map_label(self, clip_label, label_map):
        # Maps CLIP output to exact training label
        label_lower = clip_label.lower().strip()
        # Direct match
        if label_lower in label_map:
            return label_map[label_lower]
        # Partial match (check if any key is contained in label)
        for key, value in label_map.items():
            if key in label_lower or label_lower in key:
                return value
        return None
    
    def classify_tool(self, image):
        if not self.loaded:
            return {'labels': ['tractor'], 'scores': [1.0]}
        try:
            labels = ['tractor', 'plough', 'harrows', 'cultivator', 'seed drill', 'sickle', 'sprayer', 'pump', 'harvester', 'field', 'crop', 'farm']
            result = self.classifier(image, labels)
            top_label = result['labels'][0]
            mapped = self._map_label(top_label, TOOL_LABEL_MAP)
            if mapped:
                print(f"📸 Vision detected: '{top_label}' → mapped to: '{mapped}'")
                return {'labels': [mapped], 'scores': result['scores'][:1]}
            return {'labels': [top_label], 'scores': result['scores'][:1]}
        except Exception as e:
            print(f"⚠️ Vision error: {e}")
            return {'labels': ['tractor'], 'scores': [1.0]}
    
    def classify_animal(self, image):
        if not self.loaded:
            return {'labels': ['cow'], 'scores': [1.0]}
        try:
            labels = ['cow', 'buffalo', 'goat', 'sheep', 'horse', 'pig', 'chicken', 'animal', 'livestock', 'farm']
            result = self.classifier(image, labels)
            top_label = result['labels'][0]
            mapped = self._map_label(top_label, ANIMAL_LABEL_MAP)
            if mapped:
                print(f"📸 Vision detected: '{top_label}' → mapped to: '{mapped}'")
                return {'labels': [mapped], 'scores': result['scores'][:1]}
            return {'labels': [top_label], 'scores': result['scores'][:1]}
        except Exception as e:
            print(f"⚠️ Vision error: {e}")
            return {'labels': ['cow'], 'scores': [1.0]}
    
    def classify_plant_seed(self, image):
        if not self.loaded:
            return {'labels': ['wheat'], 'scores': [1.0]}
        try:
            labels = ['wheat', 'rice', 'maize', 'corn', 'cotton', 'soybean', 'mustard', 'tomato', 'plant', 'seed', 'crop', 'leaf', 'field']
            result = self.classifier(image, labels)
            top_label = result['labels'][0]
            mapped = self._map_label(top_label, SEED_LABEL_MAP)
            if mapped:
                print(f"📸 Vision detected: '{top_label}' → mapped to: '{mapped}'")
                return {'labels': [mapped], 'scores': result['scores'][:1]}
            return {'labels': [top_label], 'scores': result['scores'][:1]}
        except Exception as e:
            print(f"⚠️ Vision error: {e}")
            return {'labels': ['wheat'], 'scores': [1.0]}
"""

# ============================================
# 3. src/api.py - Robust Image Handling
# ============================================
api_code = r"""from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sys, os
from PIL import Image
import io

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

vision = None
predictor = None

try:
    from src.vision import AgriVision
    from src.predictor import AgriPredictor
    vision = AgriVision()
    predictor = AgriPredictor()
    print("✅ AI Vision and Predictor loaded successfully.")
except Exception as e:
    print(f"⚠️ AI Init Warning: {e}")
    try:
        from src.predictor import AgriPredictor
        predictor = AgriPredictor()
    except:
        pass

app = FastAPI(title="AgriShare AI Predictor")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# 🔑 SEASON MAPPING: UI "Rainy Season" → Model "rainy_season"
SEASON_MAP = {
    'rainy season': 'rainy_season',
    'winter season': 'winter_season',
    'summer season': 'summer_season',
    'year round': 'rainy_season',  # fallback
    'rainy_season': 'rainy_season',
    'winter_season': 'winter_season',
    'summer_season': 'summer_season'
}

def normalize_season(season_input):
    # Converts UI season names to model-expected lowercase format
    return SEASON_MAP.get(season_input.lower().strip(), 'rainy_season')

@app.get("/health")
def health():
    return {"status": "OK", "vision_loaded": vision is not None and vision.loaded, "predictor_loaded": predictor is not None}

@app.post("/predict/tool")
async def predict_tool(
    tool_name: str = Form("tractor"),
    region: str = Form("north"),
    season: str = Form("rainy_season"),
    rainfall: float = Form(800.0),
    temperature: float = Form(28.0),
    crop_cycle: str = Form("sowing"),
    image: UploadFile = File(None)
):
    try:
        # 🔑 FAIL-SAFE IMAGE PROCESSING
        if image and image.filename and vision is not None and vision.loaded:
            try:
                contents = await image.read()
                if len(contents) > 0:
                    img = Image.open(io.BytesIO(contents)).convert("RGB")
                    result = vision.classify_tool(img)
                    detected_tool = result['labels'][0]
                    if detected_tool:
                        tool_name = detected_tool
                        print(f"📸 Vision detected tool: {tool_name}")
            except Exception as e:
                print(f"⚠️ Vision failed, using text input '{tool_name}'. Error: {e}")
        
        # 🔑 NORMALIZE SEASON
        season = normalize_season(season)
        
        if predictor is None:
            return {"error": "Predictor not loaded", "tool": tool_name}
        
        return predictor.predict_tool(tool_name, region, season, rainfall, temperature, crop_cycle)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/breeding")
async def predict_breeding(
    animal_name: str = Form("cow"),
    male_age: float = Form(3.5),
    female_age: float = Form(3.0),
    male_weight: float = Form(350.0),
    female_weight: float = Form(300.0),
    female_milk: float = Form(18.0),
    health_score: float = Form(85.0),
    genetic_diversity: float = Form(0.7),
    region: str = Form("north"),
    image: UploadFile = File(None)
):
    try:
        if image and image.filename and vision is not None and vision.loaded:
            try:
                contents = await image.read()
                if len(contents) > 0:
                    img = Image.open(io.BytesIO(contents)).convert("RGB")
                    result = vision.classify_animal(img)
                    detected = result['labels'][0]
                    if detected:
                        animal_name = detected
                        print(f"📸 Vision detected animal: {animal_name}")
            except Exception as e:
                print(f"⚠️ Vision failed, using text input '{animal_name}'. Error: {e}")
        
        if predictor is None:
            return {"error": "Predictor not loaded", "species": animal_name}
        
        # Map animal name to species/breed
        species = animal_name.lower().strip()
        breed_map = {'cow': 'sahiwal', 'buffalo': 'murrah', 'goat': 'jamunapari', 'sheep': 'deccani'}
        breed = breed_map.get(species, 'sahiwal')
        
        return predictor.predict_breeding(species, breed, male_age, female_age, male_weight, female_weight, female_milk, health_score, genetic_diversity, region)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/seed")
async def predict_seed(
    seed_name: str = Form("wheat"),
    soil_ph: float = Form(6.5),
    rainfall: float = Form(900.0),
    temperature: float = Form(26.0),
    humidity: float = Form(70.0),
    season: str = Form("rainy_season"),
    organic_carbon: float = Form(1.2),
    region: str = Form("north"),
    image: UploadFile = File(None)
):
    try:
        if image and image.filename and vision is not None and vision.loaded:
            try:
                contents = await image.read()
                if len(contents) > 0:
                    img = Image.open(io.BytesIO(contents)).convert("RGB")
                    result = vision.classify_plant_seed(img)
                    detected = result['labels'][0]
                    if detected:
                        seed_name = detected
                        print(f"📸 Vision detected seed/plant: {seed_name}")
            except Exception as e:
                print(f"⚠️ Vision failed, using text input '{seed_name}'. Error: {e}")
        
        # 🔑 NORMALIZE SEASON
        season = normalize_season(season)
        
        if predictor is None:
            return {"error": "Predictor not loaded", "crop": seed_name}
        
        return predictor.predict_seed(seed_name, soil_ph, rainfall, temperature, humidity, season, organic_carbon, region)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
"""

# ============================================
# 4. src/predictor.py - Clean Version
# ============================================
pred_code = r"""import joblib
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
            print("✅ All ML models loaded successfully")
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
                        if le:
                            try:
                                encoded_vals[col] = le.transform([val])[0]
                            except ValueError:
                                encoded_vals[col] = 0
                        else:
                            encoded_vals[col] = 0
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
                        if le:
                            try:
                                encoded_vals[col] = le.transform([val])[0]
                            except ValueError:
                                encoded_vals[col] = 0
                        else:
                            encoded_vals[col] = 0
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
                        if le:
                            try:
                                encoded_vals[col] = le.transform([val])[0]
                            except ValueError:
                                encoded_vals[col] = 0
                        else:
                            encoded_vals[col] = 0
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

# ============================================
# 5. app.py - Updated UI with English Seasons
# ============================================
app_code = r"""import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"
st.set_page_config(page_title="AgriShare AI Predictor", layout="wide")
st.title("🌾 AgriShare AI: Smart Farming Predictor")

tabs = st.tabs(["🚜 Tool Demand Analysis", "🐄 Cross-Breeding Predictor", "🌱 Seed & Plant Advisor"])

def make_request(endpoint, data, img=None):
    files = {}
    if img:
        files = {"image": (img.name, img.getvalue(), img.type)}
    try:
        res = requests.post(f"{API_URL}{endpoint}", data=data, files=files, timeout=60)
        if res.status_code == 200:
            return res.json()
        else:
            st.error(f"⚠️ Backend Error {res.status_code}:\n```\n{res.text}\n```")
            return None
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to backend. Is uvicorn running on port 8000?")
        return None
    except Exception as e:
        st.error(f"❌ Request failed: {e}")
        return None

with tabs[0]:
    st.header("Agricultural Tool Usage & Demand")
    col1, col2 = st.columns([1, 2])
    with col1:
        tool_input = st.text_input("Enter Tool Name (e.g., tractor, sickle)")
        img = st.file_uploader("📸 Upload Tool Photo (AI will auto-detect)", type=["jpg", "png", "jpeg"])
        region = st.selectbox("Region", ["north", "south", "east", "west", "central"])
        season = st.selectbox("Season", ["Rainy Season", "Winter Season", "Summer Season"])
        rainfall = st.number_input("Rainfall (mm)", 100, 2500, 800)
        temp = st.number_input("Temperature (°C)", 10, 45, 28)
        crop = st.selectbox("Crop Cycle", ["land_preparation", "sowing", "weeding", "irrigation", "harvesting", "post_harvest"])
        
        if st.button("🔍 Analyze Tool"):
            data = {"tool_name": tool_input, "region": region, "season": season, 
                    "rainfall": rainfall, "temperature": temp, "crop_cycle": crop}
            result = make_request("/predict/tool", data, img)
            if result: st.json(result)
    with col2:
        st.info("📸 **Upload a photo** of any farm tool OR type the name. AI will auto-detect and predict demand & maintenance needs.")

with tabs[1]:
    st.header("Livestock Cross-Breeding Prediction")
    col1, col2 = st.columns([1, 2])
    with col1:
        animal_input = st.text_input("Enter Animal Name (cow/buffalo/goat/sheep)")
        img = st.file_uploader("📸 Upload Animal Photo (AI will auto-detect)", type=["jpg", "png", "jpeg"], key="animal_img")
        m_age = st.number_input("Male Age (years)", 1.0, 12.0, 3.5)
        f_age = st.number_input("Female Age (years)", 1.0, 10.0, 3.0)
        m_wt = st.number_input("Male Weight (kg)", 100, 1000, 350)
        f_wt = st.number_input("Female Weight (kg)", 100, 800, 300)
        f_milk = st.number_input("Female Milk (L/day)", 0, 40, 18)
        health = st.number_input("Health Score (0-100)", 50, 100, 85)
        genetics = st.number_input("Genetic Diversity (0.0-1.0)", 0.2, 0.95, 0.7)
        region_b = st.selectbox("Region", ["north", "south", "east", "west", "central"], key="region_b")
        
        if st.button("🔍 Predict Offspring"):
            data = {"animal_name": animal_input, "male_age": m_age, "female_age": f_age,
                    "male_weight": m_wt, "female_weight": f_wt, "female_milk": f_milk,
                    "health_score": health, "genetic_diversity": genetics, "region": region_b}
            result = make_request("/predict/breeding", data, img)
            if result: st.json(result)
    with col2:
        st.info("📸 **Upload a photo** of any animal OR type the name. AI will predict offspring traits.")

with tabs[2]:
    st.header("Seed & Plant Seasonal Suitability")
    col1, col2 = st.columns([1, 2])
    with col1:
        seed_input = st.text_input("Enter Seed/Plant Name (wheat/rice/maize/cotton)")
        img = st.file_uploader("📸 Upload Seed/Plant Photo (AI will auto-detect)", type=["jpg", "png", "jpeg"], key="seed_img")
        ph = st.number_input("Soil pH", 4.0, 9.0, 6.5)
        rain = st.number_input("Expected Rainfall (mm)", 200, 3000, 900)
        temp_s = st.number_input("Avg Temperature (°C)", 10, 40, 26)
        hum = st.number_input("Humidity (%)", 30, 95, 70)
        season_s = st.selectbox("Planting Season", ["Rainy Season", "Winter Season", "Summer Season", "Year Round"])
        org_c = st.number_input("Organic Carbon (%)", 0.5, 4.0, 1.2)
        region_s = st.selectbox("Region", ["north", "south", "east", "west", "central"], key="region_s")
        
        if st.button("🔍 Analyze Planting Potential"):
            data = {"seed_name": seed_input, "soil_ph": ph, "rainfall": rain, "temperature": temp_s,
                    "humidity": hum, "season": season_s, "organic_carbon": org_c, "region": region_s}
            result = make_request("/predict/seed", data, img)
            if result: st.json(result)
    with col2:
        st.info("📸 **Upload a photo** of any seed/plant OR type the name. AI will predict yield & suitability.")
"""

# ============================================
# Write all files
# ============================================
files = {
    'generate_data.py': gen_code,
    'src/vision.py': vision_code,
    'src/api.py': api_code,
    'src/predictor.py': pred_code,
    'app.py': app_code
}

for path, content in files.items():
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else '.', exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Updated: {path}")

print("\n🎉 ALL FILES FIXED! Now run the commands below:")
print("1. Remove-Item -Path 'models\\*.pkl' -Force")
print("2. python generate_data.py")
print("3. python train_models.py")
print("4. Restart uvicorn backend")
