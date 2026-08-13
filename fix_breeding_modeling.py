import os
import sys
import io
import subprocess
import pandas as pd
import numpy as np

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

print("=" * 70)
print("🔧 FIX: Breeding Model Not Loaded")
print("=" * 70)

PROJECT_ROOT = r"C:\Users\Lakey\Desktop\agri-predictor"
os.chdir(PROJECT_ROOT)

# ============================================
# CHECK 1: What's missing?
# ============================================
print("\n🔍 CHECKING WHAT'S MISSING...")

breeding_data_exists = os.path.exists('data/breeding_data.csv')
breeding_model_exists = os.path.exists('models/breeding_predictor.pkl')
breeding_enc_exists = os.path.exists('models/breeding_predictor_encoders.pkl')

print(f"  📊 breeding_data.csv: {'✅ EXISTS' if breeding_data_exists else '❌ MISSING'}")
print(f"  🧠 breeding_predictor.pkl: {'✅ EXISTS' if breeding_model_exists else '❌ MISSING'}")
print(f"  🧠 breeding_predictor_encoders.pkl: {'✅ EXISTS' if breeding_enc_exists else '❌ MISSING'}")

# ============================================
# FIX 1: Generate Breeding Data
# ============================================
if not breeding_data_exists:
    print("\n📊 STEP 1: Generating breeding data...")
    
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

print("📊 Generating breeding data...")

n_breeds = 3000
indian_breeds = {
    'cow': ['sahiwal', 'gir', 'red_sindhi', 'tharparkar', 'holstein', 'jersey'],
    'buffalo': ['murrah', 'niliravi', 'jaffarabadi', 'mehsana', 'surti'],
    'goat': ['jamunapari', 'beetal', 'sirohi', 'black_bengal', 'osmanabadi'],
    'sheep': ['deccani', 'mandya', 'mecheri', 'bellary', 'dorper']
}

REGIONS = ['north', 'south', 'east', 'west', 'central']

breeding_df = pd.DataFrame({
    'species': np.random.choice(list(indian_breeds.keys()), n_breeds),
    'breed': [np.random.choice(indian_breeds[s]) for s in np.random.choice(list(indian_breeds.keys()), n_breeds)],
    'male_age': np.random.uniform(2, 10, n_breeds),
    'female_age': np.random.uniform(1.5, 8, n_breeds),
    'male_weight_kg': np.random.uniform(200, 800, n_breeds),
    'female_weight_kg': np.random.uniform(150, 600, n_breeds),
    'female_milk_yield_lpd': np.random.uniform(5, 30, n_breeds),
    'health_score': np.random.uniform(60, 100, n_breeds),
    'genetic_diversity_idx': np.random.uniform(0.2, 0.95, n_breeds),
    'region': np.random.choice(REGIONS, n_breeds),
    'offspring_weight_kg': 0.0,
    'offspring_milk_potential': 0.0,
    'disease_resistance': 0.0,
    'success_prob': 0.0
})

for idx, row in breeding_df.iterrows():
    breeding_df.at[idx, 'offspring_weight_kg'] = float(
        breeding_df.at[idx, 'male_weight_kg'] * 0.3 + 
        breeding_df.at[idx, 'female_weight_kg'] * 0.4 + 
        np.random.normal(0, 15)
    )
    breeding_df.at[idx, 'offspring_milk_potential'] = float(
        breeding_df.at[idx, 'female_milk_yield_lpd'] * 0.7 + 
        np.random.normal(0, 2)
    )
    breeding_df.at[idx, 'disease_resistance'] = float(np.clip(
        breeding_df.at[idx, 'health_score'] * 0.5 + 
        breeding_df.at[idx, 'genetic_diversity_idx'] * 30 + 
        np.random.normal(0, 5), 50, 100
    ))
    breeding_df.at[idx, 'success_prob'] = float(np.clip(
        (breeding_df.at[idx, 'health_score'] / 100) * 
        breeding_df.at[idx, 'genetic_diversity_idx'] + 
        np.random.normal(0, 0.05), 0.3, 0.95
    ))

breeding_df.to_csv('data/breeding_data.csv', index=False)
print(f"✅ breeding_data.csv generated with {len(breeding_df)} rows")
'''
    
    with open('generate_breeding_data.py', 'w', encoding='utf-8') as f:
        f.write(breeding_gen_code)
    
    result = subprocess.run([sys.executable, 'generate_breeding_data.py'], 
                           capture_output=True, text=True, encoding='utf-8', errors='replace')
    print(result.stdout)
    if result.returncode != 0:
        print(f"❌ Error: {result.stderr}")
        sys.exit(1)

# ============================================
# FIX 2: Train Breeding Model
# ============================================
print("\n🧠 STEP 2: Training breeding model...")

breeding_train_code = '''import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.multioutput import MultiOutputRegressor
import warnings
import sys
import io

