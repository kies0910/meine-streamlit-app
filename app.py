import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Russian Asylum Applications", layout="wide")

# ── Black background via CSS ───────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #000000; color: #ffffff; }
    .stMarkdown, .stMarkdown p, .stMarkdown li { color: #ffffff !important; }
    h1, h2, h3, h4 { color: #ffffff !important; }
    .stButton > button {
        background-color: #000000;
        color: #ffffff;
        border: 1px solid #ffffff;
    }
    .stButton > button:hover { background-color: #222222; }
    .streamlit-expanderHeader { color: #ffffff !important; }
    .streamlit-expanderContent { background-color: #111111 !important; color: #ffffff !important; }
</style>
""", unsafe_allow_html=True)

# ── Title + methodology button ─────────────────────────────────────────────
col1, col2 = st.columns([5, 1])
with col1:
    st.title("Russian Asylum Applications to the EU")
    st.markdown("*Mean monthly asylum applications per country — men vs. women aged 18–34*")
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    show_info = st.button("About the data")

if show_info:
    with st.expander("About the data", expanded=True):
        st.markdown("""
        **What are we looking at?**
        This chart shows the mean number of monthly first-time asylum applications
        filed by Russian citizens aged 18–34 across all EU member states,
        from January 2017 to early 2026. Applications are split by sex (men vs. women)
        and averaged per country per month to make countries comparable regardless of size.

        **Dependent variable**
        The dependent variable is the number of asylum applications submitted by
        Russian men and women of conscription age (18–34) to EU countries.
        This is used as a proxy for migration driven by conscription pressure —
        since asylum is one of the few legal routes available when leaving Russia
        under wartime conditions.

        **Data collection**
        Data was retrieved from Eurostat's monthly asylum statistics database
        (MIGR_ASYAPPCTZM), which covers all EU member states.
        We filtered for: Russian citizens, aged 18–34, first-time applicants only,
        broken down by sex and receiving country.

        **How the chart is built**
        Each dot represents the mean monthly applications per EU country for that month.
        The solid line is a 3-month rolling average to smooth out short-term fluctuations
        and make the trend easier to read.

        **Event markers (E1–E7)**
        The seven dotted vertical lines mark key changes to Russia's military
        recruitment system since February 2022. Hover over a line to see the full event name.
        E3 and E4 share the same date (September 2022) and are shown as one line —
        hover over it to see both events.

        **Statistical method**
        We use a Difference-in-Differences (DiD) design — comparing men (treatment group)
        to women (control group) before and after each event. Women serve as a counterfactual:
        if both groups move similarly, the change is not conscription-related.
        A larger increase in men's applications after an event suggests a conscription effect.

        **Limitations**
        Asylum captures only part of total emigration — men with more resources may have
        left via study or work permits, which are not included here.
        Results show a strong association, not definitive causality.
        """)

# ── Load data ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    asylum = pd.read_csv("asylum.csv")
    asylum["OBS_VALUE"] = pd.to_numeric(asylum["OBS_VALUE"], errors="coerce")
    asylum = asylum.dropna(subset=["OBS_VALUE"])
    monthly = (
        asylum.groupby(["TIME_PERIOD", "sex"])["OBS_VALUE"]
        .mean()
        .reset_index()
    )
    monthly.columns = ["month", "sex", "mean_apps"]
    monthly["month_dt"] = pd.to_datetime(monthly["month"])
    return monthly

data = load_data()
men   = data[data["sex"] == "Males"].sort_values("month_dt")
women = data[data["sex"] == "Females"].sort_values("month_dt")
men["smooth"]   = men["mean_apps"].rolling(3, center=True).mean()
women["smooth"] = women["mean_apps"].rolling(3, center=True).mean()

# ── Events — E3 and E4 share one line, combined hover ─────────────────────
# Single events: (date, label, annotation_y, x_shift)
single_events = [
    ("2022-02-01", "E1: Full-scale invasion",       52, 0),
    ("2022-04-01", "E2: IT deferment",               52, 0),
    ("2023-04-01", "E5: Digital draft",              52, 0),
    ("2024-01-01", "E6: Age expansion",              52, 0),
    ("2025-09-01", "E7: Year-round conscription",    52, 0),
]

# E3 + E4 combined on one line
combined_event = {
    "date": "2022-09-01",
    "label": "E3: Mobilization<br>E4: Student deferment",
    "short": "E3 / E4",
    "ann_y": 52,
}

MEN_COLOR   = "#E8000D"
WOMEN_COLOR = "#0057E7"
EVENT_COLOR = "#aaaaaa"
BG_COLOR    = "#000000"
GRID_COLOR  = "#333333"

# ── Figure ─────────────────────────────────────────────────────────────────
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

# Smooth lines
fig.add_trace(go.Scatter(
    x=men["month_dt"], y=men["smooth"],
    mode="lines", line=dict(color=MEN_COLOR, width=3),
    name="Men",
    hovertemplate="%{x|%Y-%m}<br><b>Men: %{y:.1f}</b><extra></extra>",
))
fig.add_trace(go.Scatter(
    x=women["month_dt"], y=women["smooth"],
    mode="lines", line=dict(color=WOMEN_COLOR, width=3),
    name="Women",
    hovertemplate="%{x|%Y-%m}<br><b>Women: %{y:.1f}</b><extra></extra>",
))

# Single event lines
for date_str, label, ann_y, x_shift in single_events:
    dt = pd.to_datetime(date_str)
    short = label.split(":")[0]
    fig.add_shape(
        type="line", x0=dt, x1=dt, y0=0, y1=50,
        line=dict(color=EVENT_COLOR, width=1.2, dash="dot"),
    )
    fig.add_annotation(
        x=dt, y=ann_y, xshift=x_shift,
        text=f"<b>{short}</b>",
        showarrow=False, yanchor="bottom",
        font=dict(size=10, color="#ffffff"),
        bgcolor="rgba(0,0,0,0.7)",
        bordercolor=EVENT_COLOR, borderwidth=0.5, borderpad=3,
    )
    fig.add_trace(go.Scatter(
        x=[dt, dt], y=[0, 50],
        mode="lines",
        line=dict(color="rgba(0,0,0,0)", width=14),
        hovertemplate=f"<b>{label}</b><extra></extra>",
        showlegend=False,
    ))

# Combined E3 + E4 line
dt_combined = pd.to_datetime(combined_event["date"])
fig.add_shape(
    type="line", x0=dt_combined, x1=dt_combined, y0=0, y1=50,
    line=dict(color=EVENT_COLOR, width=1.2, dash="dot"),
)
fig.add_annotation(
    x=dt_combined, y=combined_event["ann_y"],
    text=f"<b>{combined_event['short']}</b>",
    showarrow=False, yanchor="bottom",
    font=dict(size=10, color="#ffffff"),
    bgcolor="rgba(0,0,0,0.7)",
    bordercolor=EVENT_COLOR, borderwidth=0.5, borderpad=3,
)
# One invisible hover line showing BOTH events
fig.add_trace(go.Scatter(
    x=[dt_combined, dt_combined], y=[0, 50],
    mode="lines",
    line=dict(color="rgba(0,0,0,0)", width=14),
    hovertemplate=f"<b>{combined_event['label']}</b><extra></extra>",
    showlegend=False,
))

fig.update_layout(
    height=540,
    plot_bgcolor=BG_COLOR,
    paper_bgcolor=BG_COLOR,
    font=dict(family="Arial", size=13, color="#ffffff"),
    xaxis=dict(
        showline=False,
        title="Month",
        title_font=dict(color="#ffffff"),
        tickfont=dict(color="#ffffff"),
        showgrid=True, gridcolor=GRID_COLOR,
        tickangle=-45,
        linecolor="#ffffff",
    ),
    yaxis=dict(
        showline=False,
        title="Mean monthly asylum applications per country",
        title_font=dict(color="#ffffff"),
        tickfont=dict(color="#ffffff"),
        showgrid=True, gridcolor=GRID_COLOR,
        range=[0, 58],
        linecolor="#ffffff",
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom", y=-0.25,
        xanchor="center", x=0.5,
        font=dict(size=14, color="#ffffff"),
        bgcolor="rgba(0,0,0,0)",
    ),
    hovermode="closest",
    margin=dict(t=20, b=80, l=70, r=20),
)

st.plotly_chart(fig, width="stretch")

# ── Event legend ───────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("**Conscription-policy events**")
cols = st.columns(4)
descriptions = [
    ("E1", "Full-scale invasion",     "Feb 2022", "Russia launches full-scale invasion of Ukraine"),
    ("E2", "IT deferment",            "Apr 2022", "IT workers granted deferment from military service"),
    ("E3", "Mobilization",            "Sep 2022", "Partial mobilization — 300,000 reservists called up"),
    ("E4", "Student deferment",       "Sep 2022", "University students granted temporary deferment"),
    ("E5", "Digital draft",           "Apr 2023", "Electronic summons via Gosuslugi portal introduced"),
    ("E6", "Age expansion",           "Jan 2024", "Upper conscription age expanded from 27 to 30 years"),
    ("E7", "Year-round conscription", "Nov 2025", "Draft boards now operate year-round, removing seasonal limits"),
]
for i, (code, name, date, desc) in enumerate(descriptions):
    cols[i % 4].markdown(f"**{code} — {name}** ({date})  \n{desc}")
