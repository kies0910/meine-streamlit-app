import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Russian Asylum Applications", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    * { font-family: 'Inter', sans-serif !important; }
    .stApp { background-color: #000000; color: #ffffff; }
    h1, h2, h3, h4 { color: #ffffff !important; }
    .stMarkdown, .stMarkdown p, .stMarkdown li { color: #ffffff !important; }
    .stButton > button {
        background-color: #000000 !important;
        color: #ffffff !important;
        border: 0.5px solid #555555 !important;
        border-radius: 8px !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        padding: 8px 16px !important;
    }
    .stButton > button:hover {
        border-color: #aaaaaa !important;
        color: #cccccc !important;
    }
    .info-box {
        background-color: #111111;
        border: 0.5px solid #555555;
        border-radius: 8px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1rem;
    }
    .info-box p {
        color: #ffffff !important;
        font-size: 14px !important;
        line-height: 1.7 !important;
        margin: 0.3rem 0 !important;
    }
    .info-box strong { color: #ffffff !important; }
</style>
""", unsafe_allow_html=True)

st.markdown(
    "<h2 style='font-size:22px;font-weight:600;color:#ffffff;margin:16px 0 4px;'>"
    "Did Russia's military recruitment changes drive men to flee?</h2>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='color:#888888;font-size:12px;margin:0 0 12px;'>"
    "Mean monthly asylum applications per EU country — men vs. women aged 18–34</p>",
    unsafe_allow_html=True,
)

if "show_info" not in st.session_state:
    st.session_state.show_info = False

if st.button("About the data"):
    st.session_state.show_info = not st.session_state.show_info

if st.session_state.show_info:
    st.markdown("""
    <div class="info-box">
        <p><strong>What are we looking at?</strong></p>
        <p>This chart tracks the average number of monthly first-time asylum applications by Russian citizens aged 18–34, broken down by sex and EU country, from January 2017 to October 2025. We compare men (treatment group) and women (control group) to see whether key events and changes in Russia's military recruitment system drive emigration, measured here through asylum applications. Each dot shows the raw average number. The red and blue lines are smoothed trend lines. When you hover over the line, you see the raw monthly average, the total number of applications across all EU countries that month, and the percentage change compared to the previous month. Data comes from Eurostat's monthly asylum applications database.</p>
        <br>
        <p><strong>Event markers (E1–E7)</strong></p>
        <p>The dotted vertical lines mark seven key events and changes that affect Russia's military recruitment system since February 2022. Hover over a line to see the event name and a short description of what changed.</p>
        <br>
        <p><strong>Note</strong></p>
        <p>Asylum applications are only one migration route. Men may have also left via residence permits — our residence permit dataset covers this separately but is only available as annual data.</p>
    </div>
    """, unsafe_allow_html=True)

EU_COUNTRIES = [
    "Austria","Belgium","Bulgaria","Croatia","Cyprus","Czechia",
    "Denmark","Estonia","Finland","France","Germany","Greece",
    "Hungary","Ireland","Italy","Latvia","Lithuania","Luxembourg",
    "Malta","Netherlands","Poland","Portugal","Romania",
    "Slovakia","Slovenia","Spain","Sweden"
]

@st.cache_data
def load_data():
    asylum = pd.read_csv("asylum.csv")
    asylum["OBS_VALUE"] = pd.to_numeric(asylum["OBS_VALUE"], errors="coerce")
    asylum = asylum.dropna(subset=["OBS_VALUE"])
    asylum = asylum[asylum["geo"].isin(EU_COUNTRIES)]
    monthly = (
        asylum.groupby(["TIME_PERIOD", "sex"])["OBS_VALUE"]
        .mean().reset_index()
    )
    monthly.columns = ["month", "sex", "mean_apps"]
    monthly["month_dt"] = pd.to_datetime(monthly["month"])
    total = (
        asylum.groupby(["TIME_PERIOD", "sex"])["OBS_VALUE"]
        .sum().reset_index()
    )
    total.columns = ["month", "sex", "total"]
    monthly = monthly.merge(total, on=["month", "sex"])
    return monthly

data = load_data()

men   = data[data["sex"] == "Males"].sort_values("month_dt").reset_index(drop=True)
women = data[data["sex"] == "Females"].sort_values("month_dt").reset_index(drop=True)

men["smooth"]       = men["mean_apps"].rolling(3, center=True).mean()
women["smooth"]     = women["mean_apps"].rolling(3, center=True).mean()
men["pct_change"]   = men["mean_apps"].pct_change() * 100
women["pct_change"] = women["mean_apps"].pct_change() * 100

def make_hover(row):
    pct = row["pct_change"]
    pct_str = f"{pct:+.1f}%" if not pd.isna(pct) else "—"
    return (
        f"{row['month']}<br>"
        f"<b>Mean: {row['mean_apps']:.1f}</b><br>"
        f"Total: {int(row['total']):,}<br>"
        f"Vs prev. month: {pct_str}"
    )

men["hover"]   = men.apply(make_hover, axis=1)
women["hover"] = women.apply(make_hover, axis=1)

# ── Events ─────────────────────────────────────────────────────────────────
YMAX    = 20   # axis max
LINE_Y  = 18   # dotted line height
ANN_Y   = 18   # label height
HOV_Y   = 18   # hover marker midpoint

single_events = [
    ("2022-02-01", "E1", "E1: Full-scale invasion",
     "February 2022 — Russia begins its full-scale invasion of Ukraine."),
    ("2022-04-01", "E2", "E2: IT deferment",
     "April 2022 — IT workers granted deferment from military service."),
    ("2023-04-01", "E5", "E5: Digital draft",
     "April 2023 — Russia introduces digital draft notices."),
    ("2024-01-01", "E6", "E6: Age expansion",
     "January 2024 — Upper conscription age expanded from 27 to 30 years."),
    ("2025-09-01", "E7", "E7: Year-round conscription",
     "Announced November 2025, effective January 2026 — Russia introduces year-round conscription processing."),
]

combined_event = {
    "date":  "2022-09-01",
    "short": "E3/E4",
    "hover": (
        "<b>E3: Mobilization</b><br>"
        "September 2022 — Partial mobilization announced. Around 300,000 reservists called up.<br><br>"
        "<b>E4: Student deferment</b><br>"
        "September 2022 — University students granted temporary deferment from military service."
    ),
}

MEN_COLOR   = "#E8000D"
WOMEN_COLOR = "#0057E7"
EVENT_COLOR = "#aaaaaa"
BG_COLOR    = "#000000"
GRID_COLOR  = "#333333"

fig = go.Figure()

# Raw dots
fig.add_trace(go.Scatter(
    x=men["month_dt"], y=men["mean_apps"],
    mode="markers",
    marker=dict(color=MEN_COLOR, size=5, opacity=0.3),
    showlegend=False, hoverinfo="skip",
))
fig.add_trace(go.Scatter(
    x=women["month_dt"], y=women["mean_apps"],
    mode="markers",
    marker=dict(color=WOMEN_COLOR, size=5, opacity=0.3),
    showlegend=False, hoverinfo="skip",
))

# Smoothed lines
fig.add_trace(go.Scatter(
    x=men["month_dt"], y=men["smooth"],
    mode="lines", line=dict(color=MEN_COLOR, width=3),
    name="Men",
    text=men["hover"],
    hovertemplate="%{text}<extra>Men</extra>",
))
fig.add_trace(go.Scatter(
    x=women["month_dt"], y=women["smooth"],
    mode="lines", line=dict(color=WOMEN_COLOR, width=3),
    name="Women",
    text=women["hover"],
    hovertemplate="%{text}<extra>Women</extra>",
))

# Single event lines
for date_str, short, label, desc in single_events:
    dt = pd.to_datetime(date_str)
    fig.add_shape(
        type="line", x0=dt, x1=dt, y0=0, y1=LINE_Y,
        line=dict(color=EVENT_COLOR, width=1.2, dash="dot"),
    )
    fig.add_annotation(
        x=dt, y=ANN_Y,
        text=f"<b>{short}</b>",
        showarrow=False, yanchor="bottom",
        font=dict(size=10, color="#ffffff", family="Inter"),
        bgcolor="rgba(0,0,0,0.7)",
        bordercolor=EVENT_COLOR, borderwidth=0.5, borderpad=3,
    )
    # Wide invisible hover marker at midpoint
    fig.add_trace(go.Scatter(
        x=[dt], y=[HOV_Y],
        mode="markers",
        marker=dict(size=40, color="rgba(0,0,0,0)"),
        hovertemplate=f"<b>{label}</b><br>{desc}<extra></extra>",
        showlegend=False,
    ))

# Combined E3/E4
dt_c = pd.to_datetime(combined_event["date"])
fig.add_shape(
    type="line", x0=dt_c, x1=dt_c, y0=0, y1=LINE_Y,
    line=dict(color=EVENT_COLOR, width=1.2, dash="dot"),
)
fig.add_annotation(
    x=dt_c, y=ANN_Y,
    text=f"<b>{combined_event['short']}</b>",
    showarrow=False, yanchor="bottom",
    font=dict(size=10, color="#ffffff", family="Inter"),
    bgcolor="rgba(0,0,0,0.7)",
    bordercolor=EVENT_COLOR, borderwidth=0.5, borderpad=3,
)
fig.add_trace(go.Scatter(
    x=[dt_c], y=[HOV_Y],
    mode="markers",
    marker=dict(size=40, color="rgba(0,0,0,0)"),
    hovertemplate=f"{combined_event['hover']}<extra></extra>",
    showlegend=False,
))

fig.update_layout(
    height=540,
    plot_bgcolor=BG_COLOR,
    paper_bgcolor=BG_COLOR,
    font=dict(family="Inter", size=13, color="#ffffff"),
    hoverlabel=dict(
        align="left",
        bgcolor="#222222",
        font=dict(color="#ffffff", size=13, family="Inter"),
    ),
    xaxis=dict(
        title="Month",
        title_font=dict(color="#ffffff", family="Inter"),
        tickfont=dict(color="#ffffff", family="Inter"),
        showgrid=True, gridcolor=GRID_COLOR,
        tickangle=-45,
        showline=False,
    ),
    yaxis=dict(
        title="Mean monthly asylum applications per EU country",
        title_font=dict(color="#ffffff", family="Inter"),
        tickfont=dict(color="#ffffff", family="Inter"),
        showgrid=True, gridcolor=GRID_COLOR,
        range=[0, YMAX],
        showline=False,
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom", y=-0.25,
        xanchor="center", x=0.5,
        font=dict(size=14, color="#ffffff", family="Inter"),
        bgcolor="rgba(0,0,0,0)",
    ),
    hovermode="closest",
    margin=dict(t=20, b=80, l=70, r=20),
)

st.plotly_chart(fig, width="stretch")
