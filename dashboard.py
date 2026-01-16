import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page config
st.set_page_config(
    page_title="Halle-Vilvoorde Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional, sober styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');
    
    /* Global variables */
    :root {
        --primary-color: #1a365d;
        --secondary-color: #2c5282;
        --accent-color: #3182ce;
        --background: #fafafa;
        --surface: #ffffff;
        --text-primary: #1a202c;
        --text-secondary: var(--text-primary);
        --border-light: #e2e8f0;
        --success: #2d6a4f;
        --warning: #d97706;
        --danger: #b91c1c;
    }
    
    /* Main layout */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #fafafa 100%);
        font-family: 'IBM Plex Sans', -apple-system, sans-serif;
        color: var(--text-primary);
    }
    
    /* Headers */
    h1, h2, h3 {
        font-family: 'IBM Plex Sans', sans-serif;
        font-weight: 500;
        letter-spacing: -0.02em;
        color: var(--primary-color);
    }
    
    h1 {
        font-size: 2.5rem;
        font-weight: 300;
        margin-bottom: 0.5rem;
        border-bottom: 2px solid var(--accent-color);
        padding-bottom: 0.75rem;
    }
    
    h2 {
        font-size: 1.75rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
        color: var(--text-primary);
    }
    
    h3 {
        font-size: 1.25rem;
        font-weight: 500;
        color: var(--text-primary);
    }
    
    /* Hide sidebar */
    [data-testid="stSidebar"] {
        display: none;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 1.75rem;
        font-weight: 500;
        color: var(--primary-color);
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.875rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: var(--text-primary);
    }
    
    div[data-testid="metric-container"] {
        background: var(--surface);
        padding: 1.25rem;
        border-radius: 8px;
        border: 1px solid var(--border-light);
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        transition: all 0.2s ease;
    }
    
    div[data-testid="metric-container"]:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        border-color: var(--accent-color);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: transparent;
        border-bottom: 2px solid var(--border-light);
    }
    
    .stTabs [data-baseweb="tab"] {
        font-family: 'IBM Plex Sans', sans-serif;
        font-weight: 500;
        font-size: 0.95rem;
        padding: 0.75rem 1.5rem;
        border-radius: 6px 6px 0 0;
        background: transparent;
        color: var(--text-primary);
        border: none;
        transition: all 0.2s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--surface);
        color: var(--text-primary);
        border-bottom: 3px solid var(--accent-color);
        font-weight: 600;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(49, 130, 206, 0.08);
        color: var(--primary-color);
    }
    
    /* Dataframe styling */
    .stDataFrame {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.875rem;
        background-color: white !important;
    }
    
    /* Dataframe container styling */
    [data-testid="stDataFrame"] {
        background-color: white !important;
    }
    
    [data-testid="stDataFrame"] > div {
        background-color: white !important;
    }
    
    /* Dataframe table styling */
    [data-testid="stDataFrame"] table {
        background-color: white !important;
    }
    
    [data-testid="stDataFrame"] thead {
        background-color: white !important;
    }
    
    [data-testid="stDataFrame"] tbody {
        background-color: white !important;
    }
    
    /* Selectbox (zoekbalk) styling */
    [data-testid="stSelectbox"] {
        background-color: white !important;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid var(--border-light);
    }
    
    [data-baseweb="select"] {
        background-color: white !important;
    }
    
    [data-baseweb="select"] > div {
        background-color: white !important;
        color: var(--text-primary) !important;
    }
    
    div[data-baseweb="select"] > div {
        background-color: white !important;
        color: var(--text-primary) !important;
    }
    
    /* Dropdown menu styling */
    [role="listbox"] {
        background-color: white !important;
    }
    
    [role="option"] {
        background-color: white !important;
        color: var(--text-primary) !important;
    }
    
    [role="option"]:hover {
        background-color: rgba(49, 130, 206, 0.1) !important;
        color: var(--text-primary) !important;
    }
    
    /* Select input text */
    [data-baseweb="select"] input {
        color: var(--text-primary) !important;
    }
    
    [data-baseweb="select"] svg {
        color: var(--text-primary) !important;
    }
    
    /* Buttons */
    .stDownloadButton button {
        background: var(--primary-color);
        color: white;
        font-family: 'IBM Plex Sans', sans-serif;
        font-weight: 500;
        padding: 0.625rem 1.5rem;
        border-radius: 6px;
        border: none;
        transition: all 0.2s ease;
    }
    
    .stDownloadButton button:hover {
        background: var(--secondary-color);
        box-shadow: 0 4px 12px rgba(26, 54, 93, 0.2);
    }
    
    /* Select boxes */
    .stSelectbox label {
        font-weight: 500;
        color: var(--text-primary);
        font-size: 0.95rem;
    }
    
    /* Info boxes */
    .stAlert {
        border-radius: 8px;
        border-left: 4px solid var(--accent-color);
    }
    
    /* Subtle separator */
    hr {
        margin: 2rem 0;
        border: none;
        border-top: 1px solid var(--border-light);
    }
    
    /* Cards/containers */
    div.block-container {
        padding-top: 2rem;
        max-width: 1400px;
    }
    
    /* Custom metric styling for positive/negative values */
    [data-testid="stMetricDelta"] svg {
        display: none;
    }
    
    /* Footer styling */
    footer {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.8rem;
        color: var(--text-primary);
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('nis/halle-vilvoorde.csv')
    return df

# Professional color palette
COLORS = {
    'primary': '#1a365d',
    'secondary': '#2c5282',
    'accent': '#3182ce',
    'success': '#2d6a4f',
    'warning': '#d97706',
    'danger': '#b91c1c',
    'neutral': ['#1a365d', '#2c5282', '#3182ce', '#4299e1', '#63b3ed', '#90cdf4']
}

# Plotly template
def get_plotly_layout():
    return dict(
        font=dict(family='IBM Plex Sans, sans-serif', size=12, color='#1a202c'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=60, r=20, b=50, l=20),
        title=dict(font=dict(size=16, weight=500, color='#1a365d'), x=0.02),
        legend=dict(
            font=dict(size=11, color='#000000', weight=500)
        ),
        xaxis=dict(
            gridcolor='#e2e8f0',
            linecolor='#cbd5e0',
            tickfont=dict(size=11, color='#1a202c'),
            title_font=dict(size=12, color='#1a202c')
        ),
        yaxis=dict(
            gridcolor='#e2e8f0',
            linecolor='#cbd5e0',
            tickfont=dict(size=11, color='#1a202c'),
            title_font=dict(size=12, color='#1a202c')
        ),
        hoverlabel=dict(
            bgcolor='#ffffff',
            font_size=12,
            font_family='IBM Plex Sans',
            font_color='#1a202c',
            bordercolor='#cbd5e0'
        )
    )

df = load_data()

# Title
st.markdown("<h1 style='color: #1a365d;'>Halle-Vilvoorde</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 1.1rem; color: var(--text-primary); margin-top: -0.5rem; margin-bottom: 2rem;'>Analyse gebouwenpark, huishoudens en vergunningen</p>", unsafe_allow_html=True)

# Filter data - use all municipalities
df_filtered = df.copy()

# Remove rows where gemeente name is missing
df_filtered = df_filtered[df_filtered['TX_REFNIS_NL'].notna()]

# Summary metrics
st.markdown("<h2 style='font-size: 1.5rem; margin-top: 1rem; color: #1a202c;'>Kerncijfers</h2>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_huizen = df_filtered['Huizen_totaal_2025'].sum()
    st.metric("Totaal Huizen (2025)", f"{int(total_huizen):,}")

with col2:
    total_flats = df_filtered['Appartementen_2025'].sum()
    st.metric("Totaal Appartementen (2025)", f"{int(total_flats):,}")

with col3:
    nieuwbouw_recent = df_filtered['Woningen_Nieuwbouw_2022sep-2025aug'].sum()
    st.metric("Nieuwbouw 2022-2025 (36m)", f"{int(nieuwbouw_recent):,}")

with col4:
    renovatie_recent = df_filtered['Gebouwen_Renovatie_2022sep-2025aug'].sum()
    st.metric("Renovaties 2022-2025 (36m)", f"{int(renovatie_recent):,}")

# Tabs for different visualizations
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Gebouwenpark", "Huishoudens", "Vergunningen", "Correlaties", "Alle Data"])

with tab1:
    st.markdown("<h2 style='color: #1a202c;'>Gebouwenpark 2025</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top 10 gemeenten met meeste huizen
        top_huizen = df_filtered.nlargest(10, 'Huizen_totaal_2025')[['TX_REFNIS_NL', 'Huizen_totaal_2025']]
        fig1 = px.bar(
            top_huizen,
            x='Huizen_totaal_2025',
            y='TX_REFNIS_NL',
            orientation='h',
            title='Top 10 Gemeenten - Aantal Huizen',
            labels={'Huizen_totaal_2025': 'Aantal Huizen', 'TX_REFNIS_NL': ''},
            color='Huizen_totaal_2025',
            color_continuous_scale=[[0, '#3182ce'], [1, '#1a365d']]
        )
        fig1.update_layout(**get_plotly_layout(), showlegend=False, height=450)
        fig1.update_traces(marker_line_color='#ffffff', marker_line_width=1)
        fig1.update_xaxes(title_font=dict(color='#1a202c'), tickfont=dict(color='#1a202c'))
        fig1.update_yaxes(title_font=dict(color='#1a202c'), tickfont=dict(color='#1a202c'))
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Top 10 gemeenten met meeste appartementen
        top_flats = df_filtered.nlargest(10, 'Appartementen_2025')[['TX_REFNIS_NL', 'Appartementen_2025']]
        fig2 = px.bar(
            top_flats,
            x='Appartementen_2025',
            y='TX_REFNIS_NL',
            orientation='h',
            title='Top 10 Gemeenten - Aantal Appartementen',
            labels={'Appartementen_2025': 'Aantal Appartementen', 'TX_REFNIS_NL': ''},
            color='Appartementen_2025',
            color_continuous_scale=[[0, '#d97706'], [1, '#b91c1c']]
        )
        fig2.update_layout(**get_plotly_layout(), showlegend=False, height=450)
        fig2.update_traces(marker_line_color='#ffffff', marker_line_width=1)
        fig2.update_xaxes(title_font=dict(color='#1a202c'), tickfont=dict(color='#1a202c'))
        fig2.update_yaxes(title_font=dict(color='#1a202c'), tickfont=dict(color='#1a202c'))
        st.plotly_chart(fig2, use_container_width=True)
    
    # Ratio appartementen/huizen
    df_ratio = df_filtered.copy()
    df_ratio['Flats_ratio'] = (df_ratio['Appartementen_2025'] / df_ratio['Huizen_totaal_2025'] * 100).round(2)
    top_ratio = df_ratio.nlargest(15, 'Flats_ratio')[['TX_REFNIS_NL', 'Flats_ratio']]
    
    fig3 = px.bar(
        top_ratio,
        x='TX_REFNIS_NL',
        y='Flats_ratio',
        title='Ratio Appartementen t.o.v. Totaal Huizen (%)',
        labels={'Flats_ratio': 'Percentage (%)', 'TX_REFNIS_NL': ''},
        color='Flats_ratio',
        color_continuous_scale=[[0, '#2d6a4f'], [1, '#14532d']]
    )
    fig3.update_layout(**get_plotly_layout(), showlegend=False, xaxis_tickangle=-45, height=400)
    fig3.update_traces(marker_line_color='#ffffff', marker_line_width=1)
    fig3.update_xaxes(title_font=dict(color='#1a202c'), tickfont=dict(color='#1a202c'))
    fig3.update_yaxes(title_font=dict(color='#1a202c'), tickfont=dict(color='#1a202c'))
    st.plotly_chart(fig3, use_container_width=True)

with tab2:
    st.markdown("<h2 style='color: #1a202c;'>Huishoudens - Voorspelde Toename 2025-2040</h2>", unsafe_allow_html=True)
    
    # Percentage toename per huishoudensgrootte
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<h3 style='color: #1a202c;'>Percentage Toename per Huishoudensgrootte</h3>", unsafe_allow_html=True)
        
        hh_pct_cols = ['hh_1_pct_toename', 'hh_2_pct_toename', 'hh_3_pct_toename', 'hh_4+_pct_toename']
        df_hh_pct = df_filtered[['TX_REFNIS_NL'] + hh_pct_cols].copy()
        
        # Melt voor visualisatie
        df_hh_pct_melt = df_hh_pct.melt(
            id_vars='TX_REFNIS_NL',
            var_name='Huishoudensgrootte',
            value_name='Percentage'
        )
        df_hh_pct_melt['Huishoudensgrootte'] = df_hh_pct_melt['Huishoudensgrootte'].str.replace('hh_', '').str.replace('_pct_toename', ' personen')
        
        fig4 = px.box(
            df_hh_pct_melt,
            x='Huishoudensgrootte',
            y='Percentage',
            title='Distributie Percentage Toename',
            labels={'Percentage': 'Toename (%)', 'Huishoudensgrootte': 'Grootte'},
            color='Huishoudensgrootte',
            color_discrete_sequence=COLORS['neutral']
        )
        fig4.update_layout(**get_plotly_layout(), height=450, legend_title_text="")
        fig4.update_traces(marker_line_color='#ffffff', marker_line_width=1)
        st.plotly_chart(fig4, use_container_width=True)
    
    with col2:
        st.markdown("<h3 style='color: #1a202c;'>Absolute Toename per Huishoudensgrootte</h3>", unsafe_allow_html=True)
        
        hh_abs_cols = ['hh_1_abs_toename', 'hh_2_abs_toename', 'hh_3_abs_toename', 'hh_4+_abs_toename']
        df_hh_abs = df_filtered[['TX_REFNIS_NL'] + hh_abs_cols].copy()
        
        # Totaal absolute toename per gemeente
        df_hh_abs['Totaal_toename'] = df_hh_abs[hh_abs_cols].sum(axis=1)
        top_toename = df_hh_abs.nlargest(10, 'Totaal_toename')[['TX_REFNIS_NL', 'Totaal_toename']]
        
        fig5 = px.bar(
            top_toename,
            x='Totaal_toename',
            y='TX_REFNIS_NL',
            orientation='h',
            title='Top 10 Gemeenten - Totale Toename Huishoudens',
            labels={'Totaal_toename': 'Absolute Toename', 'TX_REFNIS_NL': 'Gemeente'},
            color='Totaal_toename',
            color_continuous_scale=[[0, '#3182ce'], [1, '#1a365d']]
        )
        fig5.update_layout(**get_plotly_layout(), showlegend=False, height=450)
        fig5.update_traces(marker_line_color='#ffffff', marker_line_width=1)
        st.plotly_chart(fig5, use_container_width=True)
    
    # Gedetailleerde breakdown per gemeente (top 10)
    st.markdown("<h3 style='color: #1a202c;'>Gedetailleerde Breakdown - Top 10 Gemeenten</h3>", unsafe_allow_html=True)
    
    df_breakdown = df_filtered.copy()
    df_breakdown['Totaal_toename'] = df_breakdown[hh_abs_cols].sum(axis=1)
    top_10_gemeenten = df_breakdown.nlargest(10, 'Totaal_toename')['TX_REFNIS_NL'].tolist()
    
    df_top10 = df_filtered[df_filtered['TX_REFNIS_NL'].isin(top_10_gemeenten)][['TX_REFNIS_NL'] + hh_abs_cols].copy()
    df_top10_melt = df_top10.melt(
        id_vars='TX_REFNIS_NL',
        var_name='Grootte',
        value_name='Toename'
    )
    df_top10_melt['Grootte'] = df_top10_melt['Grootte'].str.replace('hh_', '').str.replace('_abs_toename', ' pers')
    
    fig6 = px.bar(
        df_top10_melt,
        x='TX_REFNIS_NL',
        y='Toename',
        color='Grootte',
        title='Absolute Toename per Huishoudensgrootte (Top 10 Gemeenten)',
        labels={'Toename': 'Absolute Toename', 'TX_REFNIS_NL': 'Gemeente'},
        barmode='group',
        color_discrete_sequence=COLORS['neutral']
    )
    fig6.update_layout(**get_plotly_layout(), xaxis_tickangle=-45, height=450, legend_title_text="")
    fig6.update_traces(marker_line_color='#ffffff', marker_line_width=1)
    st.plotly_chart(fig6, use_container_width=True)

with tab3:
    st.markdown("<h2 style='color: #1a202c;'>Bouwvergunningen - 36 Maanden Vergelijking</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<h3 style='color: #1a202c;'>Nieuwbouw Woningen</h3>", unsafe_allow_html=True)
        
        # Vergelijking 36 maanden voor nieuwbouw
        df_nieuwbouw = df_filtered[['TX_REFNIS_NL', 
                                    'Woningen_Nieuwbouw_2019sep-2022aug',
                                    'Woningen_Nieuwbouw_2022sep-2025aug',
                                    'Woningen_Nieuwbouw_pct_verschil_36m']].dropna()
        
        top_nieuwbouw = df_nieuwbouw.nlargest(10, 'Woningen_Nieuwbouw_2022sep-2025aug')
        
        fig7 = go.Figure()
        fig7.add_trace(go.Bar(
            name='2019-2022',
            x=top_nieuwbouw['TX_REFNIS_NL'],
            y=top_nieuwbouw['Woningen_Nieuwbouw_2019sep-2022aug'],
            marker_color='#63b3ed',
            marker_line_color='#ffffff',
            marker_line_width=1
        ))
        fig7.add_trace(go.Bar(
            name='2022-2025',
            x=top_nieuwbouw['TX_REFNIS_NL'],
            y=top_nieuwbouw['Woningen_Nieuwbouw_2022sep-2025aug'],
            marker_color='#1a365d',
            marker_line_color='#ffffff',
            marker_line_width=1
        ))
        layout = get_plotly_layout()
        layout.update(
            title='Top 10 - Nieuwbouw Woningen (36 maanden)',
            xaxis_title='Gemeente',
            yaxis_title='Aantal Woningen',
            barmode='group',
            xaxis_tickangle=-45,
            height=450
        )
        fig7.update_layout(layout)
        st.plotly_chart(fig7, use_container_width=True)
        
        # Percentage verschil nieuwbouw
        fig9 = px.bar(
            df_nieuwbouw.sort_values('Woningen_Nieuwbouw_pct_verschil_36m'),
            x='TX_REFNIS_NL',
            y='Woningen_Nieuwbouw_pct_verschil_36m',
            title='Percentage Verschil Nieuwbouw Woningen',
            labels={'Woningen_Nieuwbouw_pct_verschil_36m': 'Verschil (%)', 'TX_REFNIS_NL': 'Gemeente'},
            color='Woningen_Nieuwbouw_pct_verschil_36m',
            color_continuous_scale=['#b91c1c', '#d97706', '#2d6a4f'],
            color_continuous_midpoint=0
        )
        fig9.update_layout(**get_plotly_layout(), xaxis_tickangle=-45, showlegend=False, height=450)
        fig9.update_traces(marker_line_color='#ffffff', marker_line_width=1)
        st.plotly_chart(fig9, use_container_width=True)
    
    with col2:
        st.markdown("<h3 style='color: #1a202c;'>Renovatie Gebouwen</h3>", unsafe_allow_html=True)
        
        # Vergelijking 36 maanden voor renovatie
        df_renovatie = df_filtered[['TX_REFNIS_NL', 
                                    'Gebouwen_Renovatie_2019sep-2022aug',
                                    'Gebouwen_Renovatie_2022sep-2025aug',
                                    'Gebouwen_Renovatie_pct_verschil_36m']].dropna()
        
        top_renovatie = df_renovatie.nlargest(10, 'Gebouwen_Renovatie_2022sep-2025aug')
        
        fig8 = go.Figure()
        fig8.add_trace(go.Bar(
            name='2019-2022',
            x=top_renovatie['TX_REFNIS_NL'],
            y=top_renovatie['Gebouwen_Renovatie_2019sep-2022aug'],
            marker_color='#f59e0b',
            marker_line_color='#ffffff',
            marker_line_width=1
        ))
        fig8.add_trace(go.Bar(
            name='2022-2025',
            x=top_renovatie['TX_REFNIS_NL'],
            y=top_renovatie['Gebouwen_Renovatie_2022sep-2025aug'],
            marker_color='#d97706',
            marker_line_color='#ffffff',
            marker_line_width=1
        ))
        layout = get_plotly_layout()
        layout.update(
            title='Top 10 - Renovatie Gebouwen (36 maanden)',
            xaxis_title='Gemeente',
            yaxis_title='Aantal Gebouwen',
            barmode='group',
            xaxis_tickangle=-45,
            height=450
        )
        fig8.update_layout(layout)
        st.plotly_chart(fig8, use_container_width=True)
        
        # Percentage verschil renovatie
        fig10 = px.bar(
            df_renovatie.sort_values('Gebouwen_Renovatie_pct_verschil_36m'),
            x='TX_REFNIS_NL',
            y='Gebouwen_Renovatie_pct_verschil_36m',
            title='Percentage Verschil Renovatie Gebouwen',
            labels={'Gebouwen_Renovatie_pct_verschil_36m': 'Verschil (%)', 'TX_REFNIS_NL': 'Gemeente'},
            color='Gebouwen_Renovatie_pct_verschil_36m',
            color_continuous_scale=['#b91c1c', '#d97706', '#2d6a4f'],
            color_continuous_midpoint=0
        )
        fig10.update_layout(**get_plotly_layout(), xaxis_tickangle=-45, showlegend=False, height=450)
        fig10.update_traces(marker_line_color='#ffffff', marker_line_width=1)
        st.plotly_chart(fig10, use_container_width=True)

with tab4:
    st.markdown("<h2 style='color: #1a202c;'>Correlaties en Trends</h2>", unsafe_allow_html=True)
    
    # Scatter plots voor correlaties
    col1, col2 = st.columns(2)
    
    with col1:
        # Huishoudens toename vs nieuwbouw
        df_scatter1 = df_filtered.copy()
        df_scatter1['Totaal_hh_toename'] = df_scatter1[hh_abs_cols].sum(axis=1)
        df_scatter1 = df_scatter1.dropna(subset=['Totaal_hh_toename', 'Woningen_Nieuwbouw_2022sep-2025aug'])
        
        fig11 = px.scatter(
            df_scatter1,
            x='Totaal_hh_toename',
            y='Woningen_Nieuwbouw_2022sep-2025aug',
            text='TX_REFNIS_NL',
            title='Voorspelde Huishoudensgroei (2025-2040) vs Recente Nieuwbouw (2022-2025)',
            labels={
                'Totaal_hh_toename': 'Totale Toename Huishoudens (voorspelling 2025-2040)',
                'Woningen_Nieuwbouw_2022sep-2025aug': 'Nieuwbouw Woningen (sept 2022 - aug 2025)'
            },
            size='Huizen_totaal_2025',
            color='Totaal_hh_toename',
            color_continuous_scale=[[0, '#3182ce'], [1, '#1a365d']]
        )
        fig11.update_layout(**get_plotly_layout(), height=450, coloraxis_colorbar_title_text="")
        fig11.update_traces(textposition='top center', textfont_size=8, marker_line_color='#ffffff', marker_line_width=1)
        st.plotly_chart(fig11, use_container_width=True)
    
    with col2:
        # Appartementen ratio vs huishoudens 1-2 personen
        df_scatter2 = df_filtered.copy()
        df_scatter2['Flats_ratio'] = (df_scatter2['Appartementen_2025'] / df_scatter2['Huizen_totaal_2025'] * 100)
        df_scatter2['Klein_hh_pct'] = df_scatter2['hh_1_pct_toename'] + df_scatter2['hh_2_pct_toename']
        df_scatter2 = df_scatter2.dropna(subset=['Flats_ratio', 'Klein_hh_pct'])
        
        fig12 = px.scatter(
            df_scatter2,
            x='Flats_ratio',
            y='Klein_hh_pct',
            text='TX_REFNIS_NL',
            title='Huidige Appartementen Ratio (2025) vs Voorspelde Groei Kleine Huishoudens (2025-2040)',
            labels={
                'Flats_ratio': 'Ratio Appartementen (% van totaal, 2025)',
                'Klein_hh_pct': 'Toename 1+2 Persoons HH (% voorspelling 2025-2040)'
            },
            color='Huizen_totaal_2025',
            color_continuous_scale=[[0, '#d97706'], [1, '#b91c1c']]
        )
        fig12.update_layout(**get_plotly_layout(), height=450, coloraxis_colorbar_title_text="")
        fig12.update_traces(textposition='top center', textfont_size=8, marker_line_color='#ffffff', marker_line_width=1)
        st.plotly_chart(fig12, use_container_width=True)
    
    # Correlatie tussen nieuwbouw en renovatie
    col1, col2 = st.columns(2)
    
    with col1:
        df_scatter3 = df_filtered.dropna(subset=['Woningen_Nieuwbouw_2022sep-2025aug', 'Gebouwen_Renovatie_2022sep-2025aug'])
        
        fig13 = px.scatter(
            df_scatter3,
            x='Woningen_Nieuwbouw_2022sep-2025aug',
            y='Gebouwen_Renovatie_2022sep-2025aug',
            text='TX_REFNIS_NL',
            title='Nieuwbouw vs Renovatie - Bouwactiviteit Laatste 3 Jaar (sept 2022 - aug 2025)',
            labels={
                'Woningen_Nieuwbouw_2022sep-2025aug': 'Nieuwbouw Woningen (sept 2022 - aug 2025)',
                'Gebouwen_Renovatie_2022sep-2025aug': 'Renovatie Gebouwen (sept 2022 - aug 2025)'
            },
            color='Huizen_totaal_2025',
            color_continuous_scale=[[0, '#2d6a4f'], [1, '#14532d']]
        )
        fig13.update_layout(**get_plotly_layout(), height=450, coloraxis_colorbar_title_text="")
        fig13.update_traces(textposition='top center', textfont_size=8, marker_line_color='#ffffff', marker_line_width=1)
        st.plotly_chart(fig13, use_container_width=True)
    
    with col2:
        # Huizen totaal vs grootgezinnen (3 en 4+ personen)
        df_scatter4 = df_filtered.copy()
        df_scatter4['Groot_hh_abs'] = df_scatter4['hh_3_abs_toename'] + df_scatter4['hh_4+_abs_toename']
        df_scatter4 = df_scatter4.dropna(subset=['Huizen_totaal_2025', 'Groot_hh_abs'])
        
        fig14 = px.scatter(
            df_scatter4,
            x='Huizen_totaal_2025',
            y='Groot_hh_abs',
            text='TX_REFNIS_NL',
            title='Huidige Woningvoorraad (2025) vs Voorspelde Groei Grote Huishoudens (2025-2040)',
            labels={
                'Huizen_totaal_2025': 'Totaal Huizen (stand 2025)',
                'Groot_hh_abs': 'Toename 3-4+ Persoons HH (voorspelling 2025-2040)'
            },
            color='Appartementen_2025',
            color_continuous_scale=[[0, '#f59e0b'], [1, '#d97706']]
        )
        fig14.update_layout(**get_plotly_layout(), height=450, coloraxis_colorbar_title_text="")
        fig14.update_traces(textposition='top center', textfont_size=8, marker_line_color='#ffffff', marker_line_width=1)
        st.plotly_chart(fig14, use_container_width=True)

with tab5:
    st.markdown("<h2 style='color: #1a202c;'>Volledige Dataset</h2>", unsafe_allow_html=True)
    
    # Sectie voor het kiezen van specifieke gemeenten
    st.markdown("<h3 style='color: #1a202c;'>Selecteer Gemeente voor Details</h3>", unsafe_allow_html=True)
    selected_gemeente = st.selectbox(
        "Kies een gemeente:",
        options=['Alle gemeenten'] + sorted(df_filtered['TX_REFNIS_NL'].unique().tolist())
    )
    
    if selected_gemeente != 'Alle gemeenten':
        gemeente_data = df_filtered[df_filtered['TX_REFNIS_NL'] == selected_gemeente].iloc[0]
        
        # Toon alle variabelen voor de geselecteerde gemeente
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### Gebouwenpark 2025")
            st.metric("Totaal Huizen", f"{int(gemeente_data['Huizen_totaal_2025']):,}")
            st.metric("Appartementen", f"{int(gemeente_data['Appartementen_2025']):,}")
            st.metric("Appartementen Ratio", f"{(gemeente_data['Appartementen_2025']/gemeente_data['Huizen_totaal_2025']*100):.2f}%")
        
        with col2:
            st.markdown("### Huishoudens Toename 2025-2040")
            st.markdown("**Percentage Toename:**")
            st.write(f"• 1 persoon: {gemeente_data['hh_1_pct_toename']:.2f}%")
            st.write(f"• 2 personen: {gemeente_data['hh_2_pct_toename']:.2f}%")
            st.write(f"• 3 personen: {gemeente_data['hh_3_pct_toename']:.2f}%")
            st.write(f"• 4+ personen: {gemeente_data['hh_4+_pct_toename']:.2f}%")
            
            st.markdown("**Absolute Toename:**")
            st.write(f"• 1 persoon: {int(gemeente_data['hh_1_abs_toename']):,}")
            st.write(f"• 2 personen: {int(gemeente_data['hh_2_abs_toename']):,}")
            st.write(f"• 3 personen: {int(gemeente_data['hh_3_abs_toename']):,}")
            st.write(f"• 4+ personen: {int(gemeente_data['hh_4+_abs_toename']):,}")
            
            totaal_toename = (gemeente_data['hh_1_abs_toename'] + gemeente_data['hh_2_abs_toename'] + 
                            gemeente_data['hh_3_abs_toename'] + gemeente_data['hh_4+_abs_toename'])
            st.metric("Totale Toename", f"{int(totaal_toename):,}")
        
        with col3:
            st.markdown("### Vergunningen (36 maanden)")
            
            if pd.notna(gemeente_data['Woningen_Nieuwbouw_2019sep-2022aug']):
                st.markdown("**Nieuwbouw Woningen:**")
                st.write(f"• 2019-2022: {int(gemeente_data['Woningen_Nieuwbouw_2019sep-2022aug']):,}")
                st.write(f"• 2022-2025: {int(gemeente_data['Woningen_Nieuwbouw_2022sep-2025aug']):,}")
                st.metric("Verschil", f"{gemeente_data['Woningen_Nieuwbouw_pct_verschil_36m']:.2f}%")
                
                st.markdown("**Renovatie Gebouwen:**")
                st.write(f"• 2019-2022: {int(gemeente_data['Gebouwen_Renovatie_2019sep-2022aug']):,}")
                st.write(f"• 2022-2025: {int(gemeente_data['Gebouwen_Renovatie_2022sep-2025aug']):,}")
                st.metric("Verschil", f"{gemeente_data['Gebouwen_Renovatie_pct_verschil_36m']:.2f}%")
            else:
                st.info("Geen vergunningendata beschikbaar voor deze gemeente")
        
        # Visualisatie voor huishoudens van de gemeente
        st.markdown("---")
        st.markdown(f"<h3 style='color: #1a202c;'>Huishoudens Breakdown - {selected_gemeente}</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Percentage toename
            hh_pct_data = pd.DataFrame({
                'Grootte': ['1 persoon', '2 personen', '3 personen', '4+ personen'],
                'Percentage': [
                    gemeente_data['hh_1_pct_toename'],
                    gemeente_data['hh_2_pct_toename'],
                    gemeente_data['hh_3_pct_toename'],
                    gemeente_data['hh_4+_pct_toename']
                ]
            })
            
            fig_pct = px.bar(
                hh_pct_data,
                x='Grootte',
                y='Percentage',
                title='Percentage Toename per Huishoudensgrootte',
                color='Percentage',
                color_continuous_scale=[[0, '#3182ce'], [1, '#1a365d']]
            )
            fig_pct.update_layout(**get_plotly_layout(), showlegend=False, height=400)
            fig_pct.update_traces(marker_line_color='#ffffff', marker_line_width=1)
            st.plotly_chart(fig_pct, use_container_width=True)
        
        with col2:
            # Absolute toename
            hh_abs_data = pd.DataFrame({
                'Grootte': ['1 persoon', '2 personen', '3 personen', '4+ personen'],
                'Toename': [
                    gemeente_data['hh_1_abs_toename'],
                    gemeente_data['hh_2_abs_toename'],
                    gemeente_data['hh_3_abs_toename'],
                    gemeente_data['hh_4+_abs_toename']
                ]
            })
            
            fig_abs = px.bar(
                hh_abs_data,
                x='Grootte',
                y='Toename',
                title='Absolute Toename per Huishoudensgrootte',
                color='Toename',
                color_continuous_scale=[[0, '#2d6a4f'], [1, '#14532d']]
            )
            fig_abs.update_layout(**get_plotly_layout(), showlegend=False, height=400)
            fig_abs.update_traces(marker_line_color='#ffffff', marker_line_width=1)
            st.plotly_chart(fig_abs, use_container_width=True)
        
        # Vergunningen visualisatie
        if pd.notna(gemeente_data['Woningen_Nieuwbouw_2019sep-2022aug']):
            st.markdown("---")
            st.markdown(f"<h3 style='color: #1a202c;'>Vergunningen Evolutie - {selected_gemeente}</h3>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                nieuwbouw_data = pd.DataFrame({
                    'Periode': ['2019-2022', '2022-2025'],
                    'Aantal': [
                        gemeente_data['Woningen_Nieuwbouw_2019sep-2022aug'],
                        gemeente_data['Woningen_Nieuwbouw_2022sep-2025aug']
                    ]
                })
                
                fig_nieuwbouw = px.bar(
                    nieuwbouw_data,
                    x='Periode',
                    y='Aantal',
                    title='Nieuwbouw Woningen',
                    color='Aantal',
                    color_continuous_scale=[[0, '#f59e0b'], [1, '#d97706']]
                )
                fig_nieuwbouw.update_layout(**get_plotly_layout(), showlegend=False, height=400)
                fig_nieuwbouw.update_traces(marker_line_color='#ffffff', marker_line_width=1)
                st.plotly_chart(fig_nieuwbouw, use_container_width=True)
            
            with col2:
                renovatie_data = pd.DataFrame({
                    'Periode': ['2019-2022', '2022-2025'],
                    'Aantal': [
                        gemeente_data['Gebouwen_Renovatie_2019sep-2022aug'],
                        gemeente_data['Gebouwen_Renovatie_2022sep-2025aug']
                    ]
                })
                
                fig_renovatie = px.bar(
                    renovatie_data,
                    x='Periode',
                    y='Aantal',
                    title='Renovatie Gebouwen',
                    color='Aantal',
                    color_continuous_scale=[[0, '#d97706'], [1, '#b91c1c']]
                )
                fig_renovatie.update_layout(**get_plotly_layout(), showlegend=False, height=400)
                fig_renovatie.update_traces(marker_line_color='#ffffff', marker_line_width=1)
                st.plotly_chart(fig_renovatie, use_container_width=True)
    
    # Volledige data tabel
    st.markdown("---")
    st.markdown("<h3 style='color: #1a202c;'>Volledige Data Tabel - Alle Variabelen</h3>", unsafe_allow_html=True)
    
    # Maak een mooie weergave van alle kolommen
    display_df = df_filtered.copy()
    
    # Hernoem kolommen voor betere leesbaarheid
    column_names = {
        'TX_REFNIS_NL': 'Gemeente',
        'Huizen_totaal_2025': 'Huizen 2025',
        'Appartementen_2025': 'Appartementen 2025',
        'hh_1_pct_toename': 'HH 1p %',
        'hh_2_pct_toename': 'HH 2p %',
        'hh_3_pct_toename': 'HH 3p %',
        'hh_4+_pct_toename': 'HH 4+p %',
        'hh_1_abs_toename': 'HH 1p abs',
        'hh_2_abs_toename': 'HH 2p abs',
        'hh_3_abs_toename': 'HH 3p abs',
        'hh_4+_abs_toename': 'HH 4+p abs',
        'Woningen_Nieuwbouw_2019sep-2022aug': 'Nieuwbouw 2019-2022',
        'Woningen_Nieuwbouw_2022sep-2025aug': 'Nieuwbouw 2022-2025',
        'Woningen_Nieuwbouw_pct_verschil_36m': 'Nieuwbouw %',
        'Gebouwen_Renovatie_2019sep-2022aug': 'Renovatie 2019-2022',
        'Gebouwen_Renovatie_2022sep-2025aug': 'Renovatie 2022-2025',
        'Gebouwen_Renovatie_pct_verschil_36m': 'Renovatie %'
    }
    
    # Selecteer en hernoem kolommen
    cols_to_show = ['TX_REFNIS_NL', 'Huizen_totaal_2025', 'Appartementen_2025',
                    'hh_1_pct_toename', 'hh_2_pct_toename', 'hh_3_pct_toename', 'hh_4+_pct_toename',
                    'hh_1_abs_toename', 'hh_2_abs_toename', 'hh_3_abs_toename', 'hh_4+_abs_toename',
                    'Woningen_Nieuwbouw_2019sep-2022aug', 'Woningen_Nieuwbouw_2022sep-2025aug', 'Woningen_Nieuwbouw_pct_verschil_36m',
                    'Gebouwen_Renovatie_2019sep-2022aug', 'Gebouwen_Renovatie_2022sep-2025aug', 'Gebouwen_Renovatie_pct_verschil_36m']
    
    display_df = display_df[cols_to_show].rename(columns=column_names)
    
    # Sorteer op totaal huizen
    display_df = display_df.sort_values('Huizen 2025', ascending=False)
    
    # Toon dataframe met styling in witte container
    st.markdown("""
    <style>
    [data-testid="stDataFrame"] {
        background-color: white !important;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=600
    )
    
    # Download optie
    st.markdown("---")
    csv = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Volledige Dataset als CSV",
        data=csv,
        file_name='halle-vilvoorde-data.csv',
        mime='text/csv'
    )
    
    # Statistieken
    st.markdown("---")
    st.markdown("<h3 style='color: #1a202c;'>Dataset Statistieken</h3>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Aantal Gemeenten", len(df_filtered))
    
    with col2:
        avg_huizen = df_filtered['Huizen_totaal_2025'].mean()
        st.metric("Gem. Huizen per Gemeente", f"{int(avg_huizen):,}")
    
    with col3:
        total_hh_toename = df_filtered[['hh_1_abs_toename', 'hh_2_abs_toename', 
                                        'hh_3_abs_toename', 'hh_4+_abs_toename']].sum().sum()
        st.metric("Totale HH Toename 2025-2040", f"{int(total_hh_toename):,}")
    
    with col4:
        avg_nieuwbouw_verschil = df_filtered['Woningen_Nieuwbouw_pct_verschil_36m'].mean()
        st.metric("Gem. Nieuwbouw Verschil", f"{avg_nieuwbouw_verschil:.2f}%")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #718096; font-size: 0.875rem; padding: 1.5rem 0;'>
    <p style='margin: 0;'>Halle-Vilvoorde Dashboard • Data bijgewerkt: januari 2026</p>
    <p style='margin: 0.4rem 0 0;'>Bronvermeldingen: Gebouwenpark: Statbel, Huishoudens: Statistiek Vlaanderen, Vergunningen: Statbel</p>
</div>
""", unsafe_allow_html=True)
