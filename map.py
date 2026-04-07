import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# ── Data ───────────────────────────────────────────────────────────────────

ASYLUM_DATA = {
    "Germany":      {"total": 14330, "pct": 32.6},
    "France":       {"total": 10040, "pct": 22.9},
    "Poland":       {"total":  4145, "pct":  9.4},
    "Spain":        {"total":  2795, "pct":  6.4},
    "Austria":      {"total":  2230, "pct":  5.1},
    "Belgium":      {"total":  2070, "pct":  4.7},
    "Netherlands":  {"total":  1920, "pct":  4.4},
    "Finland":      {"total":  1520, "pct":  3.5},
    "Sweden":       {"total":  1385, "pct":  3.2},
    "Italy":        {"total":  1030, "pct":  2.3},
    "Croatia":      {"total":   965, "pct":  2.2},
    "Czechia":      {"total":   365, "pct":  0.8},
    "Denmark":      {"total":   235, "pct":  0.5},
    "Lithuania":    {"total":   225, "pct":  0.5},
    "Slovenia":     {"total":   155, "pct":  0.4},
    "Bulgaria":     {"total":   130, "pct":  0.3},
    "Estonia":      {"total":   120, "pct":  0.3},
    "Greece":       {"total":    95, "pct":  0.2},
    "Latvia":       {"total":    70, "pct":  0.2},
    "Portugal":     {"total":    50, "pct":  0.1},
    "Romania":      {"total":    20, "pct":  0.0},
    "Ireland":      {"total":    20, "pct":  0.0},
    "Cyprus":       {"total":    10, "pct":  0.0},
    "Malta":        {"total":     0, "pct":  0.0},
    "Luxembourg":   {"total":     0, "pct":  0.0},
    "Hungary":      {"total":     0, "pct":  0.0},
    "Slovakia":     {"total":     0, "pct":  0.0},
}

PERMITS_DATA = {
    "Poland":       {"total":  9663, "pct": 14.6},
    "Germany":      {"total":  9151, "pct": 13.8},
    "Czechia":      {"total":  8141, "pct": 12.3},
    "France":       {"total":  6802, "pct": 10.3},
    "Spain":        {"total":  5770, "pct":  8.7},
    "Cyprus":       {"total":  4436, "pct":  6.7},
    "Netherlands":  {"total":  3757, "pct":  5.7},
    "Finland":      {"total":  3306, "pct":  5.0},
    "Austria":      {"total":  2324, "pct":  3.5},
    "Hungary":      {"total":  1931, "pct":  2.9},
    "Italy":        {"total":  1657, "pct":  2.5},
    "Lithuania":    {"total":  1372, "pct":  2.1},
    "Sweden":       {"total":  1200, "pct":  1.8},
    "Bulgaria":     {"total":  1064, "pct":  1.6},
    "Portugal":     {"total":   823, "pct":  1.2},
    "Estonia":      {"total":   783, "pct":  1.2},
    "Ireland":      {"total":   750, "pct":  1.1},
    "Belgium":      {"total":   698, "pct":  1.1},
    "Latvia":       {"total":   529, "pct":  0.8},
    "Denmark":      {"total":   472, "pct":  0.7},
    "Greece":       {"total":   449, "pct":  0.7},
    "Slovenia":     {"total":   430, "pct":  0.6},
    "Croatia":      {"total":   308, "pct":  0.5},
    "Luxembourg":   {"total":   266, "pct":  0.4},
    "Romania":      {"total":   160, "pct":  0.2},
    "Slovakia":     {"total":    95, "pct":  0.1},
    "Malta":        {"total":    19, "pct":  0.0},
}

# Country coordinates (lon, lat)
COUNTRY_COORDS = {
    "Germany":     (10.4,  51.2),
    "France":       (2.3,  46.2),
    "Poland":      (19.1,  51.9),
    "Spain":       (-3.7,  40.4),
    "Austria":     (14.5,  47.5),
    "Belgium":      (4.5,  50.5),
    "Netherlands":  (5.3,  52.1),
    "Finland":     (25.7,  61.9),
    "Sweden":      (18.6,  59.3),
    "Italy":       (12.6,  41.9),
    "Croatia":     (15.2,  45.1),
    "Czechia":     (15.5,  49.8),
    "Denmark":      (9.5,  56.3),
    "Lithuania":   (23.9,  55.2),
    "Slovenia":    (14.9,  46.1),
    "Bulgaria":    (25.5,  42.7),
    "Estonia":     (24.7,  58.6),
    "Greece":      (21.8,  39.1),
    "Latvia":      (24.6,  56.9),
    "Portugal":    (-8.2,  39.4),
    "Romania":     (24.9,  45.9),
    "Ireland":     (-8.2,  53.4),
    "Cyprus":      (33.4,  35.1),
    "Malta":       (14.4,  35.9),
    "Luxembourg":   (6.1,  49.8),
    "Hungary":     (19.5,  47.2),
    "Slovakia":    (19.7,  48.7),
}

# Russia origin point (Moscow)
RUSSIA_COORD = (37.6, 55.7)

# ── Map builder ────────────────────────────────────────────────────────────

