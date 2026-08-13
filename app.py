import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json
import numpy as np
from datetime import datetime
from market_price_section import market_price_section

API_URL = "http://127.0.0.1:8000"

# ============================================
# 🎨 PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="AgriShare AI - Smart Farming Platform",
    layout="wide",
    page_icon="🌾",
    initial_sidebar_state="expanded"
)

# ============================================
# 💎 CUSTOM CSS - PROFESSIONAL DESIGN
# ============================================
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8edf3 100%);
    }
    
    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Hero Header */
    .hero-header {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 40px rgba(17, 153, 142, 0.3);
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    
    .hero-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: pulse 4s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 0.8; }
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        margin: 0;
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        position: relative;
        z-index: 1;
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        margin: 1rem 0 0 0;
        opacity: 0.95;
        position: relative;
        z-index: 1;
    }
    
    /* Feature badges */
    .feature-badges {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin-top: 1.5rem;
        flex-wrap: wrap;
        position: relative;
        z-index: 1;
    }
    
    .feature-badge {
        background: rgba(255,255,255,0.2);
        padding: 0.5rem 1.2rem;
        border-radius: 50px;
        color: white;
        font-weight: 600;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.3);
        transition: all 0.3s ease;
    }
    
    .feature-badge:hover {
        background: rgba(255,255,255,0.3);
        transform: translateY(-3px);
    }
    
    /* Section Cards */
    .section-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.08);
        margin-bottom: 2rem;
        transition: all 0.3s ease;
        border: 1px solid rgba(0,0,0,0.05);
    }
    
    .section-card:hover {
        box-shadow: 0 12px 40px rgba(0,0,0,0.12);
        transform: translateY(-2px);
    }
    
    /* Section Headers */
    .section-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 3px solid #f0f0f0;
    }
    
    .section-icon {
        font-size: 2.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .section-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #2c3e50;
        margin: 0;
    }
    
    .section-subtitle {
        color: #7f8c8d;
        font-size: 1rem;
        margin: 0.3rem 0 0 0;
    }
    
    /* Input Groups */
    .input-group {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        border-left: 5px solid #667eea;
    }
    
    .input-group-label {
        font-size: 1.1rem;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Metric Cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        text-align: center;
        transition: all 0.3s ease;
        border: 1px solid rgba(0,0,0,0.05);
        height: 100%;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }
    
    .metric-card-blue {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .metric-card-green {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
    }
    
    .metric-card-orange {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
    }
    
    .metric-card-purple {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
    }
    
    .metric-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        margin-bottom: 0.5rem;
        font-weight: 500;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        margin: 0.3rem 0;
    }
    
    .metric-unit {
        font-size: 0.85rem;
        opacity: 0.8;
    }
    
    /* Recommendation Box */
    .recommendation-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.3);
        margin: 1.5rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .recommendation-box::before {
        content: '💡';
        position: absolute;
        top: -20px;
        right: -20px;
        font-size: 8rem;
        opacity: 0.1;
    }
    
    .recommendation-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0 0 1rem 0;
        color: white;
    }
    
    .recommendation-text {
        font-size: 1.1rem;
        line-height: 1.6;
        margin: 0;
        color: white;
        position: relative;
        z-index: 1;
    }
    
    /* Primary Button */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.8rem 2rem;
        border-radius: 50px;
        font-weight: 700;
        font-size: 1rem;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: white;
        padding: 0.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 0.8rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Enhanced Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%);
        border-right: 3px solid #e0e0e0;
    }
    
    [data-testid="stSidebar"] .stRadio > label {
        display: none;
    }
    
    [data-testid="stSidebar"] .stRadio > div {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }
    
    [data-testid="stSidebar"] .stRadio > div > label {
        background: white;
        padding: 1rem 1.2rem;
        border-radius: 12px;
        border: 2px solid #e0e0e0;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 600;
        font-size: 0.95rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    [data-testid="stSidebar"] .stRadio > div > label:hover {
        border-color: #667eea;
        transform: translateX(5px);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
        background: linear-gradient(135deg, #f8f9ff 0%, #ffffff 100%);
    }
    
    [data-testid="stSidebar"] .stRadio > div > label[data-baseweb="radio"] {
        display: flex;
        align-items: center;
        gap: 0.8rem;
    }
    
    [data-testid="stSidebar"] .stRadio > div > label[aria-checked="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-color: #667eea;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        transform: translateX(5px);
    }
    
    [data-testid="stSidebar"] .stRadio > div > label[aria-checked="true"]::before {
        filter: brightness(0) invert(1);
    }
    
    /* Radio button circle styling */
    [data-testid="stSidebar"] .stRadio div[data-baseweb="radio"] div:first-child {
        background: white;
        border: 2px solid #667eea;
    }
    
    [data-testid="stSidebar"] .stRadio div[data-baseweb="radio"][aria-checked="true"] div:first-child {
        background: #667eea;
        border-color: #667eea;
    }
    
    /* Sidebar dividers */
    [data-testid="stSidebar"] hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        margin: 1rem 0;
    }
    
    /* Sidebar headers */
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] h4 {
        color: #2c3e50;
    }
    
    /* Smooth scrolling in sidebar */
    [data-testid="stSidebar"] .block-container {
        scroll-behavior: smooth;
    }
    
    /* Animation for section change */
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .stRadio > div > label {
        animation: slideIn 0.3s ease;
    }
    
    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #2196f3;
        margin: 1rem 0;
    }
    
    .success-box {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #4caf50;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #ff9800;
        margin: 1rem 0;
    }
    
    /* Stats grid */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #7f8c8d;
        margin-top: 3rem;
        border-top: 2px solid #ecf0f1;
    }
    
    /* Loading animation */
    @keyframes shimmer {
        0% { background-position: -1000px 0; }
        100% { background-position: 1000px 0; }
    }
    
    /* Divider */
    .custom-divider {
        height: 3px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        margin: 2rem 0;
        border-radius: 3px;
    }
    
    /* Quick action buttons */
    .quick-action {
        background: white;
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        border: 2px solid #e0e0e0;
    }
    
    .quick-action:hover {
        border-color: #667eea;
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# 🎨 HERO HEADER
# ============================================
st.markdown("""
<div class="hero-header">
    <h1 class="hero-title">🌾 AgriShare AI</h1>
    <p class="hero-subtitle">Smart Farming Platform - AI-Powered Insights for Modern Agriculture</p>
    <div class="feature-badges">
        <div class="feature-badge">🚜 Tool Analysis</div>
        <div class="feature-badge">🐄 Breeding Predictor</div>
        <div class="feature-badge">🌱 Seed Advisor</div>
        <div class="feature-badge">💰 Market Prices</div>
        <div class="feature-badge">🤖 AI Powered</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================
# 📡 HELPER FUNCTION
# ============================================
def make_request(endpoint, data, img=None, method="POST"):
    files = {}
    if img:
        files = {"image": (img.name, img.getvalue(), img.type)}
    try:
        if method == "POST":
            res = requests.post(f"{API_URL}{endpoint}", data=data, files=files, timeout=60)
        else:
            res = requests.get(f"{API_URL}{endpoint}", params=data, timeout=60)
        
        if res.status_code == 200:
            return res.json()
        else:
            st.error(f"⚠️ Backend Error {res.status_code}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to backend. Please start uvicorn server.")
        return None
    except Exception as e:
        st.error(f"❌ Request failed: {e}")
        return None

# ============================================
# 🎯 COLORFUL INTERACTIVE SIDEBAR
# ============================================
with st.sidebar:
    # Beautiful Header
    st.markdown("""
    <div style='text-align: center; padding: 1.5rem; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 15px; margin-bottom: 1.5rem; 
                box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);'>
        <div style='font-size: 3rem; margin-bottom: 0.5rem;'>🌾</div>
        <h2 style='color: white; margin: 0; font-size: 1.8rem; font-weight: 800;'>AgriShare AI</h2>
        <p style='color: rgba(255,255,255,0.9); font-size: 0.95rem; margin: 0.5rem 0 0 0;'>
            Smart Farming Platform
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Section Selection with Custom Styling
    st.markdown("""
    <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                padding: 1rem; border-radius: 12px; margin-bottom: 1rem;
                box-shadow: 0 4px 15px rgba(240, 147, 251, 0.3);'>
        <h3 style='color: white; margin: 0; text-align: center; font-size: 1.2rem;'>
            🎯 Select Your Section
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Interactive Section Selection
    section = st.radio(
        "Choose a section to explore:",
        ["🏠 Dashboard", "🚜 Tool Analysis", "🐄 Breeding Predictor", 
         "🌱 Seed & Plant Advisor", "💰 Market Price Prediction"],
        index=0,
        label_visibility="collapsed"
    )
    
    # Section Description Cards
    st.markdown("---")
    
    section_info = {
        "🏠 Dashboard": {
            "emoji": "🏠",
            "title": "Welcome Home",
            "desc": "Overview of all features",
            "color": "#667eea"
        },
        "🚜 Tool Analysis": {
            "emoji": "🚜",
            "title": "Tool Demand",
            "desc": "Predict usage & maintenance",
            "color": "#11998e"
        },
        "🐄 Breeding Predictor": {
            "emoji": "🐄",
            "title": "Animal Breeding",
            "desc": "Genetic compatibility analysis",
            "color": "#f39c12"
        },
        "🌱 Seed & Plant Advisor": {
            "emoji": "🌱",
            "title": "Crop Planning",
            "desc": "Seeds, fertilizer & yield",
            "color": "#e74c3c"
        },
        "💰 Market Price Prediction": {
            "emoji": "💰",
            "title": "Price Forecast",
            "desc": "Past, present & future prices",
            "color": "#9b59b6"
        }
    }
    
    current = section_info[section]
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, {current['color']}22 0%, {current['color']}11 100%); 
                padding: 1.5rem; border-radius: 15px; 
                border-left: 5px solid {current['color']};
                box-shadow: 0 4px 15px rgba(0,0,0,0.08);'>
        <div style='font-size: 2.5rem; text-align: center; margin-bottom: 0.5rem;'>
            {current['emoji']}
        </div>
        <h3 style='color: {current['color']}; margin: 0; text-align: center; font-size: 1.3rem;'>
            {current['title']}
        </h3>
        <p style='color: #555; text-align: center; margin: 0.5rem 0 0 0; font-size: 0.95rem;'>
            {current['desc']}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Tips Section
    st.markdown("---")
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); 
                padding: 1.2rem; border-radius: 12px; 
                box-shadow: 0 4px 15px rgba(252, 182, 159, 0.3);'>
        <h4 style='color: #d35400; margin: 0 0 0.8rem 0; text-align: center;'>
            💡 Quick Tips
        </h4>
        <ul style='color: #555; margin: 0; padding-left: 1.2rem; font-size: 0.9rem; line-height: 1.8;'>
            <li>📸 Upload photos for auto-detection</li>
            <li>🎯 Enter exact land size for accuracy</li>
            <li>📥 Export reports as JSON</li>
            <li>🌾 AI detects category automatically</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # AI Models Info
    st.markdown("---")
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); 
                padding: 1.2rem; border-radius: 12px; 
                box-shadow: 0 4px 15px rgba(168, 237, 234, 0.3);'>
        <h4 style='color: #16a085; margin: 0 0 0.8rem 0; text-align: center;'>
            🤖 AI Technologies
        </h4>
        <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem;'>
            <div style='background: white; padding: 0.5rem; border-radius: 8px; text-align: center;'>
                <div style='font-size: 1.5rem;'>🧠</div>
                <div style='font-size: 0.75rem; color: #555; font-weight: 600;'>XGBoost</div>
            </div>
            <div style='background: white; padding: 0.5rem; border-radius: 8px; text-align: center;'>
                <div style='font-size: 1.5rem;'>👁️</div>
                <div style='font-size: 0.75rem; color: #555; font-weight: 600;'>CLIP Vision</div>
            </div>
            <div style='background: white; padding: 0.5rem; border-radius: 8px; text-align: center;'>
                <div style='font-size: 1.5rem;'>📈</div>
                <div style='font-size: 0.75rem; color: #555; font-weight: 600;'>Prophet</div>
            </div>
            <div style='background: white; padding: 0.5rem; border-radius: 8px; text-align: center;'>
                <div style='font-size: 1.5rem;'>⚡</div>
                <div style='font-size: 0.75rem; color: #555; font-weight: 600;'>FastAPI</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 1rem; color: #7f8c8d; font-size: 0.85rem;'>
        <p style='margin: 0;'>🌾 Built with ❤️ for Indian Farmers</p>
        <p style='margin: 0.3rem 0 0 0; font-size: 0.75rem;'>© 2026 AgriShare AI</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# 🏠 DASHBOARD (HOME)
# ============================================
if section == "🏠 Dashboard":
    st.markdown("""
    <div class="section-card">
        <h2 style='color: #2c3e50; margin-top: 0;'>👋 Welcome to AgriShare AI</h2>
        <p style='font-size: 1.1rem; color: #555;'>
            Your intelligent farming companion powered by advanced AI and machine learning.
            Get data-driven insights to maximize your agricultural productivity and profits.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature Cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="section-card" style='border-top: 5px solid #667eea;'>
            <h3>🚜 Tool Demand Analysis</h3>
            <p>Predict tool usage, maintenance schedules, and operational costs based on your farm size and crop cycle.</p>
            <ul>
                <li>✅ AI-powered demand prediction</li>
                <li>✅ Maintenance scheduling</li>
                <li>✅ Cost & fuel analysis</li>
                <li>✅ Photo detection</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="section-card" style='border-top: 5px solid #f5576c;'>
            <h3>🌱 Seed & Plant Advisor</h3>
            <p>Get complete planting plans with seed quantities, fertilizer needs, and yield predictions.</p>
            <ul>
                <li>✅ Yield prediction per acre</li>
                <li>✅ Seed quantity calculator</li>
                <li>✅ Fertilizer recommendations</li>
                <li>✅ Soil analysis</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="section-card" style='border-top: 5px solid #11998e;'>
            <h3>🐄 Cross-Breeding Predictor</h3>
            <p>AI-powered breeding analysis with compatibility checks and offspring trait predictions.</p>
            <ul>
                <li>✅ Offspring trait prediction</li>
                <li>✅ Compatibility analysis</li>
                <li>✅ Hybrid vigor calculation</li>
                <li>✅ 21 Indian breeds</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="section-card" style='border-top: 5px solid #f39c12;'>
            <h3>💰 Market Price Prediction</h3>
            <p>AI-powered price forecasting for tools, animals, and seeds with past-present-future analysis.</p>
            <ul>
                <li>✅ Time-series forecasting</li>
                <li>✅ Price trend visualization</li>
                <li>✅ Smart recommendations</li>
                <li>✅ Multi-category support</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick Start Guide
    st.markdown("""
    <div class="section-card" style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;'>
        <h2 style='color: white; margin-top: 0;'>🚀 Quick Start Guide</h2>
        <div style='display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-top: 1rem;'>
            <div style='text-align: center;'>
                <div style='font-size: 2.5rem;'>1️⃣</div>
                <h4 style='color: white; margin: 0.5rem 0;'>Select Section</h4>
                <p style='margin: 0; font-size: 0.9rem;'>Choose from sidebar</p>
            </div>
            <div style='text-align: center;'>
                <div style='font-size: 2.5rem;'>2️⃣</div>
                <h4 style='color: white; margin: 0.5rem 0;'>Enter Details</h4>
                <p style='margin: 0; font-size: 0.9rem;'>Fill in the form</p>
            </div>
            <div style='text-align: center;'>
                <div style='font-size: 2.5rem;'>3️⃣</div>
                <h4 style='color: white; margin: 0.5rem 0;'>AI Analyzes</h4>
                <p style='margin: 0; font-size: 0.9rem;'>Smart predictions</p>
            </div>
            <div style='text-align: center;'>
                <div style='font-size: 2.5rem;'>4️⃣</div>
                <h4 style='color: white; margin: 0.5rem 0;'>Get Insights</h4>
                <p style='margin: 0; font-size: 0.9rem;'>Beautiful results</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# 🚜 SECTION 1: TOOL ANALYSIS
# ============================================
elif section == "🚜 Tool Analysis":
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">🚜</div>
        <div>
            <h2 class="section-title">Tool Demand Analysis</h2>
            <p class="section-subtitle">AI-powered tool usage prediction and maintenance scheduling</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Vertical Input Form
    with st.container():
        st.markdown("""
        <div class="input-group">
            <div class="input-group-label">🌍 Farm Details</div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            land_acres = st.number_input("Land Area (acres)", 0.1, 500.0, 5.0, 0.5, key="tool_acres")
        with col2:
            region = st.selectbox("Region", ["north", "south", "east", "west", "central"], key="tool_region")
        with col3:
            season = st.selectbox("Season", ["Rainy Season", "Winter Season", "Summer Season"], key="tool_season")
        with col4:
            crop_cycle = st.selectbox("Crop Cycle", 
                ["land_preparation", "sowing", "weeding", "irrigation", "harvesting", "post_harvest"],
                key="tool_cycle")
        
        st.markdown("""
        <div class="input-group" style='border-left-color: #11998e;'>
            <div class="input-group-label">🚜 Tool Details</div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            tool_input = st.text_input("Tool Name", placeholder="e.g., tractor, sickle", key="tool_name")
        with col2:
            rainfall = st.number_input("Rainfall (mm)", 100, 2500, 800, key="tool_rain")
        with col3:
            temp = st.number_input("Temperature (°C)", 10, 45, 28, key="tool_temp")
        
        img = st.file_uploader("📸 Upload Tool Photo (Optional)", type=["jpg", "png", "jpeg"], key="tool_img")
        
        if st.button("🔍 Analyze Tool", type="primary"):
            with st.spinner("🤖 AI is analyzing your tool requirements..."):
                data = {
                    "tool_name": tool_input, "region": region, "season": season,
                    "rainfall": rainfall, "temperature": temp, "crop_cycle": crop_cycle,
                    "land_acres": land_acres
                }
                result = make_request("/predict/tool", data, img)
                if result and 'error' not in result:
                    st.session_state['tool_result'] = result
    
    # Display Results
    if 'tool_result' in st.session_state:
        result = st.session_state['tool_result']
        
        if 'error' not in result:
            st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)
            
            # Header Banner
            st.markdown(f"""
            <div class="recommendation-box" style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);'>
                <div class="recommendation-title">🚜 {result['tool'].title()} Analysis Report</div>
                <div class="recommendation-text">
                    🌍 {result.get('land_acres', 5)} acres | 
                    🌱 {result['crop_cycle'].replace('_', ' ').title()} | 
                    🌦️ {result['season'].replace('_', ' ').title()}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Time Metrics
            st.markdown("### ⏱️ Time & Usage Metrics")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card metric-card-blue">
                    <div class="metric-icon">📊</div>
                    <div class="metric-label">Total Demand</div>
                    <div class="metric-value">{result['predicted_demand_hours']:.1f}</div>
                    <div class="metric-unit">hours</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card metric-card-green">
                    <div class="metric-icon">⚡</div>
                    <div class="metric-label">Per Acre</div>
                    <div class="metric-value">{result.get('per_acre_hours', 0):.2f}</div>
                    <div class="metric-unit">hrs/acre</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card metric-card-orange">
                    <div class="metric-icon">⏱️</div>
                    <div class="metric-label">Days to Complete</div>
                    <div class="metric-value">{result.get('days_to_complete', 0)}</div>
                    <div class="metric-unit">days</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="metric-card metric-card-purple">
                    <div class="metric-icon">🔧</div>
                    <div class="metric-label">Maintenance Due</div>
                    <div class="metric-value">{result['optimal_maintenance_days']}</div>
                    <div class="metric-unit">days</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Cost Metrics
            st.markdown("### 💰 Cost & Resource Analysis")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-icon">💵</div>
                    <div class="metric-label">Cost per Hour</div>
                    <div class="metric-value">₹{result.get('cost_per_hour', 0):,}</div>
                    <div class="metric-unit">per hour</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-icon">💰</div>
                    <div class="metric-label">Total Cost</div>
                    <div class="metric-value">₹{result.get('total_estimated_cost', 0):,.0f}</div>
                    <div class="metric-unit">total</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-icon">⛽</div>
                    <div class="metric-label">Fuel Required</div>
                    <div class="metric-value">{result.get('fuel_required_liters', 0):.1f}</div>
                    <div class="metric-unit">liters</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-icon">👷</div>
                    <div class="metric-label">Labor Needed</div>
                    <div class="metric-value">{result.get('labor_required', 0)}</div>
                    <div class="metric-unit">workers</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Recommendation
            st.markdown(f"""
            <div class="recommendation-box">
                <div class="recommendation-title">💡 AI Recommendation</div>
                <div class="recommendation-text">{result['usage_recommendation']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Additional advice
            if result.get('cost_advice'):
                st.warning(f"**💰 Cost Advice:** {result['cost_advice']}")
            if result.get('farm_advice'):
                st.info(f"**💼 Farm Advice:** {result['farm_advice']}")
            
            # Export
            with st.expander("📥 Export Report"):
                json_data = json.dumps(result, indent=2)
                st.download_button(
                    "📄 Download JSON Report",
                    data=json_data,
                    file_name=f"{result['tool']}_analysis.json",
                    mime="application/json"
                )

# ============================================
# 🐄 SECTION 2: BREEDING PREDICTOR (FIXED)
# ============================================
elif section == "🐄 Breeding Predictor":
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">🐄</div>
        <div>
            <h2 class="section-title">Cross-Breeding Predictor</h2>
            <p class="section-subtitle">AI-powered breeding analysis with genetic compatibility</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 🔑 FIXED: Species-specific breed and weight options
    SPECIES_CONFIG = {
        'cow': {
            'breeds': ['sahiwal', 'gir', 'red_sindhi', 'tharparkar', 'holstein', 'jersey'],
            'weight_range': (200, 800),
            'weight_default': 400,
            'milk_range': (10, 35),
            'milk_default': 18
        },
        'buffalo': {
            'breeds': ['murrah', 'niliravi', 'jaffarabadi', 'mehsana', 'surti'],
            'weight_range': (300, 1200),
            'weight_default': 600,
            'milk_range': (12, 30),
            'milk_default': 20
        },
        'goat': {
            'breeds': ['jamunapari', 'beetal', 'sirohi', 'black_bengal', 'osmanabadi'],
            'weight_range': (20, 80),  # 🔑 FIXED: 20-80 kg for goats
            'weight_default': 45,
            'milk_range': (1, 5),
            'milk_default': 2.5
        },
        'sheep': {
            'breeds': ['deccani', 'mandya', 'mecheri', 'bellary', 'dorper'],
            'weight_range': (30, 100),  # 🔑 FIXED: 30-100 kg for sheep
            'weight_default': 55,
            'milk_range': (0.5, 3),
            'milk_default': 1.5
        }
    }
    
    # Male Details
    st.markdown("""
    <div class="input-group" style='border-left-color: #3498db;'>
        <div class="input-group-label">♂️ Male Animal Details</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        male_species = st.selectbox("Species", ["cow", "buffalo", "goat", "sheep"], key="male_species")
    
    # 🔑 FIXED: Dynamic breed and weight based on species
    male_config = SPECIES_CONFIG[male_species]
    
    with col2:
        male_breed = st.selectbox("Breed", male_config['breeds'], key="male_breed")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        m_age = st.number_input("Age (years)", 1.0, 12.0, 3.5, key="m_age")
    with col2:
        # 🔑 FIXED: Species-specific weight range with float conversion
        m_wt = st.number_input(
            f"Weight (kg) [{male_config['weight_range'][0]}-{male_config['weight_range'][1]}]", 
            min_value=float(male_config['weight_range'][0]), 
            max_value=float(male_config['weight_range'][1]), 
            value=float(male_config['weight_default']), 
            key="m_wt"
        )
    with col3:
        male_img = st.file_uploader("📸 Photo (Optional)", type=["jpg", "png", "jpeg"], key="male_img")
    
    # Female Details
    st.markdown("""
    <div class="input-group" style='border-left-color: #e74c3c;'>
        <div class="input-group-label">♀️ Female Animal Details</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        female_species = st.selectbox("Species", ["cow", "buffalo", "goat", "sheep"], key="female_species")
    
    female_config = SPECIES_CONFIG[female_species]
    
    with col2:
        female_breed = st.selectbox("Breed", female_config['breeds'], key="female_breed")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        f_age = st.number_input("Age (years)", 1.0, 10.0, 3.0, key="f_age")
    with col2:
        # 🔑 FIXED: Species-specific weight range with float conversion
        f_wt = st.number_input(
            f"Weight (kg) [{female_config['weight_range'][0]}-{female_config['weight_range'][1]}]", 
            min_value=float(female_config['weight_range'][0]), 
            max_value=float(female_config['weight_range'][1]), 
            value=float(female_config['weight_default']), 
            key="f_wt"
        )
    with col3:
        # 🔑 FIXED: Species-specific milk range with float conversion
        f_milk = st.number_input(
            f"Milk (L/day) [{female_config['milk_range'][0]}-{female_config['milk_range'][1]}]", 
            min_value=float(female_config['milk_range'][0]), 
            max_value=float(female_config['milk_range'][1]), 
            value=float(female_config['milk_default']), 
            step=0.5,
            key="f_milk"
        )
    with col4:
        female_img = st.file_uploader("📸 Photo (Optional)", type=["jpg", "png", "jpeg"], key="female_img")
    
    # Common Parameters
    st.markdown("""
    <div class="input-group" style='border-left-color: #9b59b6;'>
        <div class="input-group-label">🧬 Genetic Parameters</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        health = st.slider("Health Score", 50, 100, 85, key="health")
    with col2:
        genetics = st.slider("Genetic Diversity", 0.2, 0.95, 0.7, 0.05, key="genetics")
    with col3:
        region_b = st.selectbox("Region", ["north", "south", "east", "west", "central"], key="region_b")
    
    if st.button("🔍 Predict Offspring", type="primary"):
        with st.spinner("🧬 Analyzing genetic compatibility..."):
            files = {}
            if male_img:
                files['male_image'] = (male_img.name, male_img.getvalue(), male_img.type)
            if female_img:
                files['female_image'] = (female_img.name, female_img.getvalue(), female_img.type)
            
            data = {
                "male_species": male_species, "male_breed": male_breed,
                "male_age": m_age, "male_weight": m_wt,
                "female_species": female_species, "female_breed": female_breed,
                "female_age": f_age, "female_weight": f_wt, "female_milk": f_milk,
                "health_score": health, "genetic_diversity": genetics, "region": region_b
            }
            
            try:
                res = requests.post(f"{API_URL}/predict/breeding", data=data, files=files, timeout=60)
                if res.status_code == 200:
                    st.session_state['breeding_result'] = res.json()
                else:
                    st.error(f"❌ Error: {res.text}")
            except Exception as e:
                st.error(f"❌ Request failed: {e}")
    
    # Display Results
    if 'breeding_result' in st.session_state:
        result = st.session_state['breeding_result']
        
        if 'error' in result:
            st.error(f"❌ {result['error']}")
            if 'suggestion' in result:
                st.info(f"💡 **Suggestion:** {result['suggestion']}")
        else:
            st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)
            
            compat = result['compatibility_score']
            
            # Compatibility Banner
            if compat >= 80:
                gradient = "linear-gradient(135deg, #11998e 0%, #38ef7d 100%)"
                status = "🎯 EXCELLENT COMPATIBILITY"
            elif compat >= 60:
                gradient = "linear-gradient(135deg, #2193b0 0%, #6dd5ed 100%)"
                status = "✅ GOOD COMPATIBILITY"
            elif compat >= 40:
                gradient = "linear-gradient(135deg, #f7971e 0%, #ffd200 100%)"
                status = "⚠️ MODERATE COMPATIBILITY"
            else:
                gradient = "linear-gradient(135deg, #cb2d3e 0%, #ef473a 100%)"
                status = "❌ LOW COMPATIBILITY"
            
            st.markdown(f"""
            <div style='background: {gradient}; padding: 2rem; border-radius: 20px; 
                        color: white; text-align: center; box-shadow: 0 8px 25px rgba(0,0,0,0.15);'>
                <h2 style='margin: 0; color: white;'>{status}</h2>
                <div style='font-size: 4rem; font-weight: bold; margin: 1rem 0;'>{compat:.1f}%</div>
                <p style='font-size: 1.2rem; margin: 0;'>
                    <strong>{result['male_species'].title()}</strong> ({result['male_breed'].title()}) ♂️
                    &nbsp;×&nbsp;
                    <strong>{result['female_species'].title()}</strong> ({result['female_breed'].title()}) ♀️
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Offspring Traits
            st.markdown("### 🐣 Predicted Offspring Traits")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card metric-card-blue">
                    <div class="metric-icon">🏋️</div>
                    <div class="metric-label">Birth Weight</div>
                    <div class="metric-value">{result['offspring_weight_kg']:.1f}</div>
                    <div class="metric-unit">kg</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card metric-card-green">
                    <div class="metric-icon">🥛</div>
                    <div class="metric-label">Milk Potential</div>
                    <div class="metric-value">{result['offspring_milk_potential_lpd']:.1f}</div>
                    <div class="metric-unit">L/day</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card metric-card-purple">
                    <div class="metric-icon">🛡️</div>
                    <div class="metric-label">Disease Resistance</div>
                    <div class="metric-value">{result['disease_resistance_score']:.1f}</div>
                    <div class="metric-unit">out of 100</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="metric-card metric-card-orange">
                    <div class="metric-icon">🎯</div>
                    <div class="metric-label">Success Rate</div>
                    <div class="metric-value">{result['breeding_success_prob']:.1f}%</div>
                    <div class="metric-unit">probability</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Recommendation
            st.markdown(f"""
            <div class="recommendation-box" style='background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);'>
                <div class="recommendation-title">💡 Expert Recommendation</div>
                <div class="recommendation-text">{result['recommendation']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Genetic Benefit
            if result.get('is_cross_breed'):
                st.success(f"🌟 **Hybrid Vigor:** {result.get('genetic_benefit', 'Hybrid vigor expected')}")
            
            # Species-specific info
            st.info(f"""
            **📊 Species Information:**
            - **{male_species.title()}** typically weighs {male_config['weight_range'][0]}-{male_config['weight_range'][1]} kg
            - **{female_species.title()}** typically weighs {female_config['weight_range'][0]}-{female_config['weight_range'][1]} kg
            - Expected offspring weight: **{result['offspring_weight_kg']:.1f} kg**
            """)

# ============================================
# 🌱 SECTION 3: SEED & PLANT ADVISOR
# ============================================
elif section == "🌱 Seed & Plant Advisor":
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">🌱</div>
        <div>
            <h2 class="section-title">Seed & Plant Advisor</h2>
            <p class="section-subtitle">Complete planting plan with seed, fertilizer, and yield predictions</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Farm Details
    st.markdown("""
    <div class="input-group">
        <div class="input-group-label">🌍 Farm Details</div>
    </div>
    """, unsafe_allow_html=True)
    
    land_acres = st.number_input("Land Area (acres)", 0.1, 500.0, 5.0, 0.5, key="seed_land")
    
    # Crop Details
    st.markdown("""
    <div class="input-group" style='border-left-color: #11998e;'>
        <div class="input-group-label">🌱 Crop Details</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        seed_input = st.text_input("Crop Name", placeholder="e.g., wheat, potato", key="seed_name")
    with col2:
        season_s = st.selectbox("Season", ["Rainy Season", "Winter Season", "Summer Season"], key="seed_season")
    with col3:
        region_s = st.selectbox("Region", ["north", "south", "east", "west", "central"], key="region_s")
    
    # Soil & Weather
    st.markdown("""
    <div class="input-group" style='border-left-color: #f39c12;'>
        <div class="input-group-label">🌍 Soil & Weather Conditions</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        ph = st.number_input("Soil pH", 4.0, 9.0, 6.5, key="seed_ph")
    with col2:
        rain = st.number_input("Rainfall (mm)", 200, 3000, 900, key="seed_rain")
    with col3:
        temp_s = st.number_input("Temperature (°C)", 10, 40, 26, key="seed_temp")
    with col4:
        hum = st.number_input("Humidity (%)", 30, 95, 70, key="seed_hum")
    
    org_c = st.number_input("Organic Carbon (%)", 0.5, 4.0, 1.2, 0.1, key="seed_org")
    img = st.file_uploader("📸 Upload Crop Photo (Optional)", type=["jpg", "png", "jpeg"], key="seed_img")
    
    if st.button("🔍 Analyze Planting Potential", type="primary"):
        with st.spinner("🌱 Analyzing your planting conditions..."):
            data = {
                "seed_name": seed_input, "soil_ph": ph, "rainfall": rain, "temperature": temp_s,
                "humidity": hum, "season": season_s, "organic_carbon": org_c, 
                "region": region_s, "land_acres": land_acres
            }
            result = make_request("/predict/seed", data, img)
            if result and 'error' not in result:
                st.session_state['seed_result'] = result
    
    # Display Results
    if 'seed_result' in st.session_state:
        result = st.session_state['seed_result']
        
        if 'error' not in result:
            st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)
            
            crop_name = result['crop'].title()
            acres = result.get('land_acres', 5.0)
            
            # Header
            st.markdown(f"""
            <div class="recommendation-box" style='background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);'>
                <div class="recommendation-title">🌱 {crop_name} Planting Plan</div>
                <div class="recommendation-text">
                    🌍 {acres} acres | 🌦️ {result['season'].replace('_', ' ').title()} | 📍 {result['region'].title()}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Yield Metrics
            st.markdown("### 🌾 Expected Yield")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card metric-card-blue">
                    <div class="metric-icon">📊</div>
                    <div class="metric-label">Yield per Acre</div>
                    <div class="metric-value">{result.get('expected_yield_per_acre', 0):.2f}</div>
                    <div class="metric-unit">tons</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card metric-card-green">
                    <div class="metric-icon">🎯</div>
                    <div class="metric-label">Total Yield</div>
                    <div class="metric-value">{result.get('total_expected_yield', 0):.2f}</div>
                    <div class="metric-unit">tons</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card metric-card-orange">
                    <div class="metric-icon">🌟</div>
                    <div class="metric-label">Suitability</div>
                    <div class="metric-value">{result['seasonal_suitability_score']:.0f}%</div>
                    <div class="metric-unit">score</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                status = "✅ Optimal" if result['seasonal_suitability_score'] > 75 else "⚠️ Wait"
                st.markdown(f"""
                <div class="metric-card metric-card-purple">
                    <div class="metric-icon">📅</div>
                    <div class="metric-label">Planting Window</div>
                    <div class="metric-value">{status}</div>
                    <div class="metric-unit">timing</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Seed Requirements
            st.markdown("### 🌱 Seed Requirements")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-icon">🌾</div>
                    <div class="metric-label">Seed Type</div>
                    <div class="metric-value" style='font-size: 1.2rem;'>{result.get('seed_type', 'Seeds').title()}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-icon">📏</div>
                    <div class="metric-label">Per Acre</div>
                    <div class="metric-value">{result.get('seed_per_acre_kg', 0):.2f}</div>
                    <div class="metric-unit">kg</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-icon">🎯</div>
                    <div class="metric-label">Total Seeds</div>
                    <div class="metric-value">{result.get('total_seed_kg', 0):.2f}</div>
                    <div class="metric-unit">kg</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-icon">💰</div>
                    <div class="metric-label">Seed Cost</div>
                    <div class="metric-value">₹{result.get('total_seed_cost', 0):,.0f}</div>
                    <div class="metric-unit">total</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Fertilizer Requirements
            st.markdown("### 🧪 Fertilizer Requirements")
            fert = result.get('fertilizer_per_acre', {})
            total_fert = result.get('total_fertilizer', {})
            fert_cost = result.get('fertilizer_cost', {})
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📏 Per Acre**")
                st.info(f"""
                🔵 Nitrogen: **{fert.get('nitrogen_kg', 0)} kg**  
                🟡 Phosphorus: **{fert.get('phosphorus_kg', 0)} kg**  
                🔴 Potassium: **{fert.get('potassium_kg', 0)} kg**  
                ⚪ Urea: **{fert.get('urea_kg', 0)} kg**  
                ⚪ DAP: **{fert.get('dap_kg', 0)} kg**  
                ⚪ MOP: **{fert.get('mop_kg', 0)} kg**  
                🟤 Organic: **{fert.get('organic_ton', 0)} tons**
                """)
            
            with col2:
                st.markdown(f"**🎯 Total for {acres} Acres**")
                st.success(f"""
                ⚪ Urea: **{total_fert.get('urea_kg', 0)} kg**  
                ⚪ DAP: **{total_fert.get('dap_kg', 0)} kg**  
                ⚪ MOP: **{total_fert.get('mop_kg', 0)} kg**  
                🟤 Organic: **{total_fert.get('organic_manure_ton', 0)} tons**  
                🧪 Micronutrients: **{result.get('micronutrients', 'As needed')}**
                """)
            
            # Cost Summary
            st.markdown("### 💰 Investment Summary")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card metric-card-blue">
                    <div class="metric-icon">🌱</div>
                    <div class="metric-label">Seed Cost</div>
                    <div class="metric-value">₹{result.get('total_seed_cost', 0):,.0f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card metric-card-orange">
                    <div class="metric-icon">🧪</div>
                    <div class="metric-label">Fertilizer Cost</div>
                    <div class="metric-value">₹{fert_cost.get('total_cost', 0):,.0f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            total_investment = result.get('total_seed_cost', 0) + fert_cost.get('total_cost', 0)
            with col3:
                st.markdown(f"""
                <div class="metric-card metric-card-green">
                    <div class="metric-icon">💼</div>
                    <div class="metric-label">Total Investment</div>
                    <div class="metric-value">₹{total_investment:,.0f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Plant Spacing
            st.markdown("### 📐 Plant Spacing Guide")
            st.info(f"**🌱 Recommended Spacing:** {result.get('plant_spacing', 'Standard spacing')}")
            
            # Soil Analysis
            st.markdown("### 🌍 Soil Analysis")
            col1, col2 = st.columns(2)
            
            with col1:
                if ph < 6.0:
                    st.warning(result.get('soil_ph_status', ''))
                elif ph > 7.5:
                    st.error(result.get('soil_ph_status', ''))
                else:
                    st.success(result.get('soil_ph_status', ''))
            
            with col2:
                if org_c < 1.0:
                    st.warning(result.get('organic_carbon_status', ''))
                else:
                    st.success(result.get('organic_carbon_status', ''))
            
            # Export
            with st.expander("📥 Export Complete Report"):
                json_data = json.dumps(result, indent=2)
                st.download_button(
                    "📄 Download JSON Report",
                    data=json_data,
                    file_name=f"{crop_name}_planting_report.json",
                    mime="application/json"
                )

# ============================================
# 💰 SECTION 4: MARKET PRICE PREDICTION
# ============================================
elif section == "💰 Market Price Prediction":
    market_price_section()

# ============================================
# 🎨 FOOTER
# ============================================
st.markdown("""
<div class="footer">
    <h3>🌾 AgriShare AI - Smart Farming Platform</h3>
    <p>Powered by XGBoost, Prophet, and CLIP Vision AI</p>
    <p>📊 Trained on realistic agricultural datasets | 🇮🇳 Built for Indian farmers</p>
    <p style='font-size: 0.85rem; margin-top: 1rem;'>© 2026 AgriShare AI. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
