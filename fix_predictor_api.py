import os

# ============================================
# FIX 1: src/predictor.py (Complete Rewrite)
# ============================================
predictor_code = '''import joblib
import pandas as pd
import os

class AgriPredictor:
    def __init__(self):
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Load tool/breeding/seed models
        try:
            self.tool_model = joblib.load(os.path.join(base_path, 'models/tool_demand.pkl'))
            self.tool_meta = joblib.load(os.path.join(base_path, 'models/tool_demand_encoders.pkl'))
            self.tool_encoders = self.tool_meta.get('encoders', {})
            self.tool_features = self.tool_meta.get('feature_cols', [])
            print(f"✅ Tool model loaded with features: {self.tool_features}")
        except Exception as e:
            print(f"⚠️ Tool model not loaded: {e}")
            self.tool_model = None
        
        try:
            self.breed_model = joblib.load(os.path.join(base_path, 'models/breeding_predictor.pkl'))
            self.breed_meta = joblib.load(os.path.join(base_path, 'models/breeding_predictor_encoders.pkl'))
            self.breed_encoders = self.breed_meta.get('encoders', {})
            self.breed_features = self.breed_meta.get('feature_cols', [])
        except Exception as e:
            print(f"⚠️ Breeding model not loaded: {e}")
            self.breed_model = None
        
        try:
            self.seed_model = joblib.load(os.path.join(base_path, 'models/seed_advisor.pkl'))
            self.seed_meta = joblib.load(os.path.join(base_path, 'models/seed_advisor_encoders.pkl'))
            self.seed_encoders = self.seed_meta.get('encoders', {})
            self.seed_features = self.seed_meta.get('feature_cols', [])
        except Exception as e:
            print(f"⚠️ Seed model not loaded: {e}")
            self.seed_model = None
        
        # Load price models
        self.price_models = {}
        self.price_models_info = {}
        try:
            self.price_models_info = joblib.load(os.path.join(base_path, 'models/price_models_info.pkl'))
            for crop, info in self.price_models_info.items():
                self.price_models[crop] = joblib.load(info['model_path'])
            print(f"✅ Loaded {len(self.price_models)} price prediction models")
        except Exception as e:
            print(f"⚠️ Price models not loaded: {e}")
    
    def predict_tool(self, tool_name, region, season, rainfall, temp, crop_cycle, land_acres=5.0):
        tool_name = str(tool_name).lower().strip()
        region = str(region).lower().strip()
        season = str(season).lower().strip()
        crop_cycle = str(crop_cycle).lower().strip()
        land_acres = float(land_acres) if land_acres else 5.0
        
        if self.tool_model is None:
            return {"error": "Model not loaded"}
        
        try:
            encoded_vals = {}
            mapping = {
                'tool_type': tool_name,
                'season': season,
                'region': region,
                'crop_cycle': crop_cycle,
                'land_acres': land_acres,
                'rainfall_mm': float(rainfall),
                'temperature_c': float(temp)
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
            
            per_acre_hours = round(demand / max(land_acres, 0.1), 2)
            
            if land_acres <= 2:
                size_category = "small farm"
                size_advice = "Consider renting equipment instead of buying."
            elif land_acres <= 10:
                size_category = "medium farm"
                size_advice = "Equipment ownership is cost-effective."
            else:
                size_category = "large farm"
                size_advice = "Invest in owned machinery for long-term savings."
            
            if crop_cycle == 'harvesting' and tool_name in ['sickle', 'harvester']:
                if demand > 80:
                    rec = f"🔥 PEAK HARVEST DEMAND: {land_acres} acres need {demand:.0f} hrs. Service {tool_name} before harvest."
                else:
                    rec = f"✅ Moderate harvest demand for {tool_name} on {land_acres} acres."
            elif crop_cycle in ['sowing', 'land_preparation'] and tool_name in ['tractor', 'plough', 'seed_drill']:
                if demand > 100:
                    rec = f"🔥 HIGH SOWING DEMAND: {land_acres} acres require {demand:.0f} hrs. Schedule pre-season maintenance."
                else:
                    rec = f"✅ Normal sowing demand for {tool_name} on {land_acres} acres."
            else:
                if demand < 60:
                    rec = f"✅ Low usage ({demand:.0f} hrs) for {tool_name} on {land_acres} acres during {crop_cycle}."
                else:
                    rec = f"⚡ {demand:.0f} hrs expected for {tool_name} on {land_acres} acres."
            
            return {
                "tool": tool_name,
                "land_acres": land_acres,
                "farm_category": size_category,
                "crop_cycle": crop_cycle,
                "season": season,
                "predicted_demand_hours": round(demand, 2),
                "per_acre_hours": per_acre_hours,
                "optimal_maintenance_days": maint,
                "usage_recommendation": rec,
                "farm_advice": size_advice
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
    
    def predict_price(self, crop, months_ahead=3):
        crop = str(crop).lower().strip()
        
        if crop not in self.price_models:
            return {"error": f"Price model not available for {crop}. Available: {list(self.price_models.keys())}"}
        
        try:
            model = self.price_models[crop]
            info = self.price_models_info[crop]
            
            days_ahead = months_ahead * 30
            future = model.make_future_dataframe(periods=days_ahead)
            forecast = model.predict(future)
            
            future_forecast = forecast.tail(days_ahead)
            
            current_price = info['latest_price']
            avg_predicted = future_forecast['yhat'].mean()
            min_predicted = future_forecast['yhat_lower'].min()
            max_predicted = future_forecast['yhat_upper'].max()
            final_price = future_forecast['yhat'].iloc[-1]
            
            price_change_pct = ((final_price - current_price) / current_price) * 100
            
            import pandas as pd
            price_df = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data/crop_prices.csv'))
            crop_meta = price_df[price_df['crop'] == crop].iloc[-1]
            
            cost_per_acre = crop_meta['cost_per_acre']
            yield_per_acre = crop_meta['yield_per_acre']
            msp = crop_meta['msp']
            
            expected_revenue = final_price * yield_per_acre
            expected_profit = expected_revenue - cost_per_acre
            roi_pct = (expected_profit / cost_per_acre) * 100
            
            if price_change_pct > 10:
                trend = "📈 STRONG BULLISH"
                advice = f"Excellent time to plant {crop}. Prices expected to rise {price_change_pct:.1f}%."
            elif price_change_pct > 0:
                trend = "📊 SLIGHTLY BULLISH"
                advice = f"Moderate price increase expected. {crop} is a safe choice."
            elif price_change_pct > -10:
                trend = "📉 SLIGHTLY BEARISH"
                advice = f"Small price dip expected. Consider alternative crops."
            else:
                trend = "⚠️ STRONG BEARISH"
                advice = f"Prices may drop {abs(price_change_pct):.1f}%. Avoid planting {crop}."
            
            return {
                "crop": crop,
                "months_ahead": months_ahead,
                "current_price": round(current_price, 2),
                "predicted_avg_price": round(avg_predicted, 2),
                "predicted_final_price": round(final_price, 2),
                "price_range": {"min": round(min_predicted, 2), "max": round(max_predicted, 2)},
                "price_change_pct": round(price_change_pct, 2),
                "trend": trend,
                "msp": msp,
                "profit_analysis": {
                    "cost_per_acre": cost_per_acre,
                    "yield_per_acre_quintals": yield_per_acre,
                    "expected_revenue": round(expected_revenue, 2),
                    "expected_profit": round(expected_profit, 2),
                    "roi_percent": round(roi_pct, 2)
                },
                "recommendation": advice,
                "model_accuracy": info['accuracy']
            }
        except Exception as e:
            return {"error": str(e)}
    
    def get_best_crop_recommendation(self, months_ahead=3):
        if not self.price_models:
            return {"error": "Price models not loaded"}
        
        try:
            results = []
            for crop in self.price_models.keys():
                prediction = self.predict_price(crop, months_ahead)
                if 'error' not in prediction:
                    results.append({
                        'crop': crop,
                        'predicted_price': prediction['predicted_final_price'],
                        'profit': prediction['profit_analysis']['expected_profit'],
                        'roi': prediction['profit_analysis']['roi_percent'],
                        'trend': prediction['trend'],
                        'price_change': prediction['price_change_pct']
                    })
            
            results.sort(key=lambda x: x['roi'], reverse=True)
            
            return {
                "best_crop": results[0]['crop'],
                "best_roi": results[0]['roi'],
                "best_profit_per_acre": results[0]['profit'],
                "all_crops_ranked": results,
                "recommendation": f"Based on {months_ahead}-month price forecast, plant {results[0]['crop']} for maximum profit (₹{results[0]['profit']:,.0f}/acre, {results[0]['roi']:.1f}% ROI)."
            }
        except Exception as e:
            return {"error": str(e)}
'''

