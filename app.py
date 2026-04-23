import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib
import warnings
import base64
from datetime import datetime
warnings.filterwarnings("ignore")

# ─── Get Dataset ────────────────────────────────────────────────────────────


import gdown
import os

@st.cache_data
def load_transaction_data():
    """Load cleaned transaction data from Google Drive"""
    
    # Google Drive file ID - REPLACE WITH YOUR ACTUAL ID
    FILE_ID = "https://drive.google.com/file/d/1-E_0ehmwzwrWUk4ZT8RLVfjM_FwHLd10/view?usp=drivesdk"  
    
    local_filename = "OnlineRetail_Cleaned.csv"
    
    # Download if file doesn't exist locally
    if not os.path.exists(local_filename):
        with st.spinner("📥 Downloading dataset (first time only)... This may take a moment ⏳"):
            # Construct download URL
            url = f"https://drive.google.com/uc?id={FILE_ID}"
            
            try:
                gdown.download(url, local_filename, quiet=False)
                st.success("✅ Dataset downloaded successfully!")
            except Exception as e:
                st.error(f"❌ Error downloading file: {e}")
                st.info("Make sure the file is shared with 'Anyone with the link'")
                return None
    
    # Load the data
    try:
        df = pd.read_csv(local_filename)
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
        return df
    except Exception as e:
        st.error(f"❌ Error reading CSV: {e}")
        return None



