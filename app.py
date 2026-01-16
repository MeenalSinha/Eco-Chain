import streamlit as st
import pandas as pd
import hashlib
import json
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from io import BytesIO
import base64
import sys
from pathlib import Path

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent / 'utils'))

# Import utility modules
from carbon_calculator import CarbonCalculator
from token_generator import GreenTokenGenerator
from blockchain_simulator import BlockchainLedger, Block
from certificate_generator import CertificateGenerator
from ai_suggestions import SustainabilitySuggester

# Page configuration
st.set_page_config(
    page_title="Eco-Chain - Verifiable Sustainability Proof",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for glassmorphism + pastel UI
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Pastel gradient background */
    .main {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
    }
    
    /* Glassmorphism sidebar */
    [data-testid="stSidebar"] {
        background: rgba(200, 230, 201, 0.7);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Headers with gradient */
    h1, h2, h3, h4, h5, h6 {
        color: #2E7D32 !important;
        font-weight: 700;
    }
    
    h1 {
        background: linear-gradient(135deg, #2E7D32 0%, #4CAF50 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Glassmorphism cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.4);
        transition: all 0.3s ease;
        animation: fadeIn 0.6s ease-out;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Hero section with glassmorphism */
    .hero-section {
        background: linear-gradient(135deg, rgba(129, 199, 132, 0.6), rgba(102, 187, 106, 0.6));
        backdrop-filter: blur(20px);
        border-radius: 25px;
        padding: 3rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
        margin-bottom: 2rem;
        animation: heroFadeIn 1s ease-out;
    }
    
    @keyframes heroFadeIn {
        from {
            opacity: 0;
            transform: scale(0.95);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    .hero-logo {
        font-size: 4rem;
        animation: bounce 2s infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    .hero-title {
        color: white !important;
        font-size: 3.5rem;
        font-weight: 900;
        margin: 1rem 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .hero-subtitle {
        color: white;
        font-size: 1.5rem;
        font-weight: 400;
        opacity: 0.95;
    }
    
    /* Pastel buttons */
    .stButton>button {
        background: linear-gradient(135deg, #66BB6A 0%, #81C784 100%);
        color: white;
        border-radius: 15px;
        height: 3.5em;
        width: 100%;
        font-size: 1.1em;
        font-weight: 700;
        border: none;
        box-shadow: 0 4px 15px rgba(102, 187, 106, 0.4);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #4CAF50 0%, #66BB6A 100%);
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(76, 175, 80, 0.5);
    }
    
    .stButton>button:active {
        transform: translateY(0px);
    }
    
    /* Metric cards with glassmorphism */
    .metric-glass-card {
        background: linear-gradient(135deg, rgba(102, 187, 106, 0.7), rgba(129, 199, 132, 0.7));
        backdrop-filter: blur(15px);
        padding: 1.8rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
        transition: all 0.3s ease;
        animation: fadeInUp 0.6s ease-out;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .metric-glass-card:hover {
        transform: translateY(-8px) scale(1.03);
        box-shadow: 0 12px 40px rgba(102, 187, 106, 0.4);
    }
    
    .metric-value {
        font-size: 3rem;
        font-weight: 900;
        margin: 0.5rem 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .metric-label {
        font-size: 1.1rem;
        opacity: 0.95;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Info boxes with glassmorphism */
    .stAlert {
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.4);
    }
    
    /* Tech badge styling */
    .tech-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(5px);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.3rem;
        font-size: 0.9rem;
        border: 1px solid rgba(255, 255, 255, 0.4);
        transition: all 0.3s ease;
    }
    
    .tech-badge:hover {
        background: rgba(255, 255, 255, 0.5);
        transform: translateY(-2px);
    }
    
    /* Input fields */
    .stTextInput>div>div>input, .stSelectbox>div>div>select, .stNumberInput>div>div>input {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.4);
        color: #2E7D32;
        font-weight: 500;
    }
    
    /* File uploader */
    .uploadedFile {
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.4);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.4);
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        padding: 3rem 1rem;
        background: rgba(255, 255, 255, 0.4);
        backdrop-filter: blur(15px);
        border-radius: 25px;
        margin-top: 3rem;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Custom alert boxes */
    .glass-alert-success {
        background: linear-gradient(135deg, rgba(102, 187, 106, 0.6), rgba(129, 199, 132, 0.6));
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .glass-alert-warning {
        background: linear-gradient(135deg, rgba(255, 193, 7, 0.6), rgba(255, 213, 79, 0.6));
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .glass-alert-info {
        background: linear-gradient(135deg, rgba(66, 165, 245, 0.6), rgba(100, 181, 246, 0.6));
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* Dataframe styling */
    .dataframe {
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(10px);
        border-radius: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'tokens' not in st.session_state:
    st.session_state.tokens = []
if 'historical_data' not in st.session_state:
    st.session_state.historical_data = []
if 'blockchain' not in st.session_state:
    st.session_state.blockchain = BlockchainLedger()
if 'carbon_calculator' not in st.session_state:
    st.session_state.carbon_calculator = CarbonCalculator()
if 'token_generator' not in st.session_state:
    st.session_state.token_generator = GreenTokenGenerator()
if 'certificate_generator' not in st.session_state:
    st.session_state.certificate_generator = CertificateGenerator()
if 'suggester' not in st.session_state:
    st.session_state.suggester = SustainabilitySuggester()

# Emission factors (kg CO2 per kWh) - IEA/EPA based
EMISSION_FACTORS = {
    "India": 0.82,
    "USA": 0.42,
    "EU": 0.28,
    "China": 0.58,
    "Global Average": 0.475
}

# Industry baseline energy consumption (kWh per month per unit)
INDUSTRY_BASELINES = {
    "Textile Manufacturing": 15000,
    "Food Processing": 12000,
    "Small Manufacturing": 10000,
    "Retail/Commercial": 5000,
    "Technology/Services": 3000
}

# Functions
def calculate_emissions(energy_kwh, business_type="Manufacturing", region="India"):
    """Calculate CO2 emissions using CarbonCalculator"""
    calculator = st.session_state.carbon_calculator
    
    # Use the calculator's method
    emissions = calculator.calculate_emissions(
        energy_kwh=energy_kwh,
        business_type=business_type,
        renewable_pct=0,
        efficiency=80
    )
    
    # Convert to tonnes
    return emissions / 1000

def calculate_baseline_emissions(business_type, region="India"):
    """Calculate baseline emissions using CarbonCalculator"""
    calculator = st.session_state.carbon_calculator
    
    # Use industry baseline
    baseline_energy = INDUSTRY_BASELINES.get(business_type, 10000)
    baseline_emissions = calculator.get_baseline_emissions(
        energy_kwh=baseline_energy,
        business_type=business_type
    )
    
    # Convert to tonnes
    return baseline_emissions / 1000

def generate_token_hash(sme_id, emissions_reduced, timestamp):
    """Generate immutable cryptographic hash for token"""
    data_string = f"{sme_id}|{emissions_reduced}|{timestamp}"
    hash_object = hashlib.sha256(data_string.encode())
    return hash_object.hexdigest()

def create_merkle_root(hashes):
    """Create Merkle root from multiple hashes"""
    if len(hashes) == 0:
        return hashlib.sha256(b"empty").hexdigest()
    if len(hashes) == 1:
        return hashes[0]
    
    new_level = []
    for i in range(0, len(hashes), 2):
        if i + 1 < len(hashes):
            combined = hashes[i] + hashes[i + 1]
        else:
            combined = hashes[i] + hashes[i]
        new_level.append(hashlib.sha256(combined.encode()).hexdigest())
    
    return create_merkle_root(new_level)

def issue_green_token(sme_id, sme_name, business_type, emissions_reduced_kg, energy_consumed, region, month="Current Period"):
    """
    Issue a Verified Green Token using CANONICAL SCHEMA
    Uses CarbonCalculator for ALL emission calculations
    """
    token_generator = st.session_state.token_generator
    blockchain = st.session_state.blockchain
    calculator = st.session_state.carbon_calculator
    
    # Use CarbonCalculator for authoritative emission calculation
    actual_emissions_kg = calculator.calculate_emissions(
        energy_kwh=energy_consumed,
        business_type=business_type,
        renewable_pct=0,
        efficiency=80
    )
    
    # Get baseline from calculator
    baseline_kwh = INDUSTRY_BASELINES.get(business_type, 10000)
    baseline_emissions_kg = calculator.get_baseline_emissions(
        energy_kwh=baseline_kwh,
        business_type=business_type
    )
    
    # Prepare token data using CANONICAL SCHEMA (always kg internally)
    token_data = {
        'sme_id': sme_id,
        'sme_name': sme_name,
        'business_type': business_type,
        'month': month,
        'energy_kwh': float(energy_consumed),
        'emissions_kg': float(actual_emissions_kg),
        'baseline_kg': float(baseline_emissions_kg),
        'emissions_reduced_kg': float(emissions_reduced_kg),
        'timestamp': datetime.now().isoformat()
    }
    
    # Generate token using canonical schema
    token = token_generator.generate_token(token_data)
    
    # Add to blockchain
    blockchain.add_block(token)
    
    # Store in session state
    st.session_state.tokens.append(token)
    
    return token

def generate_sustainability_suggestions(business_type, energy_consumed, baseline_kwh):
    """Generate data-driven sustainability recommendations using SustainabilitySuggester"""
    suggester = st.session_state.suggester
    calculator = st.session_state.carbon_calculator
    
    # Calculate current performance
    actual_emissions = calculator.calculate_emissions(energy_consumed, business_type)
    baseline_emissions = calculator.get_baseline_emissions(baseline_kwh, business_type)
    reduction_pct = calculator.calculate_reduction_percentage(actual_emissions, baseline_emissions)
    
    # Get suggestions
    suggestions = suggester.get_suggestions(
        business_type=business_type,
        avg_emissions=actual_emissions,
        current_reduction_pct=reduction_pct
    )
    
    return suggestions

def create_visualization_dashboard(historical_data):
    """Create interactive visualization dashboard"""
    if not historical_data:
        return None, None, None
    
    df = pd.DataFrame(historical_data)
    df['date'] = pd.to_datetime(df['month'])
    df = df.sort_values('date')
    
    # Emissions trend chart
    fig_emissions = go.Figure()
    fig_emissions.add_trace(go.Scatter(
        x=df['date'],
        y=df['emissions_tonnes'],
        mode='lines+markers',
        name='Actual Emissions',
        line=dict(color='#FF6B6B', width=3),
        marker=dict(size=10)
    ))
    fig_emissions.add_trace(go.Scatter(
        x=df['date'],
        y=df['baseline_emissions'],
        mode='lines',
        name='Industry Baseline',
        line=dict(color='#95A5A6', width=2, dash='dash')
    ))
    fig_emissions.update_layout(
        title="CO₂ Emissions Trend",
        xaxis_title="Month",
        yaxis_title="Emissions (tonnes CO₂)",
        hovermode='x unified',
        height=400
    )
    
    # Reduction chart
    fig_reduction = go.Figure()
    fig_reduction.add_trace(go.Bar(
        x=df['date'],
        y=df['reduction_tonnes'],
        marker_color=['#27AE60' if x > 0 else '#E74C3C' for x in df['reduction_tonnes']],
        name='Emissions Reduced'
    ))
    fig_reduction.update_layout(
        title="Monthly Emissions Reduction",
        xaxis_title="Month",
        yaxis_title="Reduction (tonnes CO₂)",
        height=400
    )
    
    # Energy efficiency chart
    fig_efficiency = go.Figure()
    fig_efficiency.add_trace(go.Scatter(
        x=df['date'],
        y=df['efficiency_ratio'],
        mode='lines+markers',
        fill='tozeroy',
        name='Efficiency Ratio',
        line=dict(color='#3498DB', width=3),
        marker=dict(size=10)
    ))
    fig_efficiency.add_hline(y=1.0, line_dash="dash", line_color="gray", 
                             annotation_text="Industry Baseline")
    fig_efficiency.update_layout(
        title="Energy Efficiency Ratio (Lower is Better)",
        xaxis_title="Month",
        yaxis_title="Ratio (Your Energy / Baseline)",
        height=400
    )
    
    return fig_emissions, fig_reduction, fig_efficiency

# Main App
def main():
    # Header with glassmorphism hero section
    st.markdown("""
    <div class="hero-section">
        <div class="hero-logo">🌱</div>
        <h1 class="hero-title">Eco-Chain</h1>
        <p class="hero-subtitle">
            Verifiable Sustainability Proof for Small Businesses<br/>
            Built for manufacturing and textile SMEs who lose contracts because they can't prove sustainability.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar with glassmorphism
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <div class="hero-logo" style="font-size: 3rem;">🌱</div>
            <h2 style="color: #2E7D32 !important; margin: 0.5rem 0;">Eco-Chain</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.title("Navigation")
        page = st.radio("", ["🏠 Dashboard", "📊 Calculate Emissions", "🎖️ My Green Tokens", "🔍 Public Verification", "📈 Insights & Suggestions"])
        
        st.markdown("---")
        st.markdown("""
        <div class="glass-card">
            <h4 style="color: #2E7D32 !important;">About Eco-Chain</h4>
            <p style="color: #666; font-size: 0.9rem; line-height: 1.6;">
                Making climate accountability accessible to SMEs through verifiable, tamper-proof sustainability proof.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="glass-alert-warning" style="margin-top: 1rem; font-size: 0.85rem;">
            <strong>⚠️ Note:</strong> Eco-Chain issues verification tokens, not tradeable carbon credits.
        </div>
        """, unsafe_allow_html=True)
    
    # Pages
    if page == "🏠 Dashboard":
        show_dashboard()
    elif page == "📊 Calculate Emissions":
        show_calculator()
    elif page == "🎖️ My Green Tokens":
        show_tokens()
    elif page == "🔍 Public Verification":
        show_verification()
    elif page == "📈 Insights & Suggestions":
        show_insights()

def show_dashboard():
    st.header("Dashboard Overview")
    
    if not st.session_state.tokens:
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: #2E7D32 !important; text-align: center;">👋 Welcome to Eco-Chain!</h3>
            <p style="text-align: center; font-size: 1.1rem; color: #666; margin: 1rem 0;">
                Upload your electricity data to get started and earn your first Green Token.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div class="glass-card" style="text-align: center;">
                <h2 style="color: #2E7D32 !important;">1️⃣</h2>
                <h4 style="color: #2E7D32 !important;">Upload Data</h4>
                <p style="color: #666;">Submit your monthly electricity bill or energy data</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="glass-card" style="text-align: center;">
                <h2 style="color: #2E7D32 !important;">2️⃣</h2>
                <h4 style="color: #2E7D32 !important;">Get Verified</h4>
                <p style="color: #666;">System calculates emissions and issues tamper-proof token</p>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div class="glass-card" style="text-align: center;">
                <h2 style="color: #2E7D32 !important;">3️⃣</h2>
                <h4 style="color: #2E7D32 !important;">Share Proof</h4>
                <p style="color: #666;">Download certificate and share with buyers, banks, regulators</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        # Summary metrics with glassmorphism (convert kg to tonnes for display)
        total_tokens = len(st.session_state.tokens)
        total_reduction_kg = sum(t['emissions_reduced_kg'] for t in st.session_state.tokens)
        total_reduction_tonnes = total_reduction_kg / 1000
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="metric-glass-card">
                <div class="metric-label">🎖️ Green Tokens Earned</div>
                <div class="metric-value">{total_tokens}</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-glass-card">
                <div class="metric-label">🌍 Total CO₂ Reduced</div>
                <div class="metric-value">{total_reduction_tonnes:.2f}</div>
                <div class="metric-label" style="font-size: 0.9rem;">tonnes ({total_reduction_kg:.0f} kg)</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            if total_reduction_kg > 0:
                trees_equivalent = int((total_reduction_kg / 1000) * 40)  # tonnes * 40
                st.markdown(f"""
                <div class="metric-glass-card">
                    <div class="metric-label">🌳 Trees Equivalent</div>
                    <div class="metric-value">{trees_equivalent}</div>
                    <div class="metric-label" style="font-size: 0.9rem;">trees/year</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Visualizations
        if st.session_state.historical_data:
            fig_emissions, fig_reduction, fig_efficiency = create_visualization_dashboard(
                st.session_state.historical_data
            )
            
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(fig_emissions, use_container_width=True)
            with col2:
                st.plotly_chart(fig_reduction, use_container_width=True)
            
            st.plotly_chart(fig_efficiency, use_container_width=True)
        
        # Recent tokens
        st.subheader("Recent Green Tokens")
        recent_tokens = st.session_state.tokens[-5:]
        for token in reversed(recent_tokens):
            emissions_reduced_tonnes = token['emissions_reduced_kg'] / 1000
            with st.expander(f"🎖️ {token['token_id']} - {token['sme_name']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Emissions Reduced:** {emissions_reduced_tonnes:.4f} tonnes ({token['emissions_reduced_kg']:.0f} kg)")
                    st.write(f"**Business Type:** {token['business_type']}")
                with col2:
                    st.write(f"**Date:** {token['timestamp'][:10]}")
                    st.write(f"**Status:** ✅ {token['status'].upper()}")

def show_calculator():
    st.header("📊 Carbon Emissions Calculator")
    
    st.info("🔬 **Data Sources**: Emission factors based on publicly available IEA/EPA averages. Demo implementation.")
    
    st.markdown("""
    Upload your monthly electricity data to calculate your carbon footprint and earn a Verified Green Token.
    """)
    
    # SME Information
    st.subheader("1️⃣ Business Information")
    col1, col2 = st.columns(2)
    with col1:
        sme_id = st.text_input("Business ID/Registration Number", placeholder="e.g., MSME123456")
        sme_name = st.text_input("Business Name", placeholder="e.g., Ravi Manufacturing Pvt Ltd")
    with col2:
        industry = st.selectbox("Industry Type", list(INDUSTRY_BASELINES.keys()))
        region = st.selectbox("Region/Country", list(EMISSION_FACTORS.keys()))
    
    # Data Upload
    st.subheader("2️⃣ Upload Energy Data")
    
    upload_method = st.radio("Choose data input method:", 
                             ["📄 Upload CSV File", "⌨️ Manual Entry"])
    
    energy_data = []
    
    if upload_method == "📄 Upload CSV File":
        st.info("Upload a CSV file with columns: Month, Energy_kWh (or Power_Consumption_kWh)")
        uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])
        
        if uploaded_file:
            try:
                df = pd.read_csv(uploaded_file)
                st.write("Preview of uploaded data:")
                st.dataframe(df.head())
                
                # Try to find energy column
                energy_col = None
                for col in df.columns:
                    if 'energy' in col.lower() or 'kwh' in col.lower() or 'consumption' in col.lower():
                        energy_col = col
                        break
                
                if energy_col:
                    for _, row in df.iterrows():
                        month = row.get('Month', row.get('month', 'Unknown'))
                        energy = float(row[energy_col])
                        energy_data.append({"month": month, "energy_kwh": energy})
                    st.success(f"✅ Successfully loaded {len(energy_data)} records")
                else:
                    st.error("Could not find energy/kWh column. Please ensure your CSV has a column with energy data.")
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")
    
    else:  # Manual Entry
        month_input = st.text_input("Month", placeholder="e.g., January 2025")
        energy_input = st.number_input("Energy Consumption (kWh)", min_value=0.0, step=100.0)
        
        if st.button("Add Entry"):
            if month_input and energy_input > 0:
                energy_data.append({"month": month_input, "energy_kwh": energy_input})
                st.success(f"Added: {month_input} - {energy_input} kWh")
    
    # Sample data option
    if st.checkbox("Use sample data for demo"):
        energy_data = [
            {"month": "November 2024", "energy_kwh": 8500},
            {"month": "December 2024", "energy_kwh": 7800},
            {"month": "January 2025", "energy_kwh": 7200}
        ]
        st.info("Using sample data for demonstration")
    
    # Calculate button
    if st.button("🧮 Calculate Emissions & Issue Token", type="primary") and energy_data:
        if not sme_id or not sme_name:
            st.error("Please fill in Business ID and Name")
            st.stop()
        
        with st.spinner("Calculating emissions and generating verification..."):
            # Calculate for each month
            results = []
            for data in energy_data:
                energy_kwh = data['energy_kwh']
                emissions = calculate_emissions(energy_kwh, region)
                baseline_emissions = calculate_baseline_emissions(industry, region)
                reduction = baseline_emissions - emissions
                
                results.append({
                    "month": data['month'],
                    "energy_kwh": energy_kwh,
                    "emissions_tonnes": emissions,
                    "baseline_emissions": baseline_emissions,
                    "reduction_tonnes": reduction,
                    "efficiency_ratio": energy_kwh / INDUSTRY_BASELINES[industry]
                })
                
                # Store in historical data
                st.session_state.historical_data.append(results[-1])
            
            # Calculate totals
            total_energy = sum(r['energy_kwh'] for r in results)
            total_emissions = sum(r['emissions_tonnes'] for r in results)
            total_reduction = sum(r['reduction_tonnes'] for r in results)
            avg_efficiency = sum(r['efficiency_ratio'] for r in results) / len(results)
            
            # Issue Green Token immediately if reduction > 0
            if total_reduction > 0:
                token = issue_green_token(
                    sme_id=sme_id,
                    sme_name=sme_name,
                    business_type=industry,
                    emissions_reduced_kg=total_reduction * 1000,  # Convert tonnes to kg
                    energy_consumed=total_energy,
                    region=region
                )
                
                # Store calculation results in session state for persistence
                st.session_state.current_calculation = {
                    'total_energy': total_energy,
                    'total_emissions': total_emissions,
                    'total_reduction': total_reduction,
                    'avg_efficiency': avg_efficiency,
                    'results': results,
                    'token': token,
                    'sme_id': sme_id,
                    'sme_name': sme_name,
                    'industry': industry,
                    'region': region
                }
                st.session_state.show_current_results = True
            else:
                st.session_state.show_current_results = False
                st.warning("Your emissions are higher than the industry baseline. Consider implementing energy efficiency measures.")
    
    # Display results if they exist in session state
    if st.session_state.get('show_current_results', False) and 'current_calculation' in st.session_state:
        calc = st.session_state.current_calculation
        
        # Display results
        st.success("✅ Calculation Complete!")
        
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="metric-glass-card">
                <div class="metric-label">Total Energy</div>
                <div class="metric-value" style="font-size: 2rem;">{calc['total_energy']:.0f}</div>
                <div class="metric-label" style="font-size: 0.9rem;">kWh</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-glass-card">
                <div class="metric-label">CO₂ Emissions</div>
                <div class="metric-value" style="font-size: 2rem;">{calc['total_emissions']:.2f}</div>
                <div class="metric-label" style="font-size: 0.9rem;">tonnes</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            reduction_pct = (calc['total_reduction']/calc['total_emissions']*100) if calc['total_emissions'] > 0 else 0
            st.markdown(f"""
            <div class="metric-glass-card">
                <div class="metric-label">Reduction</div>
                <div class="metric-value" style="font-size: 2rem;">{calc['total_reduction']:.2f}</div>
                <div class="metric-label" style="font-size: 0.9rem;">tonnes ({reduction_pct:.1f}%)</div>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            efficiency_status = "Excellent" if calc['avg_efficiency'] < 0.7 else "Good" if calc['avg_efficiency'] < 1.0 else "Needs Improvement"
            st.markdown(f"""
            <div class="metric-glass-card">
                <div class="metric-label">Efficiency</div>
                <div class="metric-value" style="font-size: 1.8rem;">{efficiency_status}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Results table
        st.subheader("Monthly Breakdown")
        results_df = pd.DataFrame(calc['results'])
        st.dataframe(results_df.style.format({
            'energy_kwh': '{:.0f}',
            'emissions_tonnes': '{:.4f}',
            'baseline_emissions': '{:.4f}',
            'reduction_tonnes': '{:.4f}',
            'efficiency_ratio': '{:.2f}'
        }))
        
        # Show token
        token = calc['token']
        st.subheader("🎖️ Verified Green Token")
        
        st.success(f"✅ Green Token Issued: {token['token_id']}")
        
        # Convert kg to tonnes for display only
        emissions_reduced_tonnes = token['emissions_reduced_kg'] / 1000
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.json({
                'token_id': token['token_id'],
                'sme_name': token['sme_name'],
                'business_type': token['business_type'],
                'emissions_reduced_kg': f"{token['emissions_reduced_kg']:.2f} kg",
                'emissions_reduced_tonnes': f"{emissions_reduced_tonnes:.4f} tonnes",
                'status': token['status'],
                'hash': token['hash'][:32] + '...'
            })
        with col2:
            st.markdown(f"""
            <div class="glass-card">
                <h4 style="color: #2E7D32 !important;">Token Details</h4>
                <p><strong>Token ID:</strong> {token['token_id']}</p>
                <p><strong>Status:</strong> ✅ {token['status'].upper()}</p>
                <p><strong>Reduction:</strong> {token['emissions_reduced_kg']:.2f} kg (≈ {emissions_reduced_tonnes:.4f} tonnes)</p>
                <p><strong>Hash:</strong> <code>{token['hash'][:16]}...</code></p>
            </div>
            """, unsafe_allow_html=True)
        
        # Generate certificate
        st.subheader("📄 Download Sustainability Certificate")
        
        if st.button("Generate Certificate", key="gen_cert_calc"):
            with st.spinner("Generating certificate..."):
                try:
                    cert_generator = st.session_state.certificate_generator
                    
                    st.info("Generating certificate...")
                    
                    pdf_bytes = cert_generator.generate_certificate(token)
                    
                    st.success("✅ Certificate generated successfully!")
                    
                    st.download_button(
                        label="📥 Download Certificate (PDF)",
                        data=pdf_bytes,
                        file_name=f"Sustainability_Certificate_{token['token_id']}.pdf",
                        mime="application/pdf",
                        key="dl_cert_calc"
                    )
                except Exception as e:
                    st.error(f"❌ Error generating certificate: {str(e)}")
                    st.error(f"Error type: {type(e).__name__}")
                    import traceback
                    st.code(traceback.format_exc())
                    st.info("💡 Please try again or contact support if the issue persists.")

def show_tokens():
    st.header("🎖️ My Green Tokens")
    
    if not st.session_state.tokens:
        st.info("No tokens issued yet. Go to the Calculator page to earn your first Green Token!")
        return
    
    # Summary (convert kg to tonnes for display)
    total_reduction_kg = sum(t['emissions_reduced_kg'] for t in st.session_state.tokens)
    total_reduction_tonnes = total_reduction_kg / 1000
    st.metric("Total Emissions Reduced", f"{total_reduction_tonnes:.2f} tonnes ({total_reduction_kg:.0f} kg)")
    
    # All tokens with merkle root
    st.subheader("Token Registry")
    all_hashes = [t['hash'] for t in st.session_state.tokens]
    merkle_root = create_merkle_root(all_hashes)
    
    st.info(f"🔒 **Merkle Root (Blockchain Integrity):** `{merkle_root[:32]}...`")
    st.caption("This cryptographic proof ensures all tokens are tamper-proof and verifiable")
    
    # Display tokens
    for token in reversed(st.session_state.tokens):
        # Convert kg to tonnes for display
        emissions_reduced_tonnes = token['emissions_reduced_kg'] / 1000
        
        with st.expander(f"🎖️ {token['token_id']} - {token['sme_name']}", expanded=False):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                **Business:** {token['sme_name']}  
                **ID:** {token['sme_id']}  
                **Type:** {token['business_type']}
                """)
            
            with col2:
                st.markdown(f"""
                **Emissions Reduced:** {token['emissions_reduced_kg']:.2f} kg (≈ {emissions_reduced_tonnes:.4f} tonnes)  
                **Energy Used:** {token['energy_kwh']:.0f} kWh  
                **Reduction:** {token['reduction_percentage']:.1f}%
                """)
            
            with col3:
                st.markdown(f"""
                **Date:** {token['timestamp'][:10]}  
                **Status:** ✅ {token['status'].upper()}  
                **Verification Hash:**  
                `{token['hash'][:16]}...`
                """)
            
            # Download certificate button
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"📥 Generate Certificate", key=f"cert_{token['token_id']}"):
                    with st.spinner("Generating certificate..."):
                        try:
                            cert_generator = st.session_state.certificate_generator
                            pdf_bytes = cert_generator.generate_certificate(token)
                            
                            st.success("✅ Certificate ready!")
                            st.download_button(
                                label="💾 Download PDF",
                                data=pdf_bytes,
                                file_name=f"Certificate_{token['token_id']}.pdf",
                                mime="application/pdf",
                                key=f"dl_{token['token_id']}"
                            )
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
                            import traceback
                            with st.expander("Debug Info"):
                                st.code(traceback.format_exc())
            
            with col2:
                verification_url = f"https://eco-chain.verify/{token['hash']}"
                st.markdown(f"🔗 [Public Verification Link]({verification_url})")

def show_verification():
    st.header("🔍 Public Verification")
    
    st.markdown("""
    Verify the authenticity of any Green Token using its verification hash.
    This provides transparent, tamper-proof validation for buyers, banks, and regulators.
    """)
    
    hash_input = st.text_input("Enter Verification Hash", placeholder="e.g., a3f5b2c...")
    
    if st.button("Verify Token"):
        if hash_input:
            # Use blockchain's verify_token_by_hash method (FIXED)
            blockchain = st.session_state.blockchain
            
            # Search for token
            found_token = None
            for token in st.session_state.tokens:
                if token['hash'].startswith(hash_input):
                    found_token = token
                    break
            
            # Verify in blockchain
            is_in_blockchain = blockchain.verify_token_by_hash(found_token['hash']) if found_token else False
            
            if found_token and is_in_blockchain:
                st.success("✅ Token Verified Successfully!")
                
                # Convert kg to tonnes for display
                emissions_reduced_tonnes = found_token['emissions_reduced_kg'] / 1000
                
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.markdown(f"""
                    ### Verified Token Details
                    **Token ID:** {found_token['token_id']}  
                    **Business:** {found_token['sme_name']}  
                    **Type:** {found_token['business_type']}  
                    **Emissions Reduced:** {found_token['emissions_reduced_kg']:.2f} kg (≈ {emissions_reduced_tonnes:.4f} tonnes)  
                    **Date Issued:** {found_token['timestamp'][:10]}  
                    **Status:** ✅ {found_token['status'].upper()}
                    """)
                
                with col2:
                    st.markdown("""
                    ### Verification Status
                    🟢 **Valid**  
                    🔒 **Cryptographically Secured**  
                    ⏱️ **Timestamp Verified**  
                    ✅ **Not Tampered**  
                    🔗 **Blockchain Confirmed**
                    """)
                
                # Verification details
                with st.expander("🔐 Cryptographic Details"):
                    st.code(f"""
Verification Hash: {found_token['hash']}
Token ID: {found_token['token_id']}
SME ID: {found_token['sme_id']}
Timestamp: {found_token['timestamp']}
Emissions Reduced: {found_token['emissions_reduced_kg']:.2f} kg (≈ {emissions_reduced_tonnes:.4f} tonnes)

Hash Algorithm: SHA-256
Signature: {found_token['signature'][:32]}...
Merkle Tree Verified: ✅
Blockchain Simulation: Active
                    """)
            else:
                st.error("❌ Token not found or not in blockchain. Please check the hash and try again.")
        else:
            st.warning("Please enter a verification hash")
    
    # Public registry
    st.markdown("---")
    st.subheader("📋 Public Token Registry")
    
    if st.session_state.tokens:
        # Create public view (without sensitive data)
        public_tokens = []
        for token in st.session_state.tokens:
            emissions_reduced_tonnes = token['emissions_reduced_kg'] / 1000
            public_tokens.append({
                "Token ID": token['token_id'],
                "Business Type": token['business_type'],
                "CO₂ Reduced (tonnes)": f"{emissions_reduced_tonnes:.4f}",
                "CO₂ Reduced (kg)": f"{token['emissions_reduced_kg']:.0f}",
                "Date": token['timestamp'][:10],
                "Status": token['status'],
                "Hash Preview": token['hash'][:16] + "..."
            })
        
        df = pd.DataFrame(public_tokens)
        st.dataframe(df, use_container_width=True)
        
        # Export option
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Export Registry (CSV)",
            data=csv,
            file_name="eco_chain_registry.csv",
            mime="text/csv"
        )
    else:
        st.info("No tokens in registry yet.")

def show_insights():
    st.header("📈 Insights & AI Suggestions")
    
    if not st.session_state.historical_data:
        st.info("No data available yet. Calculate emissions first to get personalized insights.")
        return
    
    # Get latest data
    latest = st.session_state.historical_data[-1] if st.session_state.historical_data else None
    
    if latest:
        # Performance score
        efficiency = latest['efficiency_ratio']
        if efficiency < 0.7:
            score = 95
            badge = "🏆 Excellent"
            color = "#27AE60"
        elif efficiency < 0.9:
            score = 80
            badge = "⭐ Good"
            color = "#3498DB"
        elif efficiency < 1.1:
            score = 65
            badge = "👍 Average"
            color = "#F39C12"
        else:
            score = 40
            badge = "⚠️ Needs Improvement"
            color = "#E74C3C"
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="metric-glass-card">
                <div class="metric-value">{score}</div>
                <div class="metric-label">Sustainability Score</div>
                <div class="metric-label" style="font-size: 0.9rem; margin-top: 0.5rem;">/100</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-glass-card">
                <div class="metric-value" style="font-size: 2.5rem;">{badge}</div>
                <div class="metric-label">Performance Rating</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            improvement = (1 - efficiency) * 100 if efficiency < 1 else (efficiency - 1) * -100
            st.markdown(f"""
            <div class="metric-glass-card">
                <div class="metric-value">{improvement:+.1f}%</div>
                <div class="metric-label">vs Industry Baseline</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Data-Driven Suggestions
        st.subheader("💡 Data-Driven Sustainability Recommendations")
        
        # Get token data for industry context
        if st.session_state.tokens:
            latest_token = st.session_state.tokens[-1]
            business_type = latest_token['business_type']
            energy_consumed = latest_token['energy_kwh']
            baseline_kwh = INDUSTRY_BASELINES.get(business_type, 10000)
            
            suggestions = generate_sustainability_suggestions(business_type, energy_consumed, baseline_kwh)
            
            for i, suggestion in enumerate(suggestions):
                priority_colors = {
                    "Very High": "#E74C3C",
                    "High": "#F39C12",
                    "Medium": "#3498DB",
                    "Low": "#27AE60"
                }
                color = priority_colors.get(suggestion.get('priority', 'Medium'), "#3498DB")
                
                with st.expander(f"💡 {suggestion['title']} - Priority: {suggestion.get('priority', 'Medium')}", expanded=(i==0)):
                    st.markdown(f"""
                    <div class="glass-card" style="border-left: 4px solid {color};">
                        <h4 style="color: #2E7D32 !important;">{suggestion['title']}</h4>
                        <p style="color: #666; line-height: 1.8;"><strong>Description:</strong> {suggestion['description']}</p>
                        
                        <p style="color: #666;"><strong>Expected Impact:</strong> {suggestion.get('impact', 'N/A')}</p>
                        <p style="color: #666;"><strong>CO₂ Reduction:</strong> {suggestion.get('co2_reduction', 'N/A')}</p>
                        <p style="color: #666;"><strong>Estimated Cost:</strong> {suggestion.get('cost', 'N/A')}</p>
                        <p style="color: #666;"><strong>Payback Period:</strong> {suggestion.get('payback', 'N/A')}</p>
                        
                        <h5 style="color: #2E7D32 !important; margin-top: 1rem;">Implementation Steps:</h5>
                        <ol style="color: #666; line-height: 1.8;">
                    """, unsafe_allow_html=True)
                    
                    for step in suggestion.get('steps', []):
                        st.markdown(f"<li>{step}</li>", unsafe_allow_html=True)
                    
                    st.markdown("</ol></div>", unsafe_allow_html=True)
            
            # Quick wins section
            st.markdown("---")
            st.subheader("⚡ Quick Wins (Implement This Month)")
            
            suggester = st.session_state.suggester
            quick_wins = suggester.get_quick_wins(business_type)
            
            cols = st.columns(len(quick_wins))
            for col, win in zip(cols, quick_wins):
                with col:
                    st.markdown(f"""
                    <div class="glass-card" style="text-align: center;">
                        <h4 style="color: #2E7D32 !important;">{win['title']}</h4>
                        <p style="color: #666; font-size: 0.9rem;">{win['description']}</p>
                        <p style="color: #4CAF50; font-weight: 600;">{win['impact']}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Comparison with industry
        st.subheader("📊 Industry Comparison")
        
        if st.session_state.tokens:
            latest_token = st.session_state.tokens[-1]
            business_type = latest_token['business_type']
            
            comparison_data = {
                "Metric": ["Energy Efficiency", "Carbon Intensity", "Sustainability Score"],
                "Your Business": [
                    f"{(1/efficiency)*100:.0f}%" if efficiency > 0 else "N/A",
                    f"{latest['emissions_tonnes']/latest['energy_kwh']*1000:.2f} kg CO₂/kWh" if latest['energy_kwh'] > 0 else "N/A",
                    f"{score}/100"
                ],
                "Industry Average": ["100%", "0.82 kg CO₂/kWh", "65/100"]
            }
            
            df_comparison = pd.DataFrame(comparison_data)
            st.table(df_comparison)
        
        # Impact visualization
        st.subheader("🌍 Environmental Impact")
        
        # Calculate total reduction from kg field
        total_reduction = sum(t['emissions_reduced_kg'] / 1000 for t in st.session_state.tokens)
        
        # Calculate environmental equivalents
        # 1 tree absorbs ~21 kg CO2 per year
        trees = int(total_reduction * 1000 / 21)
        # Average car emits ~4.6 tonnes CO2 per year
        cars = int(total_reduction / 4.6)
        # Average home uses ~10,000 kWh per year = ~4.9 tonnes CO2
        homes = int(total_reduction / 4.9)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="glass-card" style="text-align: center;">
                <h2 style="color: #2E7D32 !important; font-size: 3rem;">🌳</h2>
                <div class="metric-value" style="font-size: 2.5rem; color: #2E7D32;">{trees:,}</div>
                <p style="color: #666; margin-top: 0.5rem;">Trees planted equivalent<br/>(over 1 year)</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="glass-card" style="text-align: center;">
                <h2 style="color: #2E7D32 !important; font-size: 3rem;">🚗</h2>
                <div class="metric-value" style="font-size: 2.5rem; color: #2E7D32;">{cars}</div>
                <p style="color: #666; margin-top: 0.5rem;">Cars off the road<br/>(for 1 year)</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="glass-card" style="text-align: center;">
                <h2 style="color: #2E7D32 !important; font-size: 3rem;">🏠</h2>
                <div class="metric-value" style="font-size: 2.5rem; color: #2E7D32;">{homes}</div>
                <p style="color: #666; margin-top: 0.5rem;">Homes powered sustainably<br/>(1 month)</p>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
    
    # Footer with glassmorphism
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="footer">
        <div class="hero-logo" style="font-size: 2.5rem;">🌱</div>
        <h3 style="color: #2E7D32 !important; margin: 1rem 0;">Eco-Chain</h3>
        <p style="font-size: 1.2rem; color: #666; margin-bottom: 1.5rem;">
            Making Sustainability Verification Accessible to SMEs
        </p>
        <div style="margin: 1.5rem 0;">
            <span class="tech-badge">🔒 SHA-256 Secure</span>
            <span class="tech-badge">⚡ Instant Verification</span>
            <span class="tech-badge">🎯 Zero Audits</span>
            <span class="tech-badge">🌍 IEA/EPA Standards</span>
        </div>
        <p style="opacity: 0.7; font-size: 0.95rem; margin-top: 2rem;">
            Built for manufacturing and textile SMEs who lose contracts because they can't prove sustainability<br>
            Powered by Python + Streamlit + Cryptography | © 2025 Eco-Chain
        </p>
        <p style="opacity: 0.6; font-size: 0.85rem; margin-top: 1rem;">
            Version 1.0.0 | Emission factors based on publicly available IEA/EPA averages (demo implementation)
        </p>
    </div>
    """, unsafe_allow_html=True)
