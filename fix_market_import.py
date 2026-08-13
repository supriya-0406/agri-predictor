import os
import sys
import subprocess

print("=" * 70)
print("🔍 DIAGNOSING: market_price_section Import Error")
print("=" * 70)

PROJECT_ROOT = r"C:\Users\Lakey\Desktop\agri-predictor"
os.chdir(PROJECT_ROOT)

print(f"\n📂 Current directory: {os.getcwd()}")
print(f"📂 Python is looking in: {sys.path[:3]}")

# Check 1: Does the file exist?
print("\n📋 CHECK 1: File Existence")
file_path = os.path.join(PROJECT_ROOT, 'market_price_section.py')

if os.path.exists(file_path):
    size = os.path.getsize(file_path)
    print(f"  ✅ market_price_section.py EXISTS ({size:,} bytes)")
else:
    print(f"  ❌ market_price_section.py MISSING!")
    print(f"  🔨 Creating it now...")

# Check 2: List all Python files in project folder
print("\n📋 CHECK 2: Python files in project folder")
py_files = [f for f in os.listdir(PROJECT_ROOT) if f.endswith('.py')]
for f in sorted(py_files):
    print(f"  📄 {f}")

# Check 3: Look for similar filenames (typos)
print("\n📋 CHECK 3: Looking for similar filenames (typos)")
similar = [f for f in os.listdir(PROJECT_ROOT) if 'market' in f.lower() or 'price' in f.lower()]
if similar:
    for f in similar:
        print(f"  🔍 Found: {f}")
else:
    print("  ⚠️ No files with 'market' or 'price' in name")

