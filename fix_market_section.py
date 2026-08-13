import os
import subprocess
import sys

print("🔧 Fixing Market Price Section...")
print("=" * 60)

# STEP 1: Check if price data exists
if not os.path.exists('data/crop_prices.csv'):
    print("\n📊 Step 1: Generating crop price data...")
    if os.path.exists('generate_price_data.py'):
        subprocess.run([sys.executable, 'generate_price_data.py'], check=True)
    else:
        print("❌ generate_price_data.py not found!")
        exit(1)
else:
    print("✅ Price data already exists")

# STEP 2: Check if price models exist
price_models_exist = all([
    os.path.exists(f'models/price_{crop}.pkl') 
    for crop in ['wheat', 'rice', 'maize', 'cotton', 'soybean', 'mustard', 'tomato']
])

if not price_models_exist:
    print("\n🧠 Step 2: Training price prediction models...")
    if os.path.exists('train_price_model.py'):
        subprocess.run([sys.executable, 'train_price_model.py'], check=True)
    else:
        print("❌ train_price_model.py not found!")
        exit(1)
else:
    print("✅ Price models already exist")

# STEP 3: Create a test script to verify backend
test_code = '''
import requests
import sys

print("\\n🧪 Testing Backend Endpoints...")
print("=" * 60)

try:
    # Test 1: Health check
    res = requests.get("http://127.0.0.1:8000/health", timeout=5)
    print(f"✅ Health: {res.status_code}")
    
    # Test 2: Available crops
    res = requests.get("http://127.0.0.1:8000/predict/available-crops", timeout=5)
    print(f"✅ Available Crops: {res.status_code} - {res.json()}")
    
    # Test 3: Price prediction
    res = requests.post("http://127.0.0.1:8000/predict/price", 
                       data={"crop": "wheat", "months_ahead": 3}, timeout=30)
    print(f"✅ Price Prediction: {res.status_code}")
    if res.status_code == 200:
        data = res.json()
        print(f"   Current: ₹{data.get('current_price', 'N/A')}")
        print(f"   Predicted: ₹{data.get('predicted_final_price', 'N/A')}")
    else:
        print(f"   Error: {res.text}")
    
    # Test 4: Best crop
    res = requests.get("http://127.0.0.1:8000/predict/best-crop?months_ahead=3", timeout=30)
    print(f"✅ Best Crop: {res.status_code}")
    
    print("\\n🎉 All backend endpoints working!")
    
except Exception as e:
    print(f"\\n❌ Backend not running! Error: {e}")
    print("\\n📝 Please start the backend first:")
    print("   python -m uvicorn src.api:app --reload --reload-dir src --host 127.0.0.1 --port 8000")
'''

with open('test_market.py', 'w') as f:
    f.write(test_code)

print("\n" + "=" * 60)
print("✅ Fix script complete!")
print("\n📝 Next steps:")
print("1. Start backend (if not running):")
print("   python -m uvicorn src.api:app --reload --reload-dir src --host 127.0.0.1 --port 8000")
print("\n2. Test the backend:")
print("   python test_market.py")
print("\n3. Refresh your browser at http://localhost:8501")
