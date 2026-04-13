import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Russian Conscription Timeline", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    * { font-family: 'Inter', sans-serif !important; }
    .stApp { background-color: #000000; color: #ffffff; }
    h1, h2, h3, h4 { color: #ffffff !important; }
    .stMarkdown, .stMarkdown p, .stMarkdown li { color: #ffffff !important; }
    .block-container { padding: 0rem 2rem !important; }
    [data-testid="stHeader"] { display: none !important; }
    .stButton > button {
        background-color: #000000 !important;
        color: #aaaaaa !important;
        border: 0.5px solid #333333 !important;
        border-radius: 8px !important;
        font-size: 13px !important;
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
    .info-box strong { color: #ffffff !important; }
</style>
""", unsafe_allow_html=True)

RED_SHADES = [
    "#ff6666",
    "#ff4444",
    "#E8000D",
    "#cc0000",
    "#aa0000",
    "#880000",
    "#660000",
]

events = [
    {
        "id": "E1",
        "date": "Feb 2022",
        "x": 2022.1,
        "short": "February 2022 — Full-scale invasion of Ukraine.",
        "context": (
            "On 24 February 2022, Russia launched a full-scale invasion of Ukraine. "
            "This followed the recognition of the self-proclaimed 'DPR' and 'LPR' on 21 February "
            "and the deployment of Russian troops under the label of a 'special military operation.' "
            "This event marked a major political and demographic turning point, significantly increasing "
            "the perceived risk of mobilization and triggering a wave of emigration from Russia."
        ),
    },
    {
        "id": "E2",
        "date": "Apr 2022",
        "x": 2022.32,
        "short": "April 2022 — Introduction of IT-sector conscription deferments.",
        "context": (
            "In spring 2022, the Russian government introduced conscription deferments for certain "
            "employees of accredited IT companies. The key legal basis was a government decree adopted "
            "on 28 March 2022. The policy aimed to retain highly skilled workers and curb the outflow "
            "of IT specialists following the outbreak of the war. Eligibility was limited to those "
            "meeting specific criteria related to age, education, and employment in accredited firms."
        ),
    },
    {
        "id": "E3",
        "date": "Sep 2022",
        "x": 2022.72,
        "short": "September 2022 — Announcement of partial mobilization.",
        "context": (
            "On 21 September 2022, President Vladimir Putin announced a partial mobilization and signed "
            "the corresponding decree. Officially framed as recruiting reservists with prior military "
            "experience, in practice the announcement dramatically increased uncertainty and fear among "
            "men of conscription age, leading to a sharp rise in emigration from Russia in the following weeks."
        ),
    },
    {
        "id": "E4",
        "date": "Sep 2022",
        "x": 2022.9,
        "short": "September 2022 — Expansion of student conscription deferments.",
        "context": (
            "On 24 September 2022, a decree granted deferments to students enrolled in full-time or "
            "part-time programs who were obtaining their education level for the first time. Initially "
            "covering a limited set of categories, the measure was later expanded in October to include "
            "additional groups such as certain postgraduate students and students in accredited private institutions."
        ),
    },
    {
        "id": "E5",
        "date": "Apr 2023",
        "x": 2023.3,
        "short": "April 2023 — Introduction of digital draft and electronic summons.",
        "context": (
            "Russia adopted legislation reforming the military registration and conscription system. "
            "The law introduced a unified digital register of persons liable for military service and "
            "legalized electronic draft notices. Crucially, a summons could now be considered legally "
            "delivered without personal receipt, once it appeared in the official registry. "
            "The reform also introduced penalties for non-compliance, including travel restrictions."
        ),
    },
    {
        "id": "E6",
        "date": "Jan 2024",
        "x": 2024.0,
        "short": "January 2024 — Increase of conscription age limit to 30.",
        "context": (
            "Russia raised the upper age limit for compulsory military service from 27 to 30 years. "
            "The law was signed on 4 August 2023 and entered into force on 1 January 2024. "
            "Despite earlier discussions, the lower bound remained unchanged at 18 years. "
            "This reform expanded the pool of men eligible for conscription."
        ),
    },
    {
        "id": "E7",
        "date": "Nov 2025",
        "x": 2025.85,
        "short": "Announced November 2025, effective January 2026 — Introduction of year-round conscription system.",
        "context": (
            "Russia adopted a law transitioning to a de facto year-round conscription system. "
            "The law was published on 4 November 2025 and came into force on 1 January 2026. "
            "Key procedures such as medical examinations, psychological screening, and draft commission "
            "decisions can now take place throughout the entire year. This reform reduces the previous "
            "seasonality of conscription pressure and makes the system more continuous and less predictable."
        ),
    },
]

# ── Title ──────────────────────────────────────────────────────────────────
st.markdown(
    "<h2 style='font-size:22px;font-weight:600;color:#ffffff;margin:16px 0 4px;'>"
    "Which events and policy changes shaped Russia's military recruitment since 2022?</h2>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='color:#888888;font-size:12px;margin:0 0 12px;'>"
    "Key events and changes in Russia's conscription system. Hover over each marker for details.</p>",
    unsafe_allow_html=True,
)

if "show_timeline_info" not in st.session_state:
    st.session_state.show_timeline_info = False

if st.button("About the data", key="timeline_info_btn"):
    st.session_state.show_timeline_info = not st.session_state.show_timeline_info

if st.session_state.show_timeline_info:
    st.markdown("""
    <div class="info-box">
        <p><strong>What are we looking at?</strong></p>
        <p>The timeline shows seven key events and policy changes in Russia's military conscription system since the full-scale invasion of Ukraine in February 2022. The events include major political turning points and specific legal reforms affecting men's obligation to serve.</p>
        <br>
        <p><strong>How did we build the dataset?</strong></p>
        <p>We identified and selected these seven events ourselves based on a systematic review of official Russian legislation, presidential decrees and news sources. Our selection focused on changes that directly affected the legal obligation of men to serve. We then coded each event as a binary variable (0 before, 1 after) to use in our statistical analysis.</p>
    </div>
    """, unsafe_allow_html=True)

# ── Build figure ───────────────────────────────────────────────────────────
fig = go.Figure()

fig.add_shape(
    type="line",
    x0=2021.7, x1=2026.3,
    y0=0, y1=0,
    line=dict(color="#550000", width=2.5),
)

y_positions = [1.4, -1.4, 1.4, -1.4, 1.4, -1.4, 1.4]
label_y     = [1.65, -1.65, 1.65, -1.65, 1.65, -1.65, 1.65]
anchor      = ["bottom", "top", "bottom", "top", "bottom", "top", "bottom"]

for i, ev in enumerate(events):
    y_pos = y_positions[i]
    col   = RED_SHADES[i]
    hover = f"<b>{ev['id']}: {ev['short']}</b><br><br><i>{ev['context']}</i>"

    fig.add_shape(
        type="line",
        x0=ev["x"], x1=ev["x"],
        y0=0, y1=y_pos * 0.88,
        line=dict(color=col, width=1.2, dash="dot"),
    )

    fig.add_trace(go.Scatter(
        x=[ev["x"]], y=[0],
        mode="markers",
        marker=dict(size=18, color=col, line=dict(color="#000000", width=2)),
        hovertemplate=hover + "<extra></extra>",
        showlegend=False,
    ))

    fig.add_trace(go.Scatter(
        x=[ev["x"]], y=[y_pos * 0.5],
        mode="markers",
        marker=dict(size=30, color="rgba(0,0,0,0)"),
        hovertemplate=hover + "<extra></extra>",
        showlegend=False,
    ))

    fig.add_annotation(
        x=ev["x"], y=label_y[i],
        text=f"<b>{ev['id']}</b><br><span style='font-size:10px;color:#888888'>{ev['date']}</span>",
        showarrow=False,
        yanchor=anchor[i],
        font=dict(size=13, color=col, family="Inter"),
        bgcolor="rgba(0,0,0,0)",
        borderpad=3,
        align="center",
    )

fig.update_layout(
    paper_bgcolor="#000000",
    plot_bgcolor="#000000",
    font=dict(family="Inter", size=13, color="#ffffff"),
    xaxis=dict(
        range=[2021.5, 2026.5],
        tickvals=[2022, 2023, 2024, 2025, 2026],
        ticktext=["2022", "2023", "2024", "2025", "2026"],
        tickfont=dict(color="#666666", family="Inter", size=13),
        showgrid=False,
        showline=False,
        zeroline=False,
    ),
    yaxis=dict(
        range=[-2.2, 2.2],
        showgrid=False,
        showline=False,
        zeroline=False,
        showticklabels=False,
    ),
    hoverlabel=dict(
        align="left",
        bgcolor="#111111",
        bordercolor="#333333",
        font=dict(color="#ffffff", size=12, family="Inter"),
        namelength=0,
    ),
    hovermode="closest",
    margin=dict(t=10, b=50, l=20, r=20),
    height=420,
)

st.plotly_chart(fig, width="stretch")

st.markdown(
    "<p style='font-size:10px;color:#444444;margin:4px 0;'>"
    "Source: Official Russian legislation and presidential decrees · "
    "Events dataset self-constructed by the authors.</p>",
    unsafe_allow_html=True,
)
