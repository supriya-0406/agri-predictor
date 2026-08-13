import os
import subprocess
import sys

print("🔧 Fixing Potato Detection & Crop Recognition...")
print("=" * 60)

# ============================================
# FIX 1: Update generate_data.py to include potato
# ============================================
with open('generate_data.py', 'r', encoding='utf-8') as f:
    gen_content = f.read()

# Replace the crop list in seeds_df
old_crop_line = "'crop_type': np.random.choice(['wheat', 'rice', 'maize', 'cotton', 'soybean', 'mustard', 'tomato'], n_seeds),"
new_crop_line = "'crop_type': np.random.choice(['wheat', 'rice', 'maize', 'cotton', 'soybean', 'mustard', 'tomato', 'potato', 'onion', 'carrot', 'cabbage', 'cauliflower'], n_seeds),"

if old_crop_line in gen_content:
    gen_content = gen_content.replace(old_crop_line, new_crop_line)
    
    # Also update the base_yield dictionary
    old_yield = "base_yield = {'wheat': 4.5, 'rice': 5.2, 'maize': 3.8, 'cotton': 1.2, 'soybean': 2.1, 'mustard': 1.8, 'tomato': 25}.get(row['crop_type'], 3.0)"
    new_yield = "base_yield = {'wheat': 4.5, 'rice': 5.2, 'maize': 3.8, 'cotton': 1.2, 'soybean': 2.1, 'mustard': 1.8, 'tomato': 25, 'potato': 20, 'onion': 18, 'carrot': 15, 'cabbage': 22, 'cauliflower': 16}.get(row['crop_type'], 3.0)"
    
    if old_yield in gen_content:
        gen_content = gen_content.replace(old_yield, new_yield)
    
    with open('generate_data.py', 'w', encoding='utf-8') as f:
        f.write(gen_content)
    print("✅ Updated generate_data.py with potato and other vegetables")
else:
    print("⚠️ Could not find crop list in generate_data.py")

# ============================================
# FIX 2: Update src/vision.py to detect potato
# ============================================
vision_code = r'''import os
from PIL import Image

class AgriVision:
    def __init__(self):
        self.clip = None
        self.loaded = False
        try:
            from transformers import pipeline
            print("🧠 Loading CLIP Vision AI (zero-shot-image-classification)...")
            self.clip = pipeline("zero-shot-image-classification", model="openai/clip-vit-base-patch32")
            self.loaded = True
            print("✅ CLIP Vision AI loaded successfully!")
        except Exception as e:
            print(f"❌ CRITICAL: Vision AI failed to load: {e}")

    def _prepare_image(self, image):
        """Upscale tiny images so CLIP doesn't crash"""
        if image.mode != 'RGB':
            image = image.convert('RGB')
        if image.width < 224 or image.height < 224:
            image = image.resize((224, 224), Image.Resampling.LANCZOS)
        return image

    def classify_tool(self, image):
        if not self.loaded:
            return {'labels': ['unknown'], 'scores': [0.0], 'engine': 'none'}
        
        image = self._prepare_image(image)
        candidates = [
            "a photo of a farm tractor",
            "a photo of a curved metal sickle blade",
            "a photo of a wooden or metal plough",
            "a photo of a combine harvester machine",
            "a photo of a water irrigation pump",
            "a photo of a pesticide sprayer tank",
            "a photo of a seed drill machine",
            "a photo of a metal harrow",
            "a photo of a rotary cultivator"
        ]
        
        try:
            results = self.clip(image, candidate_labels=candidates)
            top_result = results[0]
            top_label = top_result['label']
            top_score = top_result['score']
            
            print(f"🔍 CLIP Raw Output: {top_label} (Score: {top_score:.3f})")
            
            mapping = {
                'tractor': 'tractor', 'sickle': 'sickle', 'plough': 'plough',
                'harvester': 'harvester', 'pump': 'pump', 'sprayer': 'sprayer',
                'seed drill': 'seed_drill', 'harrow': 'harrows', 'cultivator': 'cultivator'
            }
            
            detected_tool = 'unknown'
            for key, val in mapping.items():
                if key in top_label.lower():
                    detected_tool = val
                    break
            
            return {'labels': [detected_tool], 'scores': [top_score], 'engine': 'clip'}
        except Exception as e:
            print(f"❌ CLIP classification error: {e}")
            return {'labels': ['unknown'], 'scores': [0.0], 'engine': 'error'}

    def classify_animal(self, image):
        if not self.loaded: return {'labels': ['unknown'], 'scores': [0.0], 'engine': 'none'}
        image = self._prepare_image(image)
        candidates = ["a photo of a cow", "a photo of a buffalo", "a photo of a goat", "a photo of a sheep"]
        try:
            results = self.clip(image, candidate_labels=candidates)
            top = results[0]
            mapping = {'cow': 'cow', 'buffalo': 'buffalo', 'goat': 'goat', 'sheep': 'sheep'}
            detected = 'unknown'
            for k, v in mapping.items():
                if k in top['label'].lower(): detected = v; break
            return {'labels': [detected], 'scores': [top['score']], 'engine': 'clip'}
        except: return {'labels': ['unknown'], 'scores': [0.0], 'engine': 'error'}

    def classify_plant_seed(self, image):
        if not self.loaded: return {'labels': ['unknown'], 'scores': [0.0], 'engine': 'none'}
        image = self._prepare_image(image)
        
        # ✅ ADDED: potato, onion, carrot, cabbage, cauliflower
        candidates = [
            "a photo of wheat grains or wheat field",
            "a photo of rice paddy or rice plant",
            "a photo of maize or corn plants",
            "a photo of cotton bolls or cotton plant",
            "a photo of tomato fruits on plant",
            "a photo of mustard flowers",
            "a photo of soybean plants",
            "a photo of potato tubers or potato plant",
            "a photo of onion bulbs or onion plant",
            "a photo of carrot roots",
            "a photo of cabbage head",
            "a photo of cauliflower head"
        ]
        
        try:
            results = self.clip(image, candidate_labels=candidates)
            top = results[0]
            
            # ✅ ADDED: mapping for new crops
            mapping = {
                'wheat': 'wheat', 'rice': 'rice', 'maize': 'maize', 'corn': 'maize',
                'cotton': 'cotton', 'tomato': 'tomato', 'mustard': 'mustard', 'soybean': 'soybean',
                'potato': 'potato', 'onion': 'onion', 'carrot': 'carrot',
                'cabbage': 'cabbage', 'cauliflower': 'cauliflower'
            }
            
            detected = 'unknown'
            for k, v in mapping.items():
                if k in top['label'].lower():
                    detected = v
                    break
            
            print(f"🔍 Vision detected crop: {detected} (Score: {top['score']:.3f})")
            return {'labels': [detected], 'scores': [top['score']], 'engine': 'clip'}
        except Exception as e:
            print(f"❌ CLIP error: {e}")
            return {'labels': ['unknown'], 'scores': [0.0], 'engine': 'error'}
'''

