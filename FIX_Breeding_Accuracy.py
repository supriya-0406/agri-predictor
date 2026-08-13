import pandas as pd
import numpy as np
import os
import sys
import io
import subprocess

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

print("=" * 70)
print("🔧 FIX: Breeding Model Accuracy + Species-Specific Data")
print("=" * 70)

PROJECT_ROOT = r"C:\Users\Lakey\Desktop\agri-predictor"
os.chdir(PROJECT_ROOT)

# ============================================
# Generate more accurate species-specific data
# ============================================
print("\n📊 Generating species-specific breeding data...")

breeding_gen_code = '''import pandas as pd
import numpy as np
import os
import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

os.makedirs('data', exist_ok=True)
np.random.seed(42)

print("📊 Generating species-specific breeding data...")

# 🔑 FIXED: Realistic species-specific data
SPECIES_CONFIG = {
    'cow': {
        'breeds': ['sahiwal', 'gir', 'red_sindhi', 'tharparkar', 'holstein', 'jersey'],
        'weight_range': (200, 800),
        'milk_range': (10, 35),
        'offspring_weight': (25, 45),
        'count': 1200
    },
    'buffalo': {
        'breeds': ['murrah', 'niliravi', 'jaffarabadi', 'mehsana', 'surti'],
        'weight_range': (300, 1200),
        'milk_range': (12, 30),
        'offspring_weight': (35, 55),
        'count': 800
    },
    'goat': {
        'breeds': ['jamunapari', 'beetal', 'sirohi', 'black_bengal', 'osmanabadi'],
        'weight_range': (20, 80),  # 🔑 FIXED
        'milk_range': (1, 5),
        'offspring_weight': (2, 5),  # 🔑 FIXED: Goat kids are 2-5 kg
        'count': 600
    },
    'sheep': {
        'breeds': ['deccani', 'mandya', 'mecheri', 'bellary', 'dorper'],
        'weight_range': (30, 100),  # 🔑 FIXED
        'milk_range': (0.5, 3),
        'offspring_weight': (3, 6),  # 🔑 FIXED: Lamb is 3-6 kg
        'count': 400
    }
}

REGIONS = ['north', 'south', 'east', 'west', 'central']

all_records = []

for species, config in SPECIES_CONFIG.items():
    print(f"  📊 Generating {species} data ({config['count']} records)...")
    
    for i in range(config['count']):
        breed = np.random.choice(config['breeds'])
        
        # Parent characteristics
        male_weight = np.random.uniform(*config['weight_range'])
        female_weight = np.random.uniform(*config['weight_range'])
        male_age = np.random.uniform(2, 10)
        female_age = np.random.uniform(1.5, 8)
        female_milk = np.random.uniform(*config['milk_range'])
        
        # Health and genetics
        health_score = np.random.uniform(60, 100)
        genetic_diversity = np.random.uniform(0.2, 0.95)
        region = np.random.choice(REGIONS)
        
        # 🔑 FIXED: Species-specific offspring calculations
        # Offspring weight = 30% male + 40% female + genetics bonus
        base_offspring_weight = (
            male_weight * 0.3 + 
            female_weight * 0.4 + 
            np.random.normal(0, config['offspring_weight'][1] * 0.1)
        )
        offspring_weight = np.clip(
            base_offspring_weight, 
            config['offspring_weight'][0], 
            config['offspring_weight'][1]
        )
        
        # Milk potential (for female offspring)
        offspring_milk = np.clip(
            female_milk * 0.7 + np.random.normal(0, config['milk_range'][1] * 0.15),
            config['milk_range'][0] * 0.5,
            config['milk_range'][1] * 1.2
        )
        
        # Disease resistance
        disease_resistance = np.clip(
            health_score * 0.5 + genetic_diversity * 30 + np.random.normal(0, 5),
            50, 100
        )
        
        # Success probability
        success_prob = np.clip(
            (health_score / 100) * genetic_diversity + np.random.normal(0, 0.05),
            0.3, 0.95
        )
        
        all_records.append({
            'species': species,
            'breed': breed,
            'male_age': male_age,
            'female_age': female_age,
            'male_weight_kg': round(male_weight, 2),
            'female_weight_kg': round(female_weight, 2),
            'female_milk_yield_lpd': round(female_milk, 2),
            'health_score': round(health_score, 2),
            'genetic_diversity_idx': round(genetic_diversity, 3),
            'region': region,
            'offspring_weight_kg': round(offspring_weight, 2),
            'offspring_milk_potential': round(offspring_milk, 2),
            'disease_resistance': round(disease_resistance, 2),
            'success_prob': round(success_prob, 3)
        })

breeding_df = pd.DataFrame(all_records)
breeding_df.to_csv('data/breeding_data.csv', index=False)

print(f"\\n✅ breeding_data.csv generated with {len(breeding_df)} records")
print(f"\\n📊 Species distribution:")
print(breeding_df['species'].value_counts())
print(f"\\n📊 Weight ranges by species:")
for species in breeding_df['species'].unique():
    species_df = breeding_df[breeding_df['species'] == species]
    print(f"  {species}: {species_df['male_weight_kg'].min():.0f}-{species_df['male_weight_kg'].max():.0f} kg")
'''