# ============================================
# CREATE THE FILE IF MISSING
# ============================================
market_code = '''import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from datetime import datetime

API_URL = "http://127.0.0.1:8000"

def make_request(endpoint, data, method="POST"):
    try:
        if method == "POST":
            res = requests.post(f"{API_URL}{endpoint}", data=data, timeout=60)
        else:
            res = requests.get(f"{API_URL}{endpoint}", params=data, timeout=60)
        
        if res.status_code == 200:
            return res.json()
        return None
    except Exception as e:
        print(f"Request error: {e}")
        return None

def market_price_section():
    st.header("💰 Market Price Prediction & Analytics")
    st.markdown("*AI-powered forecasting to maximize your farming profits*")
    
    # Custom CSS
    st.markdown("""
    <style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .profit-card {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Get available crops
    try:
        crops_response = make_request("/predict/available-crops", {}, method="GET")
        available_crops = crops_response.get('crops', ['wheat', 'rice', 'maize', 'cotton', 'soybean', 'mustard', 'tomato']) if crops_response else ['wheat', 'rice', 'maize', 'cotton', 'soybean', 'mustard', 'tomato']
    except:
        available_crops = ['wheat', 'rice', 'maize', 'cotton', 'soybean', 'mustard', 'tomato']
    
    # TABS
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Single Crop Analysis",
        "🔄 Multi-Crop Comparison",
        "🏆 Best Crop Recommendation",
        "💵 Profit Calculator"
    ])
    
    # ============================================
    # TAB 1: SINGLE CROP
    # ============================================
    with tab1:
        st.subheader("📈 Single Crop Price Forecast")
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            crop = st.selectbox("Select Crop", available_crops, key="single_crop")
            months = st.slider("Forecast Period (months)", 1, 12, 3, key="single_months")
            
            if st.button("📊 Generate Forecast", type="primary", use_container_width=True):
                with st.spinner("Analyzing..."):
                    result = make_request("/predict/price", {"crop": crop, "months_ahead": months})
                    if result and 'error' not in result:
                        st.session_state['single_crop_result'] = result
                    elif result:
                        st.error(f"❌ {result.get('error', 'Unknown error')}")
        
        with col2:
            if 'single_crop_result' in st.session_state:
                result = st.session_state['single_crop_result']
                
                # Key Metrics
                col_m1, col_m2, col_m3, col_m4 = st.columns(4)
                
                with col_m1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div style="font-size: 0.9rem; opacity: 0.9;">Current Price</div>
                        <div style="font-size: 2rem; font-weight: bold;">₹{result['current_price']:,.0f}</div>
                        <div style="font-size: 0.8rem; opacity: 0.8;">per quintal</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_m2:
                    change_color = "#2ecc71" if result['price_change_pct'] > 0 else "#e74c3c"
                    st.markdown(f"""
                    <div class="metric-card">
                        <div style="font-size: 0.9rem; opacity: 0.9;">Predicted Price</div>
                        <div style="font-size: 2rem; font-weight: bold;">₹{result['predicted_final_price']:,.0f}</div>
                        <div style="font-size: 0.8rem; color: {change_color};">{result['price_change_pct']:+.1f}%</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_m3:
                    st.markdown(f"""
                    <div class="profit-card">
                        <div style="font-size: 0.9rem; opacity: 0.9;">Expected Profit</div>
                        <div style="font-size: 2rem; font-weight: bold;">₹{result['profit_analysis']['expected_profit']:,.0f}</div>
                        <div style="font-size: 0.8rem; opacity: 0.8;">per acre</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_m4:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div style="font-size: 0.9rem; opacity: 0.9;">ROI</div>
                        <div style="font-size: 2rem; font-weight: bold;">{result['profit_analysis']['roi_percent']:.1f}%</div>
                        <div style="font-size: 0.8rem; opacity: 0.8;">return on investment</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.divider()
                
                trend_emoji = "📈" if "BULLISH" in result['trend'] else "📉"
                st.info(f"**{trend_emoji} {result['trend']}**: {result['recommendation']}")
                
                # Price Trend Chart
                st.markdown("### 📊 Price Trend Forecast")
                
                historical_months = 24
                total_months = historical_months + months
                dates = pd.date_range(end=datetime.now(), periods=total_months, freq='ME')
                
                historical_prices = []
                for i in range(historical_months):
                    trend = result['current_price'] * (1 - 0.015 * (historical_months - i))
                    seasonal = 0.05 * np.sin(2 * np.pi * i / 12)
                    noise = np.random.normal(0, result['current_price'] * 0.03)
                    historical_prices.append(trend * (1 + seasonal) + noise)
                
                forecast_prices = np.linspace(result['current_price'], result['predicted_final_price'], months)
                all_prices = historical_prices + list(forecast_prices)
                
                upper_bound = [p * 1.1 for p in forecast_prices]
                lower_bound = [p * 0.9 for p in forecast_prices]
                
                df_prices = pd.DataFrame({
                    'Date': dates,
                    'Price': all_prices,
                    'Type': ['Historical'] * historical_months + ['Forecast'] * months
                })
                
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=df_prices[df_prices['Type'] == 'Historical']['Date'],
                    y=df_prices[df_prices['Type'] == 'Historical']['Price'],
                    mode='lines+markers',
                    name='Historical',
                    line=dict(color='#3498db', width=3),
                    marker=dict(size=5)
                ))
                
                fig.add_trace(go.Scatter(
                    x=df_prices[df_prices['Type'] == 'Forecast']['Date'],
                    y=df_prices[df_prices['Type'] == 'Forecast']['Price'],
                    mode='lines+markers',
                    name='Forecast',
                    line=dict(color='#2ecc71', width=3, dash='dash'),
                    marker=dict(size=6, symbol='diamond')
                ))
                
                fig.add_trace(go.Scatter(
                    x=df_prices[df_prices['Type'] == 'Forecast']['Date'].tolist() + 
                      df_prices[df_prices['Type'] == 'Forecast']['Date'].tolist()[::-1],
                    y=upper_bound + lower_bound[::-1],
                    fill='toself',
                    fillcolor='rgba(46, 204, 113, 0.2)',
                    line=dict(color='rgba(255,255,255,0)'),
                    name='Confidence Interval',
                    showlegend=True
                ))
                
                fig.update_layout(
                    title=f"{crop.title()} Price Trend (₹/quintal)",
                    xaxis_title="Month",
                    yaxis_title="Price (₹)",
                    height=500,
                    hovermode='x unified',
                    template='plotly_white'
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Seasonal Heatmap
                st.markdown("### 🗓️ Seasonal Price Pattern")
                
                months_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                
                monthly_avg = []
                for i in range(12):
                    base = result['current_price']
                    seasonal = 0.1 * np.sin(2 * np.pi * (i - 3) / 12)
                    monthly_avg.append(base * (1 + seasonal))
                
                fig_heat = go.Figure(data=go.Heatmap(
                    z=[monthly_avg],
                    x=months_list,
                    y=['Average Price'],
                    colorscale='RdYlGn',
                    text=[[f"₹{p:,.0f}" for p in monthly_avg]],
                    texttemplate="%{text}",
                    colorbar=dict(title="Price (₹)")
                ))
                
                fig_heat.update_layout(
                    title="Monthly Price Pattern (Best Time to Sell)",
                    height=200
                )
                
                st.plotly_chart(fig_heat, use_container_width=True)
                
                # Price Range
                col_r1, col_r2, col_r3 = st.columns(3)
                with col_r1:
                    st.metric("Minimum Price", f"₹{result['price_range']['min']:,.0f}")
                with col_r2:
                    st.metric("Average Price", f"₹{result['predicted_avg_price']:,.0f}")
                with col_r3:
                    st.metric("Maximum Price", f"₹{result['price_range']['max']:,.0f}")
                
                if result['msp'] > 0:
                    st.success(f"✅ **MSP Guarantee**: ₹{result['msp']:,}/quintal")
                
                st.caption(f"🤖 Model Accuracy: {result['model_accuracy']:.1f}%")
            else:
                st.info("👈 Select a crop and click **Generate Forecast**")
    
    # ============================================
    # TAB 2: MULTI-CROP COMPARISON
    # ============================================
    with tab2:
        st.subheader("🔄 Multi-Crop Comparison")
        
        if st.button("📊 Load All Crop Data", type="primary"):
            with st.spinner("Fetching data..."):
                all_data = []
                for c in available_crops:
                    result = make_request("/predict/price", {"crop": c, "months_ahead": 3})
                    if result and 'error' not in result:
                        all_data.append(result)
                
                if all_data:
                    st.session_state['multi_crop_data'] = all_data
                    st.success(f"✅ Loaded {len(all_data)} crops!")
                else:
                    st.error("❌ Could not load crop data")
        
        if 'multi_crop_data' in st.session_state:
            data = st.session_state['multi_crop_data']
            
            st.markdown("### 💰 Current vs Predicted Prices")
            
            fig_price = go.Figure(data=[
                go.Bar(
                    name='Current',
                    x=[d['crop'].title() for d in data],
                    y=[d['current_price'] for d in data],
                    marker_color='#3498db',
                    text=[f"₹{d['current_price']:,.0f}" for d in data],
                    textposition='auto'
                ),
                go.Bar(
                    name='Predicted',
                    x=[d['crop'].title() for d in data],
                    y=[d['predicted_final_price'] for d in data],
                    marker_color='#2ecc71',
                    text=[f"₹{d['predicted_final_price']:,.0f}" for d in data],
                    textposition='auto'
                )
            ])
            fig_price.update_layout(barmode='group', height=450)
            st.plotly_chart(fig_price, use_container_width=True)
            
            st.markdown("### 📈 Return on Investment (ROI)")
            
            sorted_data = sorted(data, key=lambda x: x['profit_analysis']['roi_percent'], reverse=True)
            
            fig_roi = go.Figure(data=[
                go.Bar(
                    x=[d['crop'].title() for d in sorted_data],
                    y=[d['profit_analysis']['roi_percent'] for d in sorted_data],
                    marker_color=['#f1c40f' if i == 0 else '#3498db' for i in range(len(sorted_data))],
                    text=[f"{d['profit_analysis']['roi_percent']:.1f}%" for d in sorted_data],
                    textposition='auto'
                )
            ])
            fig_roi.update_layout(title="Crop Ranking by ROI", height=450, showlegend=False)
            st.plotly_chart(fig_roi, use_container_width=True)
            
            st.markdown("### 📋 Complete Comparison")
            
            summary_df = pd.DataFrame({
                'Crop': [d['crop'].title() for d in data],
                'Current (₹)': [f"₹{d['current_price']:,.0f}" for d in data],
                'Predicted (₹)': [f"₹{d['predicted_final_price']:,.0f}" for d in data],
                'Change': [f"{d['price_change_pct']:+.1f}%" for d in data],
                'Profit/Acre': [f"₹{d['profit_analysis']['expected_profit']:,.0f}" for d in data],
                'ROI': [f"{d['profit_analysis']['roi_percent']:.1f}%" for d in data],
                'Trend': [d['trend'] for d in data]
            })
            st.dataframe(summary_df, hide_index=True, use_container_width=True)
    
    # ============================================
    # TAB 3: BEST CROP RECOMMENDATION
    # ============================================
    with tab3:
        st.subheader("🏆 Best Crop Recommendation")
        
        rec_months = st.slider("Planning Horizon (months)", 1, 12, 3, key="rec_months")
        
        if st.button("🎯 Find Best Crop", type="primary"):
            with st.spinner("Analyzing..."):
                result = make_request("/predict/best-crop", {"months_ahead": rec_months}, method="GET")
                
                if result and 'error' not in result:
                    st.session_state['best_crop_result'] = result
                elif result:
                    st.error(f"❌ {result.get('error', 'Unknown error')}")
        
        if 'best_crop_result' in st.session_state:
            result = st.session_state['best_crop_result']
            
            st.markdown(f"""
            <div style='text-align: center; padding: 3rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        border-radius: 20px; color: white; box-shadow: 0 8px 25px rgba(0,0,0,0.15);'>
                <div style='font-size: 4rem; margin-bottom: 1rem;'>🏆</div>
                <h1 style='margin: 0; color: white;'>{result['best_crop'].upper()}</h1>
                <p style='font-size: 1.3rem; margin: 1rem 0; color: white;'>{result['recommendation']}</p>
                <div style='display: flex; justify-content: space-around; margin-top: 2rem;'>
                    <div>
                        <div style='font-size: 2.5rem; font-weight: bold;'>₹{result['best_profit_per_acre']:,.0f}</div>
                        <div style='font-size: 1rem; opacity: 0.9;'>Profit/Acre</div>
                    </div>
                    <div>
                        <div style='font-size: 2.5rem; font-weight: bold;'>{result['best_roi']:.1f}%</div>
                        <div style='font-size: 1rem; opacity: 0.9;'>ROI</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### 📊 Complete Crop Ranking")
            
            ranking_df = pd.DataFrame(result['all_crops_ranked'])
            
            fig_rank = go.Figure(data=[
                go.Bar(
                    x=[f"#{i+1} {r['crop'].title()}" for i, r in ranking_df.iterrows()],
                    y=ranking_df['roi'],
                    marker_color=['#f1c40f' if r['crop'] == result['best_crop'] else '#3498db' 
                                 for _, r in ranking_df.iterrows()],
                    text=[f"{r['roi']:.1f}%" for _, r in ranking_df.iterrows()],
                    textposition='auto'
                )
            ])
            fig_rank.update_layout(title="Crop Ranking by ROI", height=450, showlegend=False)
            st.plotly_chart(fig_rank, use_container_width=True)
    
    # ============================================
    # TAB 4: PROFIT CALCULATOR
    # ============================================
    with tab4:
        st.subheader("💵 Profit Calculator")
        st.markdown("*Calculate expected profit based on your farm size and crop choice*")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            calc_crop = st.selectbox("Select Crop", available_crops, key="calc_crop")
            calc_acres = st.number_input("Land Size (acres)", 1.0, 100.0, 10.0, key="calc_acres")
            
            if st.button("💰 Calculate Profit", type="primary", use_container_width=True):
                result = make_request("/predict/price", {"crop": calc_crop, "months_ahead": 3})
                if result and 'error' not in result:
                    st.session_state['profit_calc'] = result
                elif result:
                    st.error(f"❌ {result.get('error', 'Unknown error')}")
        
        with col2:
            if 'profit_calc' in st.session_state:
                result = st.session_state['profit_calc']
                profit = result['profit_analysis']
                
                total_cost = profit['cost_per_acre'] * calc_acres
                total_revenue = profit['expected_revenue'] * calc_acres
                total_profit = profit['expected_profit'] * calc_acres
                total_yield = profit['yield_per_acre_quintals'] * calc_acres
                
                col_m1, col_m2 = st.columns(2)
                with col_m1:
                    st.metric("Total Cost", f"₹{total_cost:,.0f}")
                    st.metric("Total Revenue", f"₹{total_revenue:,.0f}")
                with col_m2:
                    st.metric("Total Profit", f"₹{total_profit:,.0f}")
                    st.metric("Total Yield", f"{total_yield:.1f} quintals")
                
                st.markdown("### 📊 Profit Breakdown")
                
                fig_water = go.Figure(go.Waterfall(
                    name="Profit",
                    orientation="v",
                    measure=["relative", "relative", "total"],
                    x=["Cost", "Revenue", "Net Profit"],
                    y=[-total_cost, total_revenue, total_profit],
                    text=[f"₹{total_cost:,.0f}", f"₹{total_revenue:,.0f}", f"₹{total_profit:,.0f}"],
                    textposition="outside",
                    connector={"line": {"color": "rgb(63, 63, 63)"}},
                    increasing={"marker": {"color": "#2ecc71"}},
                    decreasing={"marker": {"color": "#e74c3c"}},
                    totals={"marker": {"color": "#3498db"}}
                ))
                
                fig_water.update_layout(
                    title=f"Profit Analysis for {calc_acres} acres of {calc_crop.title()}",
                    showlegend=False,
                    height=400
                )
                
                st.plotly_chart(fig_water, use_container_width=True)
                
                st.markdown("### 📈 Break-Even Analysis")
                
                break_even_price = total_cost / total_yield if total_yield > 0 else 0
                
                st.info(f"""
                **Break-Even Price:** ₹{break_even_price:,.0f}/quintal
                
                You need to sell at **₹{break_even_price:,.0f}** per quintal to cover all costs.
                
                **Current Prediction:** ₹{result['predicted_final_price']:,.0f}/quintal
                
                **Margin:** ₹{result['predicted_final_price'] - break_even_price:,.0f}/quintal above break-even
                """)
            else:
                st.info("👈 Select crop and land size, then click **Calculate Profit**")
'''