# ============================================
# FIX 2: src/api.py (Complete Rewrite with ALL endpoints)
# ============================================
api_code = '''from fastapi import FastAPI, UploadFile, File, Form, HTTPException
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
    import traceback
    traceback.print_exc()

app = FastAPI(title="AgriShare AI Predictor")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

SEASON_MAP = {
    'rainy season': 'rainy_season', 'winter season': 'winter_season',
    'summer season': 'summer_season', 'year round': 'rainy_season',
    'rainy_season': 'rainy_season', 'winter_season': 'winter_season',
    'summer_season': 'summer_season'
}

def normalize_season(s):
    return SEASON_MAP.get(s.lower().strip(), 'rainy_season')

@app.get("/health")
def health():
    return {
        "status": "OK",
        "vision_loaded": vision is not None and getattr(vision, 'loaded', False),
        "predictor_loaded": predictor is not None,
        "tool_model_loaded": predictor.tool_model is not None if predictor else False,
        "price_models_count": len(predictor.price_models) if predictor else 0
    }

@app.post("/predict/tool")
async def predict_tool(
    tool_name: str = Form(""), region: str = Form("north"), season: str = Form("rainy_season"),
    rainfall: float = Form(800.0), temperature: float = Form(28.0), crop_cycle: str = Form("sowing"),
    land_acres: float = Form(5.0), image: UploadFile = File(None)
):
    try:
        KNOWN_TOOLS = ['tractor', 'plough', 'harrows', 'cultivator', 'seed_drill', 'sprayer', 'pump', 'sickle', 'harvester']
        tool_name = str(tool_name).lower().strip() if tool_name else ""
        detection_source = "user_input"
        vision_engine = "none"
        
        if image and image.filename:
            try:
                contents = await image.read()
                if len(contents) > 0:
                    img = Image.open(io.BytesIO(contents)).convert("RGB")
                    if vision and getattr(vision, 'loaded', False):
                        result = vision.classify_tool(img)
                        detected = result['labels'][0]
                        confidence = result['scores'][0]
                        vision_engine = result.get('engine', 'clip')
                        if detected != 'unknown' and confidence > 0.2:
                            tool_name = detected
                            detection_source = f"vision_ai ({vision_engine})"
            except Exception as e:
                print(f"⚠️ Image processing failed: {e}")
        
        if not tool_name or tool_name not in KNOWN_TOOLS:
            tool_name = "tractor"
            detection_source = "default"
        
        season = normalize_season(season)
        if predictor is None:
            return {"error": "Predictor not loaded"}
        
        result = predictor.predict_tool(tool_name, region, season, rainfall, temperature, crop_cycle, land_acres)
        result['detection_source'] = detection_source
        result['vision_engine'] = vision_engine
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/breeding")
async def predict_breeding(
    animal_name: str = Form(""), male_age: float = Form(3.5), female_age: float = Form(3.0),
    male_weight: float = Form(350.0), female_weight: float = Form(300.0), female_milk: float = Form(18.0),
    health_score: float = Form(85.0), genetic_diversity: float = Form(0.7), region: str = Form("north"),
    image: UploadFile = File(None)
):
    try:
        KNOWN = ['cow', 'buffalo', 'goat', 'sheep']
        animal_name = str(animal_name).lower().strip() if animal_name else ""
        detection_source = "user_input"
        
        if image and image.filename:
            try:
                contents = await image.read()
                if len(contents) > 0:
                    img = Image.open(io.BytesIO(contents)).convert("RGB")
                    if vision and getattr(vision, 'loaded', False):
                        result = vision.classify_animal(img)
                        detected = result['labels'][0]
                        if detected != 'unknown' and result['scores'][0] > 0.2:
                            animal_name = detected
                            detection_source = f"vision_ai ({result.get('engine', 'clip')})"
            except:
                pass
        
        if not animal_name or animal_name not in KNOWN:
            animal_name = "cow"
        
        if predictor is None:
            return {"error": "Predictor not loaded"}
        
        breed_map = {'cow': 'sahiwal', 'buffalo': 'murrah', 'goat': 'jamunapari', 'sheep': 'deccani'}
        result = predictor.predict_breeding(animal_name, breed_map.get(animal_name, 'sahiwal'),
                                           male_age, female_age, male_weight, female_weight,
                                           female_milk, health_score, genetic_diversity, region)
        result['detection_source'] = detection_source
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/seed")
async def predict_seed(
    seed_name: str = Form(""), soil_ph: float = Form(6.5), rainfall: float = Form(900.0),
    temperature: float = Form(26.0), humidity: float = Form(70.0), season: str = Form("rainy_season"),
    organic_carbon: float = Form(1.2), region: str = Form("north"), image: UploadFile = File(None)
):
    try:
        KNOWN = ['wheat', 'rice', 'maize', 'cotton', 'soybean', 'mustard', 'tomato']
        seed_name = str(seed_name).lower().strip() if seed_name else ""
        detection_source = "user_input"
        
        if image and image.filename:
            try:
                contents = await image.read()
                if len(contents) > 0:
                    img = Image.open(io.BytesIO(contents)).convert("RGB")
                    if vision and getattr(vision, 'loaded', False):
                        result = vision.classify_plant_seed(img)
                        detected = result['labels'][0]
                        if detected != 'unknown' and result['scores'][0] > 0.2:
                            seed_name = detected
                            detection_source = f"vision_ai ({result.get('engine', 'clip')})"
            except:
                pass
        
        if not seed_name or seed_name not in KNOWN:
            seed_name = "wheat"
        
        season = normalize_season(season)
        if predictor is None:
            return {"error": "Predictor not loaded"}
        
        result = predictor.predict_seed(seed_name, soil_ph, rainfall, temperature, humidity, season, organic_carbon, region)
        result['detection_source'] = detection_source
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/price")
async def predict_price(crop: str = Form("wheat"), months_ahead: int = Form(3)):
    try:
        if predictor is None:
            return {"error": "Predictor not loaded"}
        return predictor.predict_price(crop, months_ahead)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/predict/best-crop")
async def get_best_crop(months_ahead: int = 3):
    try:
        if predictor is None:
            return {"error": "Predictor not loaded"}
        return predictor.get_best_crop_recommendation(months_ahead)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/predict/available-crops")
async def get_available_crops():
    if predictor is None or not hasattr(predictor, 'price_models_info'):
        return {"crops": ["wheat", "rice", "maize", "cotton", "soybean", "mustard", "tomato"], "count": 7}
    return {
        "crops": list(predictor.price_models_info.keys()),
        "count": len(predictor.price_models_info)
    }
'''

# Write both files
with open('src/predictor.py', 'w', encoding='utf-8') as f:
    f.write(predictor_code)
print("✅ Fixed src/predictor.py")

with open('src/api.py', 'w', encoding='utf-8') as f:
    f.write(api_code)
print("✅ Fixed src/api.py")

print("\n🎉 Both files rewritten! Now restart the backend.")