def build_map(mode="Asylum"):
    data = ASYLUM_DATA if mode == "Asylum" else PERMITS_DATA
    label = "asylum applications" if mode == "Asylum" else "residence permit applications"
    max_val = max(d["total"] for d in data.values()) or 1

    fig = go.Figure()

    # ── Choropleth base map ────────────────────────────────────────────────
    countries  = list(data.keys())
    pct_values = [data[c]["pct"] for c in countries]
    totals     = [data[c]["total"] for c in countries]

    # ISO codes for choropleth
    iso_map = {
        "Germany": "DEU", "France": "FRA", "Poland": "POL", "Spain": "ESP",
        "Austria": "AUT", "Belgium": "BEL", "Netherlands": "NLD", "Finland": "FIN",
        "Sweden": "SWE", "Italy": "ITA", "Croatia": "HRV", "Czechia": "CZE",
        "Denmark": "DNK", "Lithuania": "LTU", "Slovenia": "SVN", "Bulgaria": "BGR",
        "Estonia": "EST", "Greece": "GRC", "Latvia": "LVA", "Portugal": "PRT",
        "Romania": "ROU", "Ireland": "IRL", "Cyprus": "CYP", "Malta": "MLT",
        "Luxembourg": "LUX", "Hungary": "HUN", "Slovakia": "SVK",
        "Russia": "RUS",
    }

    iso_codes    = [iso_map[c] for c in countries]
    hover_texts  = [
        f"<b>{c}</b><br>{data[c]['pct']}% of total<br>{data[c]['total']:,} {label}"
        for c in countries
    ]

    fig.add_trace(go.Choropleth(
        locations      = iso_codes,
        z              = pct_values,
        locationmode   = "ISO-3",
        colorscale     = [
            [0.0,  "#111111"],
            [0.01, "#1a0a0a"],
            [0.1,  "#6b0000"],
            [0.3,  "#b00000"],
            [0.6,  "#d40000"],
            [1.0,  "#E8000D"],
        ],
        zmin           = 0,
        zmax           = max(pct_values),
        showscale      = True,
        colorbar       = dict(
            title      = dict(text="% of total", font=dict(color="#ffffff", family="Inter", size=12)),
            tickfont   = dict(color="#ffffff", family="Inter", size=11),
            bgcolor    = "#000000",
            bordercolor= "#333333",
            thickness  = 14,
            len        = 0.5,
            x          = 1.01,
        ),
        text           = hover_texts,
        hovertemplate  = "%{text}<extra></extra>",
        marker_line_color  = "#333333",
        marker_line_width  = 0.5,
    ))

    # Russia in blue
    fig.add_trace(go.Choropleth(
        locations     = ["RUS"],
        z             = [1],
        locationmode  = "ISO-3",
        colorscale    = [[0, "#0057E7"], [1, "#0057E7"]],
        showscale     = False,
        hovertemplate = "<b>Russia</b><br>Origin country<extra></extra>",
        marker_line_color = "#333333",
        marker_line_width = 0.5,
    ))

    # ── Route lines from Russia to each country ────────────────────────────
    for country, coord in COUNTRY_COORDS.items():
        if country not in data:
            continue
        total = data[country]["total"]
        pct   = data[country]["pct"]
        # Line width proportional to total
        width = max(0.5, (total / max_val) * 5)
        alpha = max(0.15, min(0.85, total / max_val))

        fig.add_trace(go.Scattergeo(
            lon  = [RUSSIA_COORD[0], coord[0]],
            lat  = [RUSSIA_COORD[1], coord[1]],
            mode = "lines",
            line = dict(
                width = width,
                color = f"rgba(232,0,13,{alpha:.2f})",
            ),
            hovertemplate = (
                f"<b>Russia → {country}</b><br>"
                f"{pct}% of total<br>"
                f"{total:,} {label}"
                f"<extra></extra>"
            ),
            showlegend = False,
        ))

    # ── Country dots ──────────────────────────────────────────────────────
    lons = [COUNTRY_COORDS[c][0] for c in countries if c in COUNTRY_COORDS]
    lats = [COUNTRY_COORDS[c][1] for c in countries if c in COUNTRY_COORDS]
    dots_text = [
        f"<b>{c}</b><br>{data[c]['pct']}% of total<br>{data[c]['total']:,} {label}"
        for c in countries if c in COUNTRY_COORDS
    ]
    dot_sizes = [
        max(6, (data[c]["total"] / max_val) * 20)
        for c in countries if c in COUNTRY_COORDS
    ]

    fig.add_trace(go.Scattergeo(
        lon            = lons,
        lat            = lats,
        mode           = "markers",
        marker         = dict(
            size       = dot_sizes,
            color      = "#E8000D",
            opacity    = 0.85,
            line       = dict(color="#ffffff", width=0.5),
        ),
        text           = dots_text,
        hovertemplate  = "%{text}<extra></extra>",
        showlegend     = False,
    ))

    # Russia dot
    fig.add_trace(go.Scattergeo(
        lon            = [RUSSIA_COORD[0]],
        lat            = [RUSSIA_COORD[1]],
        mode           = "markers+text",
        marker         = dict(size=14, color="#0057E7", line=dict(color="#ffffff", width=1)),
        text           = ["Russia"],
        textposition   = "bottom center",
        textfont       = dict(color="#ffffff", size=11, family="Inter"),
        hovertemplate  = "<b>Russia</b><br>Origin country<extra></extra>",
        showlegend     = False,
    ))

    # ── Layout ────────────────────────────────────────────────────────────
    fig.update_layout(
        paper_bgcolor = "#000000",
        geo = dict(
            scope          = "europe",
            showframe      = False,
            showcoastlines = True,
            coastlinecolor = "#333333",
            showland       = True,
            landcolor      = "#111111",
            showocean      = True,
            oceancolor     = "#000000",
            showlakes      = False,
            showrivers     = False,
            bgcolor        = "#000000",
            projection_type= "natural earth",
            lonaxis_range  = [-15, 65],
            lataxis_range  = [30, 73],
        ),
        margin   = dict(t=10, b=0, l=0, r=0),
        height   = 580,
        hoverlabel = dict(
            align   = "left",
            bgcolor = "#222222",
            font    = dict(color="#ffffff", size=13, family="Inter"),
        ),
    )

    return fig


# ── Streamlit UI ───────────────────────────────────────────────────────────