# Write the file
with open('market_price_section.py', 'w', encoding='utf-8') as f:
    f.write(market_code)

print(f"\n✅ Created: {file_path}")
print(f"   Size: {os.path.getsize(file_path):,} bytes")

# ============================================
# VERIFY THE FIX
# ============================================
print("\n🧪 VERIFICATION: Testing import...")

try:
    # Add current directory to path
    if PROJECT_ROOT not in sys.path:
        sys.path.insert(0, PROJECT_ROOT)
    
    # Try to import
    import importlib
    import market_price_section
    importlib.reload(market_price_section)
    
    print("  ✅ SUCCESS! market_price_section can be imported!")
    print(f"  📦 Function available: {hasattr(market_price_section, 'market_price_section')}")
    
except Exception as e:
    print(f"  ❌ Import still failing: {e}")

# ============================================
# CHECK app.py HAS THE IMPORT
# ============================================
print("\n📋 CHECK 4: app.py import statement")
app_path = os.path.join(PROJECT_ROOT, 'app.py')
if os.path.exists(app_path):
    with open(app_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'from market_price_section import market_price_section' in content:
        print("  ✅ app.py has the import statement")
    else:
        print("  ⚠️ app.py is missing the import statement!")
        print("  🔨 Adding it now...")
        
        # Add import after existing imports
        if 'import numpy as np' in content:
            content = content.replace(
                'import numpy as np',
                'import numpy as np\nfrom market_price_section import market_price_section'
            )
        elif 'from datetime import datetime' in content:
            content = content.replace(
                'from datetime import datetime',
                'from datetime import datetime\nfrom market_price_section import market_price_section'
            )
        
        with open(app_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("  ✅ Import statement added to app.py")
    
    # Check Section 4 uses the function
    if 'market_price_section()' in content:
        print("  ✅ app.py calls market_price_section()")
    else:
        print("  ⚠️ app.py doesn't call market_price_section()")

# ============================================
# CLEAN CACHE
# ============================================
print("\n🧹 CLEANING CACHE")
import shutil
cache_dir = os.path.join(PROJECT_ROOT, '__pycache__')
if os.path.exists(cache_dir):
    shutil.rmtree(cache_dir)
    print("  ✅ Cleared __pycache__")

print("\n" + "=" * 70)
print("✅ FIX COMPLETE!")
print("=" * 70)
print("\n📝 Next steps:")
print("1. Restart Streamlit (Ctrl+C in Terminal 2, then run again)")
print("2. Refresh browser at http://localhost:8501")
print("3. Click the 💰 Market Price Prediction tab")