# ─── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Customer Intelligence Platform",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Load image as base64 ───────────────────────────────────────────────────
def get_image_base64(image_path):
    try:
        with open(image_path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        return data
    except Exception:
        return None

LOGO_B64 = get_image_base64("image.jpg")

# ─── Custom CSS ────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
#MainMenu, footer { visibility: hidden; }
.block-container { padding: 1.2rem 2rem 2rem; }

.app-header {
    background: linear-gradient(135deg, #0F2B3D 0%, #1B4F6E 70%, #2C7DA0 100%);
    border-radius: 16px;
    padding: 20px 32px;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.app-header h1 { color: #fff; font-size: 24px; font-weight: 700; margin: 0; }
.app-header p { color: rgba(255,255,255,0.75); font-size: 12px; margin: 6px 0 0; }
.header-badge {
    background: rgba(255,255,255,0.12);
    color: #fff;
    font-size: 11px;
    padding: 6px 16px;
    border-radius: 30px;
    border: 1px solid rgba(255,255,255,0.2);
    white-space: nowrap;
}

.kpi-wrap { display: flex; gap: 12px; margin-bottom: 1.5rem; flex-wrap: wrap; }
.kpi-card {
    flex: 1;
    min-width: 140px;
    background: linear-gradient(135deg, #F0F9F4 0%, #E8F5E9 100%);
    border: 1px solid #C8E6D9;
    border-radius: 16px;
    padding: 16px 20px;
    text-align: center;
    transition: all 0.3s ease;
    cursor: pointer;
}
.kpi-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 24px rgba(0,0,0,0.12);
    background: linear-gradient(135deg, #E8F5E9 0%, #C8E6D9 100%);
    border-color: #2C7DA0;
}
.kpi-card .val { font-size: 28px; font-weight: 800; color: #1B4F6E; line-height: 1.2; letter-spacing: -0.5px; }
.kpi-card .lbl { font-size: 11px; color: #5A7A8C; margin-top: 8px; text-transform: uppercase; letter-spacing: 0.8px; font-weight: 600; }

.sec-hdr {
    font-size: 13px;
    font-weight: 700;
    color: #1B4F6E;
    border-left: 4px solid #2C7DA0;
    padding-left: 12px;
    margin: 1.5rem 0 0.8rem;
}

.insight {
    background: #E8F4F8;
    border-left: 4px solid #2C7DA0;
    border-radius: 0 10px 10px 0;
    padding: 12px 18px;
    font-size: 13px;
    color: #1E3A5F;
    margin-top: 0.8rem;
}

.pred-box {
    background: linear-gradient(135deg, #E8F4F8, #D0EAF2);
    border: 1px solid #A8D0E6;
    border-radius: 16px;
    padding: 24px 32px;
    margin-bottom: 1.2rem;
    text-align: center;
}
.pred-box .big { font-size: 56px; font-weight: 800; color: #0F2B3D; }
.pred-box .sub { font-size: 13px; color: #2C7DA0; margin-top: 8px; }
.pred-box .tag { font-size: 11px; color: #2C7DA0; font-weight: 600; text-transform: uppercase; margin-bottom: 6px; }

.risk-high { background: #FFEBEE; color: #C62828; padding: 8px; border-radius: 20px; text-align: center; font-weight: 600; }
.risk-medium { background: #FFF8E1; color: #F57C00; padding: 8px; border-radius: 20px; text-align: center; font-weight: 600; }
.risk-low { background: #E8F5E9; color: #2E7D32; padding: 8px; border-radius: 20px; text-align: center; font-weight: 600; }

.stTabs [data-baseweb="tab-list"] { gap: 4px; border-bottom: 1px solid #E2E8F0; }
.stTabs [data-baseweb="tab"] { font-size: 14px; font-weight: 500; padding: 8px 20px; color: #5A7A8C; }
.stTabs [aria-selected="true"] { color: #2C7DA0 !important; border-bottom: 2px solid #2C7DA0 !important; }

[data-testid="stSidebar"] { background: #F5F9FC; border-right: 1px solid #D0E2ED; }
.sb-logo-box {
    background: linear-gradient(135deg, #0F2B3D, #1B4F6E);
    border-radius: 14px;
    padding: 20px 16px;
    text-align: center;
    margin-bottom: 16px;
}
.sb-logo-box .title { color: #fff; font-size: 18px; font-weight: 700; margin: 10px 0 4px; }
.sb-logo-box .sub { color: rgba(255,255,255,0.7); font-size: 11px; }
.sb-section { font-size: 10px; font-weight: 700; color: #2C7DA0; text-transform: uppercase; margin: 16px 0 8px; }
.sb-divider { border-top: 1px solid #D0E2ED; margin: 12px 0; }
.sb-stat { display: flex; justify-content: space-between; padding: 6px 0; font-size: 12px; }
.sb-stat .sk { color: #5A7A8C; }
.sb-stat .sv { color: #0F2B3D; font-weight: 500; }

.filter-note { background: #E0F2FE; border-left: 4px solid #0284C7; padding: 8px 12px; font-size: 11px; color: #0C4A6E; margin-top: 10px; border-radius: 4px; }

.seg-card {
    background: white;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 16px;
    text-align: center;
    transition: all 0.3s ease;
    cursor: pointer;
}
.seg-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.12);
    border-color: #2C7DA0;
}
.seg-card .seg-name { font-size: 16px; font-weight: 700; margin-bottom: 8px; }
.seg-card .seg-count { font-size: 32px; font-weight: 800; }
.seg-card .seg-rev { font-size: 12px; color: #5A7A8C; margin-top: 4px; }

.footer-credit { text-align: center; padding: 20px 0 8px; border-top: 1px solid #D0E2ED; margin-top: 20px; }
.credit-name { font-size: 18px; font-weight: 700; color: #2C7DA0; text-decoration: none; }
.credit-name:hover { color: #1B4F6E; }
.credit-title { font-size: 11px; color: #5A7A8C; margin-top: 5px; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

def kpi_card(val, lbl):
    return f'<div class="kpi-card"><div class="val">{val}</div><div class="lbl">{lbl}</div></div>'

def section_header(title):
    st.markdown(f'<div class="sec-hdr">{title}</div>', unsafe_allow_html=True)

def insight_box(text):
    st.markdown(f'<div class="insight">💡 {text}</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# DATA LOADING
# ═══════════════════════════════════════════════════════════════════════════

@st.cache_data
def load_transaction_data():
    df = pd.read_csv('OnlineRetail_Cleaned.csv')
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    return df

@st.cache_data
def load_rfm_data():
    rfm = pd.read_csv('RFM_dataset.csv')
    return rfm

@st.cache_resource
def load_cltv_models():
    models = {}
    for months in [1, 3, 6]:
        try:
            models[months] = joblib.load(f'cltv_best_model_{months}m.pkl')
        except Exception as e:
            models[months] = None
    return models

@st.cache_resource
def load_churn_model():
    try:
        model = joblib.load('churn_best_model.pkl')
        scaler = joblib.load('churn_scaler.pkl')
        return model, scaler
    except Exception as e:
        return None, None


# Load all data
df_trans = load_transaction_data()
rfm = load_rfm_data()
cltv_models = load_cltv_models()
churn_model, churn_scaler = load_churn_model()

# Sidebar KPIs
total_customers = rfm['CustomerID'].nunique()
total_revenue = rfm['Monetary'].sum()
avg_ltv = rfm['Monetary'].mean()
churn_rate = (rfm['Segment'] == 'Lost').mean() * 100

all_countries = sorted(df_trans['Country'].unique())
all_years = sorted(df_trans['Year'].unique())


# ═══════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════

with st.sidebar:
    if LOGO_B64:
        st.markdown(f"""
        <div class="sb-logo-box">
            <img src="data:image/jpeg;base64,{LOGO_B64}"
                 style="width:100%; max-width:180px; border-radius:12px;
                        margin-bottom:12px; background:#fff; padding:8px;" />
            <div class="title">Customer Intelligence<br>Platform</div>
            <div class="sub">Predict · Analyze · Grow</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="sb-logo-box">
            <div style="font-size:48px">📈</div>
            <div class="title">Customer Intelligence<br>Platform</div>
            <div class="sub">Predict · Analyze · Grow</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="sb-section">📊 Dataset Overview</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background:#fff;border-radius:10px;padding:10px 14px;border:1px solid #D0E2ED;">
        <div class="sb-stat"><span class="sk">👥 Total Customers</span><span class="sv">{total_customers:,}</span></div>
        <div class="sb-stat"><span class="sk">💰 Total Revenue</span><span class="sv">${total_revenue:,.0f}</span></div>
        <div class="sb-stat"><span class="sk">📈 Avg Customer Value</span><span class="sv">${avg_ltv:,.0f}</span></div>
        <div class="sb-stat"><span class="sk">⚠️ At Risk</span><span class="sv">{churn_rate:.1f}%</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="sb-section">🔎 Filters (EDA Tab)</div>', unsafe_allow_html=True)
    
    selected_countries = st.multiselect("Select Countries", options=all_countries, default=[])
    selected_years = st.multiselect("Select Years", options=all_years, default=[])
    
    st.markdown('<div class="filter-note">ℹ️ Select countries/years to filter EDA charts. Leave empty to show all data.</div>', unsafe_allow_html=True)
    
    st.markdown('<hr class="sb-divider">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="footer-credit">
        <a href="https://www.linkedin.com/in/abdallah-ibrahim-mohamed-4556792a5" 
           target="_blank" class="credit-name">
            Abdallah Ibrahim
        </a>
        <div class="credit-title">Data Science & AI Engineer</div>
    </div>
    """, unsafe_allow_html=True)


# Apply filters
if len(selected_countries) > 0 and len(selected_years) > 0:
    filtered_df = df_trans[
        (df_trans['Country'].isin(selected_countries)) & 
        (df_trans['Year'].isin(selected_years))
    ]
elif len(selected_countries) > 0:
    filtered_df = df_trans[df_trans['Country'].isin(selected_countries)]
elif len(selected_years) > 0:
    filtered_df = df_trans[df_trans['Year'].isin(selected_years)]
else:
    filtered_df = df_trans.copy()


# ═══════════════════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="app-header">
    <div>
        <h1>📈 Customer Intelligence Platform</h1>
        <p>AI-Powered Customer Analytics · CLTV Forecasting · Churn Prevention · Smart Segmentation</p>
    </div>
    <span class="header-badge">Predictive Analytics · Business Intelligence</span>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════════════════════════════════════

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Exploratory Data Analysis",
    "🧠 Customer Segmentation",
    "⚠️ Churn Prediction",
    "💰 CLTV Forecasting"
])


# ────────────────────────────────────────────────────────────────────────────
# TAB 1 – EDA
# ────────────────────────────────────────────────────────────────────────────

with tab1:
    if len(filtered_df) == 0:
        st.warning("No data matches the selected filters. Please select countries/years in the sidebar.")
    else:
        st.markdown(
            '<div class="kpi-wrap">'
            + kpi_card(f"{len(filtered_df):,}", "📦 Total Transactions")
            + kpi_card(f"{filtered_df['CustomerID'].nunique():,}", "👥 Unique Customers")
            + kpi_card(f"${filtered_df['TotalPrice'].sum():,.0f}", "💰 Total Revenue")
            + kpi_card(f"${filtered_df['TotalPrice'].mean():.2f}", "🛒 Avg Order Value")
            + kpi_card(f"{filtered_df['Country'].nunique()}", "🌍 Countries")
            + '</div>', unsafe_allow_html=True)
        
        section_header("Revenue & Sales Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            monthly_rev = filtered_df.resample('ME', on='InvoiceDate')['TotalPrice'].sum().reset_index()
            fig1 = px.line(monthly_rev, x='InvoiceDate', y='TotalPrice', 
                           title='Monthly Revenue Trend',
                           labels={'InvoiceDate': 'Date', 'TotalPrice': 'Revenue ($)'},
                           line_shape='spline', markers=True)
            fig1.update_traces(line_color='#2C7DA0', line_width=2.5)
            fig1.update_layout(height=350)
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            country_rev = filtered_df.groupby('Country')['TotalPrice'].sum().sort_values(ascending=False).head(8).reset_index()
            fig2 = px.bar(country_rev, x='TotalPrice', y='Country', orientation='h',
                          title='Top Countries by Revenue', color='TotalPrice', 
                          color_continuous_scale='Tealgrn')
            fig2.update_layout(height=350)
            st.plotly_chart(fig2, use_container_width=True)
        
        section_header("Product & Customer Insights")
        
        col3, col4 = st.columns(2)
        
        with col3:
            top_products = filtered_df.groupby('Description')['TotalPrice'].sum().sort_values(ascending=False).head(10).reset_index()
            fig3 = px.bar(top_products, x='TotalPrice', y='Description', orientation='h',
                          title='Top 10 Products by Revenue', color='TotalPrice', 
                          color_continuous_scale='Tealgrn')
            fig3.update_layout(height=400)
            st.plotly_chart(fig3, use_container_width=True)
        
        with col4:
            dow_rev = filtered_df.groupby('DayName')['TotalPrice'].sum().reset_index()
            dow_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            dow_rev['DayName'] = pd.Categorical(dow_rev['DayName'], categories=dow_order, ordered=True)
            dow_rev = dow_rev.sort_values('DayName')
            fig4 = px.bar(dow_rev, x='DayName', y='TotalPrice', 
                          title='Revenue by Day of Week', color='TotalPrice', 
                          color_continuous_scale='Tealgrn')
            fig4.update_layout(height=400)
            st.plotly_chart(fig4, use_container_width=True)
        
        section_header("Seasonality & Trends")
        
        col5, col6 = st.columns(2)
        
        with col5:
            month_rev = filtered_df.groupby('MonthName')['TotalPrice'].sum().reset_index()
            month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                           'July', 'August', 'September', 'October', 'November', 'December']
            month_rev['MonthName'] = pd.Categorical(month_rev['MonthName'], categories=month_order, ordered=True)
            month_rev = month_rev.sort_values('MonthName')
            fig5 = px.bar(month_rev, x='MonthName', y='TotalPrice',
                          title='Revenue by Month (Seasonality)', color='TotalPrice',
                          color_continuous_scale='Tealgrn')
            fig5.update_layout(height=350, xaxis_tickangle=-45)
            st.plotly_chart(fig5, use_container_width=True)
        
        with col6:
            quarter_rev = filtered_df.groupby('Quarter')['TotalPrice'].sum().reset_index()
            fig6 = px.pie(quarter_rev, values='TotalPrice', names='Quarter',
                          title='Revenue Distribution by Quarter',
                          color_discrete_sequence=px.colors.sequential.Teal)
            fig6.update_layout(height=350)
            st.plotly_chart(fig6, use_container_width=True)
        
        section_header("Top Customers")
        top_customers = filtered_df.groupby('CustomerID')['TotalPrice'].sum().sort_values(ascending=False).head(10).reset_index()
        top_customers['CustomerID'] = top_customers['CustomerID'].astype(str)
        fig7 = px.bar(top_customers, x='TotalPrice', y='CustomerID', orientation='h',
                      title='Top 10 Customers by Revenue', color='TotalPrice',
                      color_continuous_scale='Tealgrn')
        fig7.update_layout(height=350)
        st.plotly_chart(fig7, use_container_width=True)
        
        insight_box("""
        **Key Insights:** Peak revenue in November (holiday season). United Kingdom dominates sales (>80%). 
        Top products include bunting, ornaments, and gift items. Thursday and Tuesday are highest-grossing days.
        """)


# ────────────────────────────────────────────────────────────────────────────
# TAB 2 – CUSTOMER SEGMENTATION 
# ────────────────────────────────────────────────────────────────────────────

with tab2:
    seg_counts = rfm['Segment'].value_counts()
    seg_revenue = rfm.groupby('Segment')['Monetary'].sum()
    
    st.markdown(
        '<div class="kpi-wrap">'
        + kpi_card(f"{len(rfm):,}", "👥 Total Customers")
        + kpi_card(f"{seg_counts.get('VIP', 0):,}", "💎 VIP")
        + kpi_card(f"{seg_counts.get('Regular', 0):,}", "🟢 Regular")
        + kpi_card(f"{seg_counts.get('Potential', 0):,}", "🟡 Potential")
        + kpi_card(f"{seg_counts.get('Lost', 0):,}", "🔴 At Risk")
        + '</div>', unsafe_allow_html=True)
    
    section_header("Segment Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_seg1 = px.pie(values=seg_counts.values, names=seg_counts.index, 
                          title='Customer Distribution by Segment',
                          color_discrete_sequence=px.colors.sequential.Teal_r, 
                          hole=0.4)
        fig_seg1.update_traces(textposition='inside', textinfo='percent+label')
        fig_seg1.update_layout(height=450)
        st.plotly_chart(fig_seg1, use_container_width=True)
    
    with col2:
        seg_rev_df = seg_revenue.reset_index()
        seg_rev_df.columns = ['Segment', 'Revenue']
        fig_seg2 = px.bar(seg_rev_df, x='Segment', y='Revenue', 
                          title='Revenue Contribution by Segment',
                          color='Segment', 
                          color_discrete_sequence=px.colors.sequential.Teal,
                          text='Revenue')
        fig_seg2.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
        fig_seg2.update_layout(height=450)
        st.plotly_chart(fig_seg2, use_container_width=True)
    
    insight_box(f"""
    **📊 Key Business Insight:**  
    • A small group of VIP customers generates a large portion of total revenue  
    • **Strategy:** Prioritize retention and loyalty programs for VIP customers  
    • **At Risk customers** ({seg_counts.get('Lost', 0)} customers) represent lost revenue opportunity - win-back campaigns recommended
    """)
    
    section_header("Segment Profiles")
    
    col3, col4, col5, col6 = st.columns(4)
    
    with col3:
        st.markdown(f"""
        <div class="seg-card">
            <div class="seg-name" style="color:#2E7D32">💎 VIP</div>
            <div class="seg-count">{seg_counts.get('VIP', 0)}</div>
            <div class="seg-rev">Revenue: ${seg_revenue.get('VIP', 0):,.0f}</div>
            <div class="seg-rev">Avg LTV: ${rfm[rfm['Segment']=='VIP']['Monetary'].mean():,.0f}</div>
            <div class="seg-rev">Avg Orders: {rfm[rfm['Segment']=='VIP']['Frequency'].mean():.1f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="seg-card">
            <div class="seg-name" style="color:#1565C0">🟢 Regular</div>
            <div class="seg-count">{seg_counts.get('Regular', 0)}</div>
            <div class="seg-rev">Revenue: ${seg_revenue.get('Regular', 0):,.0f}</div>
            <div class="seg-rev">Avg LTV: ${rfm[rfm['Segment']=='Regular']['Monetary'].mean():,.0f}</div>
            <div class="seg-rev">Avg Orders: {rfm[rfm['Segment']=='Regular']['Frequency'].mean():.1f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class="seg-card">
            <div class="seg-name" style="color:#F57C00">🟡 Potential</div>
            <div class="seg-count">{seg_counts.get('Potential', 0)}</div>
            <div class="seg-rev">Revenue: ${seg_revenue.get('Potential', 0):,.0f}</div>
            <div class="seg-rev">Avg LTV: ${rfm[rfm['Segment']=='Potential']['Monetary'].mean():,.0f}</div>
            <div class="seg-rev">Avg Orders: {rfm[rfm['Segment']=='Potential']['Frequency'].mean():.1f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col6:
        st.markdown(f"""
        <div class="seg-card">
            <div class="seg-name" style="color:#C62828">🔴 At Risk</div>
            <div class="seg-count">{seg_counts.get('Lost', 0)}</div>
            <div class="seg-rev">Revenue: ${seg_revenue.get('Lost', 0):,.0f}</div>
            <div class="seg-rev">Avg LTV: ${rfm[rfm['Segment']=='Lost']['Monetary'].mean():,.0f}</div>
            <div class="seg-rev">Avg Orders: {rfm[rfm['Segment']=='Lost']['Frequency'].mean():.1f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with st.expander("📋 View Customer Segment Data"):
        st.dataframe(rfm.head(20), use_container_width=True)


# ────────────────────────────────────────────────────────────────────────────
# TAB 3 – CHURN PREDICTION
# ────────────────────────────────────────────────────────────────────────────

with tab3:
    st.markdown("""
    <div class="pred-box">
        <div class="tag">CHURN RISK ASSESSMENT</div>
        <div class="big">Predict Customer Churn</div>
        <div class="sub">Enter customer behavior metrics</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        freq_input = st.number_input("📊 Number of Purchases", min_value=0, max_value=100, value=5, step=1, key="churn_freq")
        monetary_input = st.number_input("💰 Total Amount Spent ($)", min_value=0.0, max_value=50000.0, value=500.0, step=50.0, key="churn_monetary")
    
    with col2:
        aov_input = st.number_input("🛒 Average Order Value ($)", min_value=0.0, max_value=5000.0, value=100.0, step=10.0, key="churn_aov")
        lifetime_input = st.number_input("📅 Customer Tenure (days)", min_value=0, max_value=1000, value=180, step=10, key="churn_lifetime")
    
    if st.button("🔮 Predict Churn Risk", use_container_width=True, type="primary"):
        if churn_model is not None and churn_scaler is not None:
            input_df = pd.DataFrame([[
                freq_input, monetary_input, aov_input, lifetime_input
            ]], columns=['Frequency', 'Monetary', 'AvgOrderValue', 'CustomerLifetime'])
            
            input_scaled = churn_scaler.transform(input_df)
            churn_prob = churn_model.predict_proba(input_scaled)[0][1]
            
            section_header("Results")
            
            col_r1, col_r2, col_r3 = st.columns(3)
            
            with col_r1:
                st.metric("Churn Probability", f"{churn_prob:.1%}")
            
            with col_r2:
                if churn_prob > 0.6:
                    st.markdown('<div class="risk-high">⚠️ HIGH RISK</div>', unsafe_allow_html=True)
                elif churn_prob > 0.3:
                    st.markdown('<div class="risk-medium">⚠️ MEDIUM RISK</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="risk-low">✅ LOW RISK</div>', unsafe_allow_html=True)
            
            with col_r3:
                if churn_prob > 0.6:
                    st.markdown("**Recommended Action:** 🚨 Win-back Campaign")
                elif churn_prob > 0.3:
                    st.markdown("**Recommended Action:** 📧 Re-engagement Email")
                else:
                    st.markdown("**Recommended Action:** ✅ Normal Retention")
            
            insight_box(f"**Customer Analysis:** {freq_input} purchases, ${monetary_input:,.2f} total, {lifetime_input} days tenure → **{churn_prob:.1%}** churn risk")
        else:
            st.error("❌ Churn model not loaded. Please check 'churn_best_model.pkl' and 'churn_scaler.pkl'")
    
    with st.expander("ℹ️ About This Model"):
        st.markdown("""
        **How Churn Prediction Works:**
        
        This model analyzes customer behavior to predict who is likely to stop purchasing.
        
        **Input Features:**
        - **Purchase Frequency**: How often the customer buys
        - **Monetary Value**: Total amount spent
        - **Average Order Value**: Average spend per purchase
        - **Customer Tenure**: How long they've been a customer
        
        **Risk Levels:**
        - **Low (<30%)**: Customer is engaged - continue normal retention
        - **Medium (30-60%)**: Early warning signs - send re-engagement offers
        - **High (>60%)**: Customer likely to churn - immediate win-back campaign needed
        """)


# ────────────────────────────────────────────────────────────────────────────
# TAB 4 – CLTV FORECASTING 
# ────────────────────────────────────────────────────────────────────────────

with tab4:
    st.markdown("""
    <div class="pred-box">
        <div class="tag">CLTV FORECASTING</div>
        <div class="big">Predict Customer Lifetime Value</div>
        <div class="sub">Select period and enter customer metrics</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Row 1: Recency, Frequency, Monetary
    col1, col2, col3 = st.columns(3)
    
    with col1:
        cltv_recency = st.number_input("⏰ Days Since Last Purchase", min_value=0, max_value=365, value=30, step=5, key="cltv_recency")
    
    with col2:
        cltv_frequency = st.number_input("📊 Number of Purchases", min_value=0, max_value=100, value=8, step=1, key="cltv_frequency")
    
    with col3:
        cltv_monetary = st.number_input("💰 Total Amount Spent ($)", min_value=0.0, max_value=50000.0, value=600.0, step=50.0, key="cltv_monetary")
    
    # Row 2: Avg Order Value, Avg Items per Order, Customer Tenure
    col4, col5, col6 = st.columns(3)
    
    with col4:
        cltv_avg_order = st.number_input("🛒 Average Order Value ($)", min_value=0.0, max_value=5000.0, value=75.0, step=10.0, key="cltv_avg_order")
    
    with col5:
        cltv_basket_size = st.number_input("🧺 Average Items per Order", min_value=0.0, max_value=50.0, value=5.0, step=0.5, key="cltv_basket_size",
                                           help="Average quantity of items per purchase")
    
    with col6:
        cltv_lifetime = st.number_input("📅 Customer Tenure (days)", min_value=0, max_value=1000, value=180, step=10, key="cltv_lifetime")
    
    # Row 3: Purchase Rate
    col7, col8, col9 = st.columns(3)
    
    with col7:
        cltv_purchase_rate = st.number_input("📈 Purchase Rate", min_value=0.0, max_value=1.0, value=0.0444, step=0.001, format="%.4f", key="cltv_purchase_rate",
                                             help="Number of purchases divided by customer tenure (Frequency / Tenure)")
    
    period = st.select_slider("📅 Prediction Period", options=[1, 3, 6], value=3,
                               format_func=lambda x: f"{x} month{'s' if x > 1 else ''}")
    
    if st.button("💰 Predict CLTV", use_container_width=True, type="primary"):
        model = cltv_models.get(period)
        
        if model is not None:
            input_df = pd.DataFrame([{
                'Recency': cltv_recency,
                'Frequency': cltv_frequency,
                'Monetary': cltv_monetary,
                'AvgOrderValue': cltv_avg_order,
                'CustomerLifetime': cltv_lifetime,
                'PurchaseRate': cltv_purchase_rate,
                'AvgBasketSize': cltv_basket_size
            }])
            
            predicted = model.predict(input_df)[0]
            
            st.markdown(f"""
            <div class="pred-box">
                <div class="tag">PREDICTED CUSTOMER VALUE</div>
                <div class="big">${predicted:,.2f}</div>
                <div class="sub">Expected spend over next {period} month(s)</div>
            </div>
            """, unsafe_allow_html=True)
            
            if predicted > 1000:
                st.success("💎 **High Value Customer** → Loyalty rewards, exclusive offers, premium support")
            elif predicted > 300:
                st.info("🟡 **Medium Value Customer** → Personalized recommendations, bundle offers, email nurture")
            else:
                st.warning("🔴 **Low Value Customer** → Win-back campaigns, discount offers, re-engagement")
        else:
            st.error(f"❌ Model for {period} month(s) not available. Please check model files.")
    
    with st.expander("ℹ️ About CLTV"):
        st.markdown("""
        **What is CLTV (Customer Lifetime Value)?**  
        CLTV predicts the total revenue a customer will generate over a specific future period.
        
        **Why it matters:**
        - Identify your most valuable customers
        - Guide marketing budget allocation
        - Determine maximum acquisition cost
        - Enable personalized customer treatment
        
        **Input Guide:**
        - **Purchase Rate** = Frequency ÷ Tenure (e.g., 8 purchases / 180 days = 0.0444)
        - **Lower Recency** = More recent purchase = Higher predicted value
        - **Higher Frequency** = More loyal customer = Higher predicted value
        - **Average Items per Order** = Higher basket size = Higher predicted value
        """)
