import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Russian Conscription Quotas", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    * { font-family: 'Inter', sans-serif !important; }
    .stApp { background-color: #000000; color: #ffffff; }
    h1, h2, h3, h4 { color: #ffffff !important; }
    .stMarkdown, .stMarkdown p, .stMarkdown li { color: #ffffff !important; }
    .block-container { padding: 0rem 2rem !important; margin-top: 0 !important; }
[data-testid="stAppViewContainer"] { padding-top: 0 !important; }
[data-testid="stHeader"] { display: none !important; }
    .stButton > button {
        background-color: #000000 !important;
        color: #aaaaaa !important;
        border: 0.5px solid #333333 !important;
        border-radius: 8px !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        padding: 6px 14px !important;
    }
    .stButton > button:hover {
        border-color: #666666 !important;
        color: #ffffff !important;
    }
    .info-box {
        background-color: #111111;
        border: 0.5px solid #333333;
        border-radius: 8px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1rem;
    }
    .info-box p {
        color: #ffffff !important;
        font-size: 13px !important;
        line-height: 1.7 !important;
        margin: 0.3rem 0 !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("Military_emigration_and_conscription_-_Conscription.csv")
    df.columns = ["year", "spring", "autumn", "total"]
    for col in ["spring", "autumn", "total"]:
        df[col] = pd.to_numeric(
            df[col].astype(str).str.replace(".", "", regex=False).str.replace(",", "", regex=False),
            errors="coerce"
        )
    df.loc[df["year"] == 2026, "spring"] = 261000
    df.loc[df["year"] == 2026, "autumn"] = 0
    df.loc[df["year"] == 2026, "total"]  = 261000
    df["year_str"] = df["year"].astype(str)
    return df

df = load_data()

# ── Title ──────────────────────────────────────────────────────────────────
st.markdown(
    "<h2 style='font-size:22px;font-weight:600;color:#ffffff;margin:0 0 4px;'>"
    "How many Russian men were conscripted each year?</h2>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='color:#888888;font-size:12px;margin:0 0 12px;'>"
    "Annual conscription quotas in Russia by draft cycle, 2008–2026</p>",
    unsafe_allow_html=True,
)

if "show_conscription_info" not in st.session_state:
    st.session_state.show_conscription_info = False

if st.button("About the data", key="conscription_info_btn"):
    st.session_state.show_conscription_info = not st.session_state.show_conscription_info

if st.session_state.show_conscription_info:
    st.markdown("""
    <div class="info-box">
        <p><strong>What are we looking at?</strong></p>
        <p>This chart shows Russia's annual military conscription quotas — the number of men called up for mandatory military service each year. Russia conducts two conscription cycles per year: a spring draft (April–July) and an autumn draft (October–December).</p>
        <br>
        <p><strong>Data source</strong></p>
        <p>Data was collected from official Russian presidential decrees on conscription, published annually. Each decree specifies the number of citizens to be called up for that cycle.</p>
        <br>
        <p><strong>Note on 2026</strong></p>
        <p>The 2026 figure reflects Russia's first year-round conscription system, signed into law in November 2025 and effective January 2026. The total planned quota is 261,000 — shown as a single bar since the seasonal split no longer applies.</p>
    </div>
    """, unsafe_allow_html=True)

years  = df["year_str"].tolist()
spring = df["spring"].tolist()
autumn = df["autumn"].tolist()
total  = df["total"].tolist()

fig = go.Figure()

# Spring draft — all years except 2026
fig.add_trace(go.Bar(
    x=[y for y in years if y != "2026"],
    y=[spring[i] for i, y in enumerate(years) if y != "2026"],
    name="Spring draft",
    marker_color="rgba(0,87,231,0.6)",
    hovertemplate="<b>%{x}</b><br>Spring draft: %{y:,.0f}<extra></extra>",
))

# Autumn draft — all years except 2026
fig.add_trace(go.Bar(
    x=[y for y in years if y != "2026"],
    y=[autumn[i] for i, y in enumerate(years) if y != "2026"],
    name="Autumn draft",
    marker_color="rgba(0,87,231,0.35)",
    hovertemplate="<b>%{x}</b><br>Autumn draft: %{y:,.0f}<extra></extra>",
))

# 2026 — total draft as single bar
fig.add_trace(go.Bar(
    x=["2026"],
    y=[261000],
    name="Total draft",
    marker_color="rgba(0,87,231,0.5)",
    hovertemplate="<b>2026</b><br>Total draft: 261,000<extra></extra>",
))

# Total line
fig.add_trace(go.Scatter(
    x=years, y=total,
    name="Total",
    mode="lines+markers",
    line=dict(color="#0057E7", width=2.5),
    marker=dict(size=6, color="#0057E7"),
    hovertemplate="<b>%{x}</b><br>Total: %{y:,.0f}<extra></extra>",
))

# Full-scale invasion line in red
fig.add_shape(
    type="line",
    x0="2022", x1="2022",
    y0=0, y1=580000,
    line=dict(color="#E8000D", width=1.5, dash="dot"),
)
fig.add_annotation(
    x="2022", y=590000,
    text="Full-scale invasion",
    showarrow=False,
    yanchor="bottom",
    xanchor="left",
    xshift=6,
    font=dict(size=10, color="#E8000D", family="Inter"),
    bgcolor="rgba(0,0,0,0)",
)

fig.update_layout(
    barmode="stack",
    paper_bgcolor="#000000",
    plot_bgcolor="#000000",
    font=dict(family="Inter", size=12, color="#ffffff"),
    xaxis=dict(
        title=dict(text="Year", font=dict(color="#ffffff", family="Inter", size=12)),
        tickfont=dict(color="#ffffff", family="Inter", size=11),
        showgrid=False,
        tickangle=-45,
        showline=False,
        categoryorder="array",
        categoryarray=years,
    ),
    yaxis=dict(
        title=dict(text="Number of conscripts", font=dict(color="#ffffff", family="Inter", size=12)),
        tickfont=dict(color="#ffffff", family="Inter", size=11),
        gridcolor="#222222",
        showline=False,
        tickformat=",d",
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom", y=-0.28,
        xanchor="center", x=0.5,
        font=dict(size=12, color="#ffffff", family="Inter"),
        bgcolor="rgba(0,0,0,0)",
    ),
    hoverlabel=dict(
        align="left",
        bgcolor="#222222",
        font=dict(color="#ffffff", size=12, family="Inter"),
    ),
    hovermode="x unified",
    margin=dict(t=10, b=100, l=70, r=20),
    height=460,
)

st.plotly_chart(fig, width="stretch")

st.markdown(
    "<p style='font-size:10px;color:#444444;margin:4px 0;'>"
    "Source: Official Russian presidential conscription decrees · "
    "Spring draft: April–July · Autumn draft: October–December · "
    "2026: Year-round conscription system</p>",
    unsafe_allow_html=True,
)