st.markdown("---")
st.markdown("### Where did Russian men go?")
st.markdown(
    "*Routes and destination countries for Russian men aged 18–34 — "
    "click on a country or hover over a route to see the share of applications.*"
)

mode = st.radio(
    "Show:",
    ["Asylum", "Residence Permits"],
    horizontal=True,
    label_visibility="collapsed",
)

st.markdown("""
<style>
    div[data-testid="stRadio"] label {
        color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
    }
    div[data-testid="stRadio"] > div {
        gap: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

fig = build_map(mode)
st.plotly_chart(fig, width="stretch")

# Caption
if mode == "Asylum":
    st.caption(
        "Data: Eurostat MIGR_ASYAPPCTZM · Russian men aged 18–34 · First-time applicants · 2017–2026 · "
        "Line thickness proportional to number of applications."
    )
else:
    st.caption(
        "Data: Eurostat MIGR_RESFAS · Russian men aged 18–29 · 2017–2024 · "
        "Line thickness proportional to number of applications."
    )


import streamlit as st
import plotly.graph_objects as go

ASYLUM_GLOBAL_MAX  = 42.0
PERMITS_GLOBAL_MAX = 17.0

ASYLUM_BY_YEAR = {
    2017: {"Austria":{"total":250,"pct":6.5},"Belgium":{"total":155,"pct":4.0},"Bulgaria":{"total":0,"pct":0.0},"Croatia":{"total":0,"pct":0.0},"Cyprus":{"total":0,"pct":0.0},"Czechia":{"total":5,"pct":0.1},"Denmark":{"total":30,"pct":0.8},"Estonia":{"total":0,"pct":0.0},"Finland":{"total":140,"pct":3.6},"France":{"total":790,"pct":20.5},"Germany":{"total":1290,"pct":33.5},"Greece":{"total":0,"pct":0.0},"Hungary":{"total":0,"pct":0.0},"Ireland":{"total":0,"pct":0.0},"Italy":{"total":40,"pct":1.0},"Latvia":{"total":0,"pct":0.0},"Lithuania":{"total":45,"pct":1.2},"Luxembourg":{"total":0,"pct":0.0},"Malta":{"total":0,"pct":0.0},"Netherlands":{"total":120,"pct":3.1},"Poland":{"total":730,"pct":19.0},"Portugal":{"total":0,"pct":0.0},"Romania":{"total":0,"pct":0.0},"Slovakia":{"total":0,"pct":0.0},"Slovenia":{"total":0,"pct":0.0},"Spain":{"total":95,"pct":2.5},"Sweden":{"total":160,"pct":4.2}},
    2018: {"Austria":{"total":150,"pct":3.7},"Belgium":{"total":130,"pct":3.2},"Bulgaria":{"total":0,"pct":0.0},"Croatia":{"total":0,"pct":0.0},"Cyprus":{"total":0,"pct":0.0},"Czechia":{"total":20,"pct":0.5},"Denmark":{"total":30,"pct":0.7},"Estonia":{"total":10,"pct":0.2},"Finland":{"total":160,"pct":4.0},"France":{"total":1315,"pct":32.6},"Germany":{"total":1130,"pct":28.0},"Greece":{"total":0,"pct":0.0},"Hungary":{"total":0,"pct":0.0},"Ireland":{"total":0,"pct":0.0},"Italy":{"total":70,"pct":1.7},"Latvia":{"total":0,"pct":0.0},"Lithuania":{"total":0,"pct":0.0},"Luxembourg":{"total":0,"pct":0.0},"Malta":{"total":0,"pct":0.0},"Netherlands":{"total":175,"pct":4.3},"Poland":{"total":525,"pct":13.0},"Portugal":{"total":0,"pct":0.0},"Romania":{"total":0,"pct":0.0},"Slovakia":{"total":0,"pct":0.0},"Slovenia":{"total":0,"pct":0.0},"Spain":{"total":175,"pct":4.3},"Sweden":{"total":145,"pct":3.6}},
    2019: {"Austria":{"total":95,"pct":2.7},"Belgium":{"total":160,"pct":4.5},"Bulgaria":{"total":0,"pct":0.0},"Croatia":{"total":0,"pct":0.0},"Cyprus":{"total":10,"pct":0.3},"Czechia":{"total":20,"pct":0.6},"Denmark":{"total":10,"pct":0.3},"Estonia":{"total":0,"pct":0.0},"Finland":{"total":135,"pct":3.8},"France":{"total":1065,"pct":30.0},"Germany":{"total":885,"pct":24.9},"Greece":{"total":0,"pct":0.0},"Hungary":{"total":0,"pct":0.0},"Ireland":{"total":0,"pct":0.0},"Italy":{"total":20,"pct":0.6},"Latvia":{"total":0,"pct":0.0},"Lithuania":{"total":40,"pct":1.1},"Luxembourg":{"total":0,"pct":0.0},"Malta":{"total":0,"pct":0.0},"Netherlands":{"total":195,"pct":5.5},"Poland":{"total":515,"pct":14.5},"Portugal":{"total":0,"pct":0.0},"Romania":{"total":0,"pct":0.0},"Slovakia":{"total":0,"pct":0.0},"Slovenia":{"total":0,"pct":0.0},"Spain":{"total":260,"pct":7.3},"Sweden":{"total":145,"pct":4.1}},
    2020: {"Austria":{"total":70,"pct":4.0},"Belgium":{"total":80,"pct":4.6},"Bulgaria":{"total":0,"pct":0.0},"Croatia":{"total":0,"pct":0.0},"Cyprus":{"total":0,"pct":0.0},"Czechia":{"total":5,"pct":0.3},"Denmark":{"total":10,"pct":0.6},"Estonia":{"total":0,"pct":0.0},"Finland":{"total":60,"pct":3.4},"France":{"total":500,"pct":28.5},"Germany":{"total":480,"pct":27.4},"Greece":{"total":0,"pct":0.0},"Hungary":{"total":0,"pct":0.0},"Ireland":{"total":0,"pct":0.0},"Italy":{"total":5,"pct":0.3},"Latvia":{"total":0,"pct":0.0},"Lithuania":{"total":0,"pct":0.0},"Luxembourg":{"total":0,"pct":0.0},"Malta":{"total":0,"pct":0.0},"Netherlands":{"total":120,"pct":6.8},"Poland":{"total":210,"pct":12.0},"Portugal":{"total":0,"pct":0.0},"Romania":{"total":0,"pct":0.0},"Slovakia":{"total":0,"pct":0.0},"Slovenia":{"total":0,"pct":0.0},"Spain":{"total":145,"pct":8.3},"Sweden":{"total":70,"pct":4.0}},
    2021: {"Austria":{"total":125,"pct":6.1},"Belgium":{"total":125,"pct":6.1},"Bulgaria":{"total":10,"pct":0.5},"Croatia":{"total":0,"pct":0.0},"Cyprus":{"total":0,"pct":0.0},"Czechia":{"total":0,"pct":0.0},"Denmark":{"total":0,"pct":0.0},"Estonia":{"total":0,"pct":0.0},"Finland":{"total":55,"pct":2.7},"France":{"total":465,"pct":22.5},"Germany":{"total":605,"pct":29.3},"Greece":{"total":0,"pct":0.0},"Hungary":{"total":0,"pct":0.0},"Ireland":{"total":0,"pct":0.0},"Italy":{"total":10,"pct":0.5},"Latvia":{"total":0,"pct":0.0},"Lithuania":{"total":40,"pct":1.9},"Luxembourg":{"total":0,"pct":0.0},"Malta":{"total":0,"pct":0.0},"Netherlands":{"total":160,"pct":7.7},"Poland":{"total":215,"pct":10.4},"Portugal":{"total":0,"pct":0.0},"Romania":{"total":0,"pct":0.0},"Slovakia":{"total":0,"pct":0.0},"Slovenia":{"total":0,"pct":0.0},"Spain":{"total":95,"pct":4.6},"Sweden":{"total":160,"pct":7.7}},
    2022: {"Austria":{"total":490,"pct":6.4},"Belgium":{"total":375,"pct":4.9},"Bulgaria":{"total":60,"pct":0.8},"Croatia":{"total":230,"pct":3.0},"Cyprus":{"total":0,"pct":0.0},"Czechia":{"total":95,"pct":1.2},"Denmark":{"total":50,"pct":0.7},"Estonia":{"total":80,"pct":1.0},"Finland":{"total":595,"pct":7.8},"France":{"total":1450,"pct":19.0},"Germany":{"total":1625,"pct":21.3},"Greece":{"total":20,"pct":0.3},"Hungary":{"total":0,"pct":0.0},"Ireland":{"total":10,"pct":0.1},"Italy":{"total":295,"pct":3.9},"Latvia":{"total":50,"pct":0.7},"Lithuania":{"total":80,"pct":1.0},"Luxembourg":{"total":0,"pct":0.0},"Malta":{"total":0,"pct":0.0},"Netherlands":{"total":525,"pct":6.9},"Poland":{"total":725,"pct":9.5},"Portugal":{"total":10,"pct":0.1},"Romania":{"total":20,"pct":0.3},"Slovakia":{"total":0,"pct":0.0},"Slovenia":{"total":75,"pct":1.0},"Spain":{"total":310,"pct":4.1},"Sweden":{"total":460,"pct":6.0}},
    2023: {"Austria":{"total":590,"pct":5.3},"Belgium":{"total":550,"pct":4.9},"Bulgaria":{"total":60,"pct":0.5},"Croatia":{"total":410,"pct":3.7},"Cyprus":{"total":0,"pct":0.0},"Czechia":{"total":105,"pct":0.9},"Denmark":{"total":80,"pct":0.7},"Estonia":{"total":30,"pct":0.3},"Finland":{"total":240,"pct":2.1},"France":{"total":2310,"pct":20.6},"Germany":{"total":4550,"pct":40.5},"Greece":{"total":30,"pct":0.3},"Hungary":{"total":0,"pct":0.0},"Ireland":{"total":10,"pct":0.1},"Italy":{"total":280,"pct":2.5},"Latvia":{"total":10,"pct":0.1},"Lithuania":{"total":20,"pct":0.2},"Luxembourg":{"total":0,"pct":0.0},"Malta":{"total":0,"pct":0.0},"Netherlands":{"total":295,"pct":2.6},"Poland":{"total":625,"pct":5.6},"Portugal":{"total":10,"pct":0.1},"Romania":{"total":0,"pct":0.0},"Slovakia":{"total":0,"pct":0.0},"Slovenia":{"total":70,"pct":0.6},"Spain":{"total":810,"pct":7.2},"Sweden":{"total":145,"pct":1.3}},
    2024: {"Austria":{"total":265,"pct":4.8},"Belgium":{"total":195,"pct":3.5},"Bulgaria":{"total":0,"pct":0.0},"Croatia":{"total":215,"pct":3.9},"Cyprus":{"total":0,"pct":0.0},"Czechia":{"total":55,"pct":1.0},"Denmark":{"total":5,"pct":0.1},"Estonia":{"total":0,"pct":0.0},"Finland":{"total":65,"pct":1.2},"France":{"total":1095,"pct":19.9},"Germany":{"total":2290,"pct":41.5},"Greece":{"total":30,"pct":0.5},"Hungary":{"total":0,"pct":0.0},"Ireland":{"total":0,"pct":0.0},"Italy":{"total":180,"pct":3.3},"Latvia":{"total":10,"pct":0.2},"Lithuania":{"total":0,"pct":0.0},"Luxembourg":{"total":0,"pct":0.0},"Malta":{"total":0,"pct":0.0},"Netherlands":{"total":180,"pct":3.3},"Poland":{"total":395,"pct":7.2},"Portugal":{"total":0,"pct":0.0},"Romania":{"total":0,"pct":0.0},"Slovakia":{"total":0,"pct":0.0},"Slovenia":{"total":10,"pct":0.2},"Spain":{"total":445,"pct":8.1},"Sweden":{"total":80,"pct":1.5}},
    2025: {"Austria":{"total":195,"pct":4.5},"Belgium":{"total":300,"pct":7.0},"Bulgaria":{"total":0,"pct":0.0},"Croatia":{"total":110,"pct":2.6},"Cyprus":{"total":0,"pct":0.0},"Czechia":{"total":60,"pct":1.4},"Denmark":{"total":20,"pct":0.5},"Estonia":{"total":0,"pct":0.0},"Finland":{"total":70,"pct":1.6},"France":{"total":1050,"pct":24.5},"Germany":{"total":1475,"pct":34.4},"Greece":{"total":15,"pct":0.3},"Hungary":{"total":0,"pct":0.0},"Ireland":{"total":0,"pct":0.0},"Italy":{"total":130,"pct":3.0},"Latvia":{"total":0,"pct":0.0},"Lithuania":{"total":0,"pct":0.0},"Luxembourg":{"total":0,"pct":0.0},"Malta":{"total":0,"pct":0.0},"Netherlands":{"total":150,"pct":3.5},"Poland":{"total":205,"pct":4.8},"Portugal":{"total":30,"pct":0.7},"Romania":{"total":0,"pct":0.0},"Slovakia":{"total":0,"pct":0.0},"Slovenia":{"total":0,"pct":0.0},"Spain":{"total":460,"pct":10.7},"Sweden":{"total":20,"pct":0.5}},
}

PERMITS_BY_YEAR = {
    2017: {"Austria":{"total":271,"pct":4.1},"Belgium":{"total":68,"pct":1.0},"Bulgaria":{"total":59,"pct":0.9},"Croatia":{"total":13,"pct":0.2},"Cyprus":{"total":355,"pct":5.4},"Czechia":{"total":596,"pct":9.0},"Denmark":{"total":40,"pct":0.6},"Estonia":{"total":84,"pct":1.3},"Finland":{"total":298,"pct":4.5},"France":{"total":694,"pct":10.5},"Germany":{"total":710,"pct":10.7},"Greece":{"total":28,"pct":0.4},"Hungary":{"total":94,"pct":1.4},"Ireland":{"total":57,"pct":0.9},"Italy":{"total":59,"pct":0.9},"Latvia":{"total":52,"pct":0.8},"Lithuania":{"total":116,"pct":1.8},"Luxembourg":{"total":14,"pct":0.2},"Malta":{"total":1,"pct":0.0},"Netherlands":{"total":254,"pct":3.8},"Poland":{"total":868,"pct":13.1},"Portugal":{"total":37,"pct":0.6},"Romania":{"total":10,"pct":0.2},"Slovakia":{"total":7,"pct":0.1},"Slovenia":{"total":26,"pct":0.4},"Spain":{"total":510,"pct":7.7},"Sweden":{"total":95,"pct":1.4}},
    2018: {"Austria":{"total":272,"pct":3.8},"Belgium":{"total":72,"pct":1.0},"Bulgaria":{"total":69,"pct":1.0},"Croatia":{"total":14,"pct":0.2},"Cyprus":{"total":481,"pct":6.8},"Czechia":{"total":706,"pct":10.0},"Denmark":{"total":47,"pct":0.7},"Estonia":{"total":84,"pct":1.2},"Finland":{"total":340,"pct":4.8},"France":{"total":742,"pct":10.5},"Germany":{"total":730,"pct":10.3},"Greece":{"total":38,"pct":0.5},"Hungary":{"total":112,"pct":1.6},"Ireland":{"total":63,"pct":0.9},"Italy":{"total":83,"pct":1.2},"Latvia":{"total":54,"pct":0.8},"Lithuania":{"total":131,"pct":1.9},"Luxembourg":{"total":20,"pct":0.3},"Malta":{"total":1,"pct":0.0},"Netherlands":{"total":290,"pct":4.1},"Poland":{"total":988,"pct":14.0},"Portugal":{"total":49,"pct":0.7},"Romania":{"total":12,"pct":0.2},"Slovakia":{"total":9,"pct":0.1},"Slovenia":{"total":33,"pct":0.5},"Spain":{"total":541,"pct":7.7},"Sweden":{"total":123,"pct":1.7}},
    2019: {"Austria":{"total":254,"pct":3.5},"Belgium":{"total":73,"pct":1.0},"Bulgaria":{"total":89,"pct":1.2},"Croatia":{"total":21,"pct":0.3},"Cyprus":{"total":521,"pct":7.2},"Czechia":{"total":709,"pct":9.8},"Denmark":{"total":52,"pct":0.7},"Estonia":{"total":94,"pct":1.3},"Finland":{"total":370,"pct":5.1},"France":{"total":777,"pct":10.7},"Germany":{"total":748,"pct":10.3},"Greece":{"total":49,"pct":0.7},"Hungary":{"total":154,"pct":2.1},"Ireland":{"total":80,"pct":1.1},"Italy":{"total":97,"pct":1.3},"Latvia":{"total":65,"pct":0.9},"Lithuania":{"total":152,"pct":2.1},"Luxembourg":{"total":24,"pct":0.3},"Malta":{"total":2,"pct":0.0},"Netherlands":{"total":320,"pct":4.4},"Poland":{"total":953,"pct":13.2},"Portugal":{"total":65,"pct":0.9},"Romania":{"total":18,"pct":0.2},"Slovakia":{"total":12,"pct":0.2},"Slovenia":{"total":42,"pct":0.6},"Spain":{"total":625,"pct":8.6},"Sweden":{"total":107,"pct":1.5}},
    2020: {"Austria":{"total":179,"pct":3.3},"Belgium":{"total":49,"pct":0.9},"Bulgaria":{"total":68,"pct":1.3},"Croatia":{"total":17,"pct":0.3},"Cyprus":{"total":362,"pct":6.7},"Czechia":{"total":469,"pct":8.7},"Denmark":{"total":33,"pct":0.6},"Estonia":{"total":61,"pct":1.1},"Finland":{"total":238,"pct":4.4},"France":{"total":529,"pct":9.8},"Germany":{"total":554,"pct":10.3},"Greece":{"total":35,"pct":0.6},"Hungary":{"total":98,"pct":1.8},"Ireland":{"total":44,"pct":0.8},"Italy":{"total":69,"pct":1.3},"Latvia":{"total":41,"pct":0.8},"Lithuania":{"total":89,"pct":1.7},"Luxembourg":{"total":15,"pct":0.3},"Malta":{"total":1,"pct":0.0},"Netherlands":{"total":203,"pct":3.8},"Poland":{"total":711,"pct":13.2},"Portugal":{"total":50,"pct":0.9},"Romania":{"total":11,"pct":0.2},"Slovakia":{"total":8,"pct":0.1},"Slovenia":{"total":27,"pct":0.5},"Spain":{"total":450,"pct":8.3},"Sweden":{"total":74,"pct":1.4}},
    2021: {"Austria":{"total":199,"pct":3.2},"Belgium":{"total":59,"pct":1.0},"Bulgaria":{"total":82,"pct":1.3},"Croatia":{"total":20,"pct":0.3},"Cyprus":{"total":452,"pct":7.3},"Czechia":{"total":608,"pct":9.8},"Denmark":{"total":43,"pct":0.7},"Estonia":{"total":74,"pct":1.2},"Finland":{"total":272,"pct":4.4},"France":{"total":611,"pct":9.8},"Germany":{"total":617,"pct":9.9},"Greece":{"total":43,"pct":0.7},"Hungary":{"total":137,"pct":2.2},"Ireland":{"total":60,"pct":1.0},"Italy":{"total":91,"pct":1.5},"Latvia":{"total":48,"pct":0.8},"Lithuania":{"total":117,"pct":1.9},"Luxembourg":{"total":18,"pct":0.3},"Malta":{"total":2,"pct":0.0},"Netherlands":{"total":257,"pct":4.1},"Poland":{"total":870,"pct":14.0},"Portugal":{"total":65,"pct":1.0},"Romania":{"total":13,"pct":0.2},"Slovakia":{"total":10,"pct":0.2},"Slovenia":{"total":38,"pct":0.6},"Spain":{"total":560,"pct":9.0},"Sweden":{"total":100,"pct":1.6}},
    2022: {"Austria":{"total":372,"pct":2.9},"Belgium":{"total":81,"pct":0.6},"Bulgaria":{"total":224,"pct":1.7},"Croatia":{"total":70,"pct":0.5},"Cyprus":{"total":1748,"pct":13.6},"Czechia":{"total":592,"pct":4.6},"Denmark":{"total":94,"pct":0.7},"Estonia":{"total":97,"pct":0.8},"Finland":{"total":712,"pct":5.5},"France":{"total":1135,"pct":8.8},"Germany":{"total":2091,"pct":16.2},"Greece":{"total":151,"pct":1.2},"Hungary":{"total":441,"pct":3.4},"Ireland":{"total":153,"pct":1.2},"Italy":{"total":272,"pct":2.1},"Latvia":{"total":89,"pct":0.7},"Lithuania":{"total":620,"pct":4.8},"Luxembourg":{"total":39,"pct":0.3},"Malta":{"total":6,"pct":0.0},"Netherlands":{"total":936,"pct":7.3},"Poland":{"total":1584,"pct":12.3},"Portugal":{"total":92,"pct":0.7},"Romania":{"total":16,"pct":0.1},"Slovakia":{"total":14,"pct":0.1},"Slovenia":{"total":73,"pct":0.6},"Spain":{"total":988,"pct":7.7},"Sweden":{"total":221,"pct":1.7}},
    2023: {"Austria":{"total":389,"pct":3.2},"Belgium":{"total":103,"pct":0.8},"Bulgaria":{"total":247,"pct":2.0},"Croatia":{"total":80,"pct":0.7},"Cyprus":{"total":810,"pct":6.6},"Czechia":{"total":1753,"pct":14.3},"Denmark":{"total":93,"pct":0.8},"Estonia":{"total":152,"pct":1.2},"Finland":{"total":601,"pct":4.9},"France":{"total":1183,"pct":9.7},"Germany":{"total":1801,"pct":14.7},"Greece":{"total":94,"pct":0.8},"Hungary":{"total":383,"pct":3.1},"Ireland":{"total":167,"pct":1.4},"Italy":{"total":368,"pct":3.0},"Latvia":{"total":109,"pct":0.9},"Lithuania":{"total":244,"pct":2.0},"Luxembourg":{"total":56,"pct":0.5},"Malta":{"total":5,"pct":0.0},"Netherlands":{"total":637,"pct":5.2},"Poland":{"total":2001,"pct":16.3},"Portugal":{"total":194,"pct":1.6},"Romania":{"total":40,"pct":0.3},"Slovakia":{"total":31,"pct":0.3},"Slovenia":{"total":115,"pct":0.9},"Spain":{"total":1166,"pct":9.5},"Sweden":{"total":192,"pct":1.6}},
    2024: {"Austria":{"total":320,"pct":2.8},"Belgium":{"total":107,"pct":0.9},"Bulgaria":{"total":188,"pct":1.6},"Croatia":{"total":83,"pct":0.7},"Cyprus":{"total":522,"pct":4.5},"Czechia":{"total":1708,"pct":14.8},"Denmark":{"total":108,"pct":0.9},"Estonia":{"total":137,"pct":1.2},"Finland":{"total":475,"pct":4.1},"France":{"total":1131,"pct":9.8},"Germany":{"total":1363,"pct":11.8},"Greece":{"total":55,"pct":0.5},"Hungary":{"total":522,"pct":4.5},"Ireland":{"total":173,"pct":1.5},"Italy":{"total":465,"pct":4.0},"Latvia":{"total":116,"pct":1.0},"Lithuania":{"total":238,"pct":2.1},"Luxembourg":{"total":79,"pct":0.7},"Malta":{"total":4,"pct":0.0},"Netherlands":{"total":536,"pct":4.6},"Poland":{"total":1656,"pct":14.3},"Portugal":{"total":270,"pct":2.3},"Romania":{"total":42,"pct":0.4},"Slovakia":{"total":25,"pct":0.2},"Slovenia":{"total":148,"pct":1.3},"Spain":{"total":960,"pct":8.3},"Sweden":{"total":202,"pct":1.7}},
}

COUNTRY_COORDS = {
    "Germany":     (10.4, 51.2), "France":      ( 2.3, 46.2),
    "Poland":      (19.1, 51.9), "Spain":       (-3.7, 40.4),
    "Austria":     (14.5, 47.5), "Belgium":     ( 4.5, 50.5),
    "Netherlands": ( 5.3, 52.1), "Finland":     (25.7, 61.9),
    "Sweden":      (18.6, 59.3), "Italy":       (12.6, 41.9),
    "Croatia":     (15.2, 45.1), "Czechia":     (15.5, 49.8),
    "Denmark":     ( 9.5, 56.3), "Lithuania":   (23.9, 55.2),
    "Slovenia":    (14.9, 46.1), "Bulgaria":    (25.5, 42.7),
    "Estonia":     (24.7, 58.6), "Greece":      (21.8, 39.1),
    "Latvia":      (24.6, 56.9), "Portugal":    (-8.2, 39.4),
    "Romania":     (24.9, 45.9), "Ireland":     (-8.2, 53.4),
    "Cyprus":      (33.4, 35.1), "Malta":       (14.4, 35.9),
    "Luxembourg":  ( 6.1, 49.8), "Hungary":     (19.5, 47.2),
    "Slovakia":    (19.7, 48.7),
}

ISO_MAP = {
    "Germany":"DEU","France":"FRA","Poland":"POL","Spain":"ESP",
    "Austria":"AUT","Belgium":"BEL","Netherlands":"NLD","Finland":"FIN",
    "Sweden":"SWE","Italy":"ITA","Croatia":"HRV","Czechia":"CZE",
    "Denmark":"DNK","Lithuania":"LTU","Slovenia":"SVN","Bulgaria":"BGR",
    "Estonia":"EST","Greece":"GRC","Latvia":"LVA","Portugal":"PRT",
    "Romania":"ROU","Ireland":"IRL","Cyprus":"CYP","Malta":"MLT",
    "Luxembourg":"LUX","Hungary":"HUN","Slovakia":"SVK",
    "Kosovo":"XKX","Montenegro":"MNE","Russia":"RUS",
}

RUSSIA_COORD = (37.6, 55.7)

# Light to dark red scale — low values transparent/light, high values deep red
RED_SCALE = [
    [0.00, "rgba(232,0,13,0.05)"],
    [0.12, "rgba(232,0,13,0.15)"],
    [0.25, "rgba(232,0,13,0.30)"],
    [0.40, "rgba(232,0,13,0.50)"],
    [0.55, "rgba(232,0,13,0.65)"],
    [0.70, "rgba(232,0,13,0.80)"],
    [0.85, "rgba(232,0,13,0.92)"],
    [1.00, "rgba(232,0,13,1.00)"],
]


def build_map(mode, year):
    data       = ASYLUM_BY_YEAR[year]   if mode == "Asylum" else PERMITS_BY_YEAR[year]
    label      = "asylum applications"  if mode == "Asylum" else "residence permit applications"
    global_max = ASYLUM_GLOBAL_MAX      if mode == "Asylum" else PERMITS_GLOBAL_MAX
    max_val    = max((d["total"] for d in data.values()), default=1) or 1

    countries   = list(data.keys())
    iso_codes   = [ISO_MAP[c] for c in countries]
    pct_values  = [data[c]["pct"] for c in countries]
    hover_texts = [
        f"<b>{c}</b><br>{data[c]['pct']}% of total<br>{data[c]['total']:,} {label} ({year})"
        for c in countries
    ]

    fig = go.Figure()

    # EU choropleth
    fig.add_trace(go.Choropleth(
        locations=iso_codes, z=pct_values, locationmode="ISO-3",
        colorscale=RED_SCALE, zmin=0, zmax=global_max, showscale=True,
        colorbar=dict(
            title=dict(text="% of total", font=dict(color="#ffffff", family="Inter", size=11)),
            tickfont=dict(color="#ffffff", family="Inter", size=10),
            bgcolor="rgba(0,0,0,0)", bordercolor="#333333",
            thickness=12, len=0.35, x=1.01,
        ),
        text=hover_texts, hovertemplate="%{text}<extra></extra>",
        marker_line_color="rgba(80,80,80,0.6)",
        marker_line_width=0.5,
    ))

    # Russia
    fig.add_trace(go.Choropleth(
        locations=["RUS"], z=[1], locationmode="ISO-3",
        colorscale=[[0, "rgba(0,87,231,0.7)"], [1, "rgba(0,87,231,0.7)"]],
        showscale=False,
        hovertemplate="<b>Russia</b><br>Origin country<extra></extra>",
        marker_line_color="rgba(80,80,80,0.6)",
        marker_line_width=0.5,
    ))

    # Kosovo + Montenegro
    fig.add_trace(go.Choropleth(
        locations=["XKX", "MNE"], z=[0, 0], locationmode="ISO-3",
        colorscale=[[0, "rgba(40,40,40,0.5)"], [1, "rgba(40,40,40,0.5)"]],
        showscale=False,
        hovertemplate="<b>%{location}</b><br>No data<extra></extra>",
        marker_line_color="rgba(100,100,100,0.7)",
        marker_line_width=0.8,
    ))

    # Route lines
    for country, coord in COUNTRY_COORDS.items():
        if country not in data or data[country]["total"] == 0:
            continue
        total = data[country]["total"]
        pct   = data[country]["pct"]
        width = max(0.4, (total / max_val) * 4)
        alpha = max(0.08, min(0.75, total / max_val))
        fig.add_trace(go.Scattergeo(
            lon=[RUSSIA_COORD[0], coord[0]], lat=[RUSSIA_COORD[1], coord[1]],
            mode="lines",
            line=dict(width=width, color=f"rgba(232,0,13,{alpha:.2f})"),
            hovertemplate=f"<b>Russia → {country}</b><br>{pct}% of total<br>{total:,} {label} ({year})<extra></extra>",
            showlegend=False,
        ))

    # Country dots
    active = [c for c in countries if c in COUNTRY_COORDS and data[c]["total"] > 0]
    fig.add_trace(go.Scattergeo(
        lon=[COUNTRY_COORDS[c][0] for c in active],
        lat=[COUNTRY_COORDS[c][1] for c in active],
        mode="markers",
        marker=dict(
            size=[max(4, (data[c]["total"] / max_val) * 14) for c in active],
            color="rgba(232,0,13,0.8)",
            line=dict(color="rgba(255,255,255,0.5)", width=0.5),
        ),
        text=[f"<b>{c}</b><br>{data[c]['pct']}% of total<br>{data[c]['total']:,} {label} ({year})" for c in active],
        hovertemplate="%{text}<extra></extra>",
        showlegend=False,
    ))

    # Russia dot
    fig.add_trace(go.Scattergeo(
        lon=[RUSSIA_COORD[0]], lat=[RUSSIA_COORD[1]],
        mode="markers+text",
        marker=dict(size=10, color="rgba(0,87,231,0.9)", line=dict(color="rgba(255,255,255,0.6)", width=1)),
        text=["Russia"], textposition="bottom center",
        textfont=dict(color="#aaaaaa", size=9, family="Inter"),
        hovertemplate="<b>Russia</b><br>Origin country<extra></extra>",
        showlegend=False,
    ))

    fig.update_layout(
        paper_bgcolor="#000000",
        geo=dict(
            showframe=False,
            showcoastlines=False,
            showland=True, landcolor="#0a0a0a",
            showocean=True, oceancolor="#000000",
            showlakes=False, showrivers=False,
            showcountries=True, countrycolor="rgba(60,60,60,0.5)",
            bgcolor="#000000",
            projection_type="natural earth",
            lonaxis_range=[-25, 80],
            lataxis_range=[25, 75],
        ),
        margin=dict(t=0, b=0, l=0, r=0),
        height=470,
        hoverlabel=dict(
            align="left", bgcolor="#1a1a1a",
            font=dict(color="#ffffff", size=12, family="Inter"),
            bordercolor="#333333",
        ),
    )
    return fig


# ── Streamlit UI ───────────────────────────────────────────────────────────

st.markdown("---")
st.markdown("### Migration routes of Russian men to the EU")
st.markdown(
    "<p style='font-size:13px;color:#888888;margin:-8px 0 10px;'>"
    "Hover over a country to see the share of applications. "
    "Use the slider to explore changes by year.</p>",
    unsafe_allow_html=True,
)

st.markdown("""
<style>
    div[data-testid="stRadio"] label { color: #aaaaaa !important; font-family: 'Inter', sans-serif !important; font-size: 12px !important; }
    div[data-testid="stSlider"] p { color: #aaaaaa !important; font-size: 11px !important; }
    div[data-testid="stSlider"] div[data-testid="stMarkdownContainer"] p { color: #aaaaaa !important; }
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 3])
with col1:
    mode = st.radio(
        "", ["Asylum", "Residence Permits"],
        horizontal=False, label_visibility="collapsed",
        key="map_mode",
    )
with col2:
    years = list(range(2017, 2026)) if mode == "Asylum" else list(range(2017, 2025))
    selected_year = st.select_slider(
        "", options=years, value=years[0], format_func=str,
        key="map_year_slider",
    )

# Top 5 — no bold stars
data_sel  = ASYLUM_BY_YEAR[selected_year] if mode == "Asylum" else PERMITS_BY_YEAR[selected_year]
top5      = sorted(data_sel.items(), key=lambda x: x[1]["total"], reverse=True)[:5]
top5_text = "  ·  ".join([f"{c} {d['pct']}%" for c, d in top5])
st.markdown(
    f"<p style='font-size:11px;color:#666666;margin:2px 0 4px;'>Top destinations {selected_year}: {top5_text}</p>",
    unsafe_allow_html=True,
)

fig = build_map(mode, selected_year)
st.plotly_chart(fig, width="stretch")

label_cap = "asylum applications (first-time, men aged 18–34)" if mode == "Asylum" else "residence permit applications (men aged 18–29)"
st.markdown(
    f"<p style='font-size:10px;color:#444444;margin:2px 0;'>Source: Eurostat · {label_cap} · Color scale fixed across all years.</p>",
    unsafe_allow_html=True,
)