with open('generate_breeding_data.py', 'w', encoding='utf-8') as f:
    f.write(breeding_gen_code)

# Generate data
result = subprocess.run([sys.executable, 'generate_breeding_data.py'], 
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
print(result.stdout)
if result.returncode != 0:
    print(f"❌ Error: {result.stderr}")
    sys.exit(1)

# ============================================
# Retrain model with better data
# ============================================
print("\n🧠 Retraining breeding model with species-specific data...")

train_code = '''import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import warnings
import sys
import io

warnings.filterwarnings('ignore')

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

print("\\n🧠 Training improved breeding model...")

BREED_FEATURES = [
    'species', 'breed', 'male_age', 'female_age', 
    'male_weight_kg', 'female_weight_kg', 'female_milk_yield_lpd',
    'health_score', 'genetic_diversity_idx', 'region'
]

TARGET_COLS = [
    'offspring_weight_kg', 'offspring_milk_potential',
    'disease_resistance', 'success_prob'
]

df = pd.read_csv('data/breeding_data.csv')
print(f"  📊 Data shape: {df.shape}")
print(f"  📊 Species: {df['species'].unique()}")

# Encode categorical columns
encoders = {}
df_clean = df.copy()

for col in BREED_FEATURES:
    if df_clean[col].dtype == 'object':
        le = LabelEncoder()
        df_clean[col] = le.fit_transform(df_clean[col].astype(str))
        encoders[f'le_{col}'] = le

X = df_clean[BREED_FEATURES]
y = df_clean[TARGET_COLS]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 🔑 IMPROVED: Better hyperparameters
model = XGBRegressor(
    n_estimators=400,           # More trees
    max_depth=10,               # Deeper trees
    learning_rate=0.03,         # Slower learning
    subsample=0.8,              # Row sampling
    colsample_bytree=0.8,       # Column sampling
    random_state=42
)
model = MultiOutputRegressor(model)
model.fit(X_train, y_train)

# Evaluate
test_preds = model.predict(X_test)
mae_per_target = [mean_absolute_error(y_test.iloc[:, i], test_preds[:, i]) for i in range(len(TARGET_COLS))]
r2_per_target = [r2_score(y_test.iloc[:, i], test_preds[:, i]) for i in range(len(TARGET_COLS))]

print(f"  📊 MAE per target: {[f'{m:.2f}' for m in mae_per_target]}")
print(f"  📊 R² per target: {[f'{r:.3f}' for r in r2_per_target]}")

# Save model
joblib.dump(model, 'models/breeding_predictor.pkl')
joblib.dump({'encoders': encoders, 'feature_cols': BREED_FEATURES}, 
            'models/breeding_predictor_encoders.pkl')

print(f"  ✅ Model saved: models/breeding_predictor.pkl")
print(f"  ✅ Encoders saved: models/breeding_predictor_encoders.pkl")
print("\\n✅ Improved breeding model training complete!")
'''

with open('train_breeding_model.py', 'w', encoding='utf-8') as f:
    f.write(train_code)

result = subprocess.run([sys.executable, 'train_breeding_model.py'], 
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
print(result.stdout)
if result.returncode != 0:
    print(f"❌ Error: {result.stderr}")
    sys.exit(1)

print("\n" + "=" * 70)
print("✅ FIX COMPLETE!")
print("=" * 70)
print("\n📝 Next steps:")
print("1. Restart backend (Ctrl+C in Terminal 1, then run uvicorn)")
print("2. Refresh browser at http://localhost:8501")
print("3. Test Section 2 with goat/sheep - weight ranges are now correct!")