warnings.filterwarnings('ignore')

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

print("\\n🧠 Training breeding model...")

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

# Encode categorical columns
encoders = {}
df_clean = df.copy()

for col in BREED_FEATURES:
    if df_clean[col].dtype == 'object':
        le = LabelEncoder()
        df_clean[col] = le.fit_transform(df_clean[col].astype(str))
        encoders[f'le_{col}'] = le
        print(f"  ✅ Encoded: {col}")

X = df_clean[BREED_FEATURES]
y = df_clean[TARGET_COLS]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = XGBRegressor(n_estimators=300, max_depth=8, learning_rate=0.05, random_state=42)
model = MultiOutputRegressor(model)
model.fit(X_train, y_train)

# Evaluate
from sklearn.metrics import mean_absolute_error
test_preds = model.predict(X_test)
mae_per_target = [mean_absolute_error(y_test.iloc[:, i], test_preds[:, i]) for i in range(len(TARGET_COLS))]

print(f"  📊 MAE per target: {[f'{m:.2f}' for m in mae_per_target]}")

# Save model
joblib.dump(model, 'models/breeding_predictor.pkl')
joblib.dump({'encoders': encoders, 'feature_cols': BREED_FEATURES}, 
            'models/breeding_predictor_encoders.pkl')

print(f"  ✅ Model saved: models/breeding_predictor.pkl")
print(f"  ✅ Encoders saved: models/breeding_predictor_encoders.pkl")
print(f"  📊 Features: {BREED_FEATURES}")
print("\\n✅ Breeding model training complete!")
'''

with open('train_breeding_model.py', 'w', encoding='utf-8') as f:
    f.write(breeding_train_code)

result = subprocess.run([sys.executable, 'train_breeding_model.py'], 
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
print(result.stdout)
if result.returncode != 0:
    print(f"❌ Error: {result.stderr}")
    sys.exit(1)

# ============================================
# VERIFY
# ============================================
print("\n🔍 VERIFICATION:")

if os.path.exists('models/breeding_predictor.pkl'):
    size = os.path.getsize('models/breeding_predictor.pkl')
    print(f"  ✅ breeding_predictor.pkl ({size:,} bytes)")
else:
    print(f"  ❌ breeding_predictor.pkl MISSING!")

if os.path.exists('models/breeding_predictor_encoders.pkl'):
    size = os.path.getsize('models/breeding_predictor_encoders.pkl')
    print(f"  ✅ breeding_predictor_encoders.pkl ({size:,} bytes)")
else:
    print(f"  ❌ breeding_predictor_encoders.pkl MISSING!")

# ============================================
# TEST THE MODEL
# ============================================
print("\n🧪 TESTING MODEL:")

test_code = '''
import sys
import io
import joblib
import pandas as pd

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Load model
model = joblib.load('models/breeding_predictor.pkl')
meta = joblib.load('models/breeding_predictor_encoders.pkl')

print(f"✅ Model loaded: {type(model).__name__}")
print(f"✅ Features: {meta['feature_cols']}")

# Test prediction
test_data = {
    'species': 'cow',
    'breed': 'sahiwal',
    'male_age': 3.5,
    'female_age': 3.0,
    'male_weight_kg': 400,
    'female_weight_kg': 350,
    'female_milk_yield_lpd': 18,
    'health_score': 85,
    'genetic_diversity_idx': 0.7,
    'region': 'north'
}

# Encode
encoded = {}
for col, val in test_data.items():
    if isinstance(val, str):
        le = meta['encoders'].get(f'le_{col}')
        if le:
            encoded[col] = le.transform([val])[0]
        else:
            encoded[col] = 0
    else:
        encoded[col] = val

X = pd.DataFrame([encoded], columns=meta['feature_cols'])
preds = model.predict(X)[0]

print(f"\\n📊 Test Prediction for Cow (Sahiwal):")
print(f"   Offspring Weight: {preds[0]:.2f} kg")
print(f"   Milk Potential: {preds[1]:.2f} L/day")
print(f"   Disease Resistance: {preds[2]:.2f}")
print(f"   Success Probability: {preds[3]*100:.1f}%")
print(f"\\n✅ MODEL IS WORKING!")
'''

with open('test_breeding.py', 'w', encoding='utf-8') as f:
    f.write(test_code)

result = subprocess.run([sys.executable, 'test_breeding.py'], 
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
print(result.stdout)
if result.returncode != 0:
    print(f"❌ Test failed: {result.stderr}")

print("\n" + "=" * 70)
print("✅ FIX COMPLETE!")
print("=" * 70)
print("\n📝 Next steps:")
print("1. Restart backend (Ctrl+C in Terminal 1, then run uvicorn)")
print("2. Refresh browser at http://localhost:8501")
print("3. Test Section 2: Cross-Breeding Predictor")