with open('src/vision.py', 'w', encoding='utf-8') as f:
    f.write(vision_code)
print("✅ Updated src/vision.py with potato detection")

# ============================================
# FIX 3: Update src/api.py to include potato in KNOWN_CROPS
# ============================================
with open('src/api.py', 'r', encoding='utf-8') as f:
    api_content = f.read()

# Replace KNOWN_CROPS in predict_seed endpoint
old_known = "KNOWN = ['wheat', 'rice', 'maize', 'cotton', 'soybean', 'mustard', 'tomato']"
new_known = "KNOWN = ['wheat', 'rice', 'maize', 'cotton', 'soybean', 'mustard', 'tomato', 'potato', 'onion', 'carrot', 'cabbage', 'cauliflower']"

if old_known in api_content:
    api_content = api_content.replace(old_known, new_known)
    
    # Also fix the fallback logic to use text input when available
    old_fallback = '''        if not seed_name or seed_name not in KNOWN:
            seed_name = "wheat"'''
    new_fallback = '''        if not seed_name or seed_name not in KNOWN:
            # Try to extract crop name from text input
            text_lower = seed_name.lower() if seed_name else ""
            for crop in KNOWN:
                if crop in text_lower:
                    seed_name = crop
                    break
            else:
                seed_name = "wheat"'''
    
    if old_fallback in api_content:
        api_content = api_content.replace(old_fallback, new_fallback)
    
    with open('src/api.py', 'w', encoding='utf-8') as f:
        f.write(api_content)
    print("✅ Updated src/api.py with potato in KNOWN_CROPS")
else:
    print("⚠️ Could not find KNOWN_CROPS in api.py")

# ============================================
# FIX 4: Update app.py to include potato in dropdown
# ============================================
with open('app.py', 'r', encoding='utf-8') as f:
    app_content = f.read()

# Update the seed input placeholder
old_placeholder = 'seed_input = st.text_input("Enter Seed/Plant Name")'
new_placeholder = 'seed_input = st.text_input("Enter Seed/Plant Name (e.g., wheat, potato, tomato)")'

if old_placeholder in app_content:
    app_content = app_content.replace(old_placeholder, new_placeholder)
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(app_content)
    print("✅ Updated app.py with potato in placeholder")

print("\n" + "=" * 60)
print("✅ All files updated!")
print("\n📝 Next steps:")
print("1. Regenerate data: python generate_data.py")
print("2. Retrain models: python train_models.py")
print("3. Restart backend (Ctrl+C, then run uvicorn command)")
print("4. Refresh browser")
