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
    [data-testid="stExpander"] {
        border: 0.5px solid #333333 !important;
        border-radius: 8px !important;
        background-color: #000000 !important;
    }
    [data-testid="stExpander"] summary {
        color: #ffffff !important;
        background-color: #000000 !important;
        list-style: none !important;
    }
    [data-testid="stExpander"] summary::-webkit-details-marker { display: none !important; }
    [data-testid="stExpander"] summary svg { display: none !important; }
    [data-testid="stExpander"] summary p {
        font-size: 14px !important;
        font-weight: 500 !important;
        color: #aaaaaa !important;
    }
    [data-testid="stExpanderDetails"] {
        background-color: #111111 !important;
        color: #ffffff !important;
    }
    [data-testid="stExpanderDetails"] p,
    [data-testid="stExpanderDetails"] li,
    [data-testid="stExpanderDetails"] strong { color: #ffffff !important; }
    div[data-testid="metric-container"] {
        background-color: #111111 !important;
        border: 0.5px solid #222222 !important;
        border-radius: 8px !important;
        padding: 12px !important;
    }
    div[data-testid="metric-container"] label { color: #aaaaaa !important; font-size: 12px !important; }
    div[data-testid="metric-container"] div { color: #ffffff !important; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("Military_emigration_and_conscription_-_Conscription.csv")
    df.columns = ["year", "spring", "autumn", "total"]
    for col in ["spring", "autumn", "total"]:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(".", ""), errors="coerce")
    return df

df = load_data()

st.title("Russian Military Conscription Quotas")
st.markdown(
    "<p style='color:#888888;font-size:13px;margin:-8px 0 16px;'>"
    "Annual conscription quotas in Russia by draft cycle, 2008–2026</p>",
    unsafe_allow_html=True,
)

with st.expander("About the data"):
    st.markdown("**What are we looking at?**")
    st.markdown("This chart shows Russia's annual military conscription quotas — the number of men called up for mandatory military service each year. Russia conducts two conscription cycles per year: a spring draft (April–July) and an autumn draft (October–December).")
    st.markdown("**Data source**")
    st.markdown("Data was collected from official Russian presidential decrees on conscription, published annually. Each decree specifies the number of citizens to be called up for that cycle.")
    st.markdown("**Note on 2026**")
    st.markdown("The 2026 figure reflects Russia's first year-round conscription system, signed into law in November 2025 and effective January 2026. The figure of 261,000 represents the total planned quota under the new system.")

st.markdown("<p style='height:8px'></p>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
pre_war  = df[df["year"] < 2022]["total"].mean()
post_war = df[df["year"] >= 2022]["total"].mean()
peak     = df["total"].max()
peak_yr  = int(df.loc[df["total"].idxmax(), "year"])
latest   = int(df[df["year"] == df["year"].max()]["total"].values[0])

col1.metric("Average pre-2022", f"{int(pre_war):,}")
col2.metric("Average 2022–2026", f"{int(post_war):,}")
col3.metric(f"Peak ({peak_yr})", f"{int(peak):,}")
col4.metric("Latest quota (2026)", f"{latest:,}")

st.markdown("<p style='height:8px'></p>", unsafe_allow_html=True)

fig = go.Figure()

fig.add_trace(go.Bar(
    x=df["year"], y=df["spring"],
    name="Spring draft",
    marker_color="rgba(0,87,231,0.6)",
    hovertemplate="<b>%{x}</b><br>Spring draft: %{y:,}<extra></extra>",
))

fig.add_trace(go.Bar(
    x=df["year"], y=df["autumn"],
    name="Autumn draft",
    marker_color="rgba(0,87,231,0.35)",
    hovertemplate="<b>%{x}</b><br>Autumn draft: %{y:,}<extra></extra>",
))

fig.add_trace(go.Scatter(
    x=df["year"], y=df["total"],
    name="Total",
    mode="lines+markers",
    line=dict(color="#0057E7", width=2.5),
    marker=dict(size=6, color="#0057E7"),
    hovertemplate="<b>%{x}</b><br>Total: %{y:,}<extra></extra>",
))

fig.add_shape(
    type="line", x0=2022, x1=2022, y0=0, y1=620000,
    line=dict(color="#aaaaaa", width=1, dash="dot"),
)
fig.add_annotation(
    x=2022, y=620000,
    text="<b>Full-scale invasion</b>",
    showarrow=False, yanchor="bottom",
    font=dict(size=10, color="#aaaaaa", family="Inter"),
    bgcolor="rgba(0,0,0,0.7)",
    bordercolor="#aaaaaa", borderwidth=0.5, borderpad=3,
)

fig.update_layout(
    barmode="stack",
    paper_bgcolor="#000000",
    plot_bgcolor="#000000",
    font=dict(family="Inter", size=13, color="#ffffff"),
    xaxis=dict(
        title="Year",
        tickfont=dict(color="#ffffff", family="Inter"),
        titlefont=dict(color="#ffffff", family="Inter"),
        showgrid=False,
        dtick=1,
        tickangle=-45,
        showline=False,
    ),
    yaxis=dict(
        title="Number of conscripts",
        tickfont=dict(color="#ffffff", family="Inter"),
        titlefont=dict(color="#ffffff", family="Inter"),
        gridcolor="#222222",
        showline=False,
        tickformat=",.0f",
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom", y=-0.3,
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
    margin=dict(t=20, b=80, l=70, r=20),
    height=480,
)

st.plotly_chart(fig, width="stretch")

st.markdown(
    "<p style='font-size:10px;color:#444444;margin:4px 0;'>"
    "Source: Official Russian presidential conscription decrees · "
    "Spring draft: April–July · Autumn draft: October–December</p>",
    unsafe_allow_html=True,
)
