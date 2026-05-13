import streamlit as st
import plotly.express as px
import pandas as pd
import requests
import unicodedata

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="Chequea360",
    page_icon="favicon.png",
    layout="wide"
)

# =========================================================
# HELPERS
# =========================================================

def clean_text(text):
    text = text.lower().strip()
    text = unicodedata.normalize("NFD", text)
    return "".join(
        c for c in text
        if unicodedata.category(c) != "Mn"
    )

@st.cache_data(ttl=3600)
def fetch_worldbank_data(country_code, indicator_code):

    url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/{indicator_code}"

    params = {
        "format": "json",
        "per_page": 100
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=20
        )

        data = response.json()

        if not isinstance(data, list) or len(data) < 2:
            return pd.DataFrame()

        rows = []

        for item in data[1]:

            if item.get("value") is not None:

                rows.append({
                    "year": int(item.get("date")),
                    "value": float(item.get("value"))
                })

        df = pd.DataFrame(rows)

        if df.empty:
            return df

        return df.sort_values("year")

    except:
        return pd.DataFrame()

@st.cache_data(ttl=86400)
def fetch_worldbank_countries():

    url = "https://api.worldbank.org/v2/country"

    params = {
        "format": "json",
        "per_page": 400
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=20
        )

        data = response.json()

        if not isinstance(data, list) or len(data) < 2:
            return []

        countries = []

        for item in data[1]:

            region = item.get(
                "region",
                {}
            ).get("value", "")

            if region and region != "Aggregates":

                countries.append({
                    "name": item.get("name"),
                    "code": item.get("id")
                })

        return countries

    except:
        return []

@st.cache_data(ttl=3600)
def fetch_global_ranking(indicator_code):

    countries = fetch_worldbank_countries()
    rows = []

    for country in countries:

        df = fetch_worldbank_data(
            country["code"],
            indicator_code
        )

        if not df.empty:

            latest = df.iloc[-1]

            try:

                value = float(latest["value"])

                rows.append({
                    "country": country["name"],
                    "code": country["code"],
                    "year": int(latest["year"]),
                    "value": value
                })

            except:
                pass

    ranking_df = pd.DataFrame(rows)

    if ranking_df.empty:
        return ranking_df

    ranking_df = ranking_df.sort_values(
        "value",
        ascending=False
    )

    ranking_df.insert(
        0,
        "rank",
        range(1, len(ranking_df) + 1)
    )

    return ranking_df

def get_country_aliases():

    aliases = {}

    for country in fetch_worldbank_countries():

        official_name = country["name"]

        cleaned_name = clean_text(
            official_name
        )

        aliases[cleaned_name] = {
            "name": official_name,
            "code": country["code"]
        }

    manual_aliases = {

        "alemania": ("Germany", "DEU"),
        "germany": ("Germany", "DEU"),

        "suecia": ("Sweden", "SWE"),
        "sweden": ("Sweden", "SWE"),

        "inglaterra": ("United Kingdom", "GBR"),
        "reino unido": ("United Kingdom", "GBR"),
        "uk": ("United Kingdom", "GBR"),

        "estados unidos": ("United States", "USA"),
        "eeuu": ("United States", "USA"),
        "usa": ("United States", "USA"),

        "francia": ("France", "FRA"),
        "france": ("France", "FRA"),

        "espana": ("Spain", "ESP"),
        "spain": ("Spain", "ESP"),

        "italia": ("Italy", "ITA"),
        "italy": ("Italy", "ITA"),

        "portugal": ("Portugal", "PRT"),

        "japon": ("Japan", "JPN"),
        "japan": ("Japan", "JPN"),

        "china": ("China", "CHN"),
        "india": ("India", "IND"),

        "corea del sur": ("Korea, Rep.", "KOR"),
        "south korea": ("Korea, Rep.", "KOR"),

        "mexico": ("Mexico", "MEX"),
        "brasil": ("Brazil", "BRA"),
        "brazil": ("Brazil", "BRA"),

        "ecuador": ("Ecuador", "ECU"),
        "colombia": ("Colombia", "COL"),
        "argentina": ("Argentina", "ARG"),
        "peru": ("Peru", "PER"),
        "chile": ("Chile", "CHL"),

        "haiti": ("Haiti", "HTI"),
        "canada": ("Canada", "CAN"),

        "australia": ("Australia", "AUS"),

        "sudafrica": ("South Africa", "ZAF"),
        "south africa": ("South Africa", "ZAF")
    }

    for alias, data in manual_aliases.items():

        aliases[alias] = {
            "name": data[0],
            "code": data[1]
        }

    return aliases

# =========================================================
# DESIGN
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #FAF7F2;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

.header-box {
    background: linear-gradient(135deg, #142B6F 0%, #1D3F95 100%);
    padding: 1.6rem;
    border-radius: 24px;
    color: white;
    margin-bottom: 1.2rem;
    box-shadow: 0 8px 24px rgba(20,43,111,0.18);
}

.header-title {
    font-size: 3rem;
    font-weight: 900;
    color: #F6A300;
}

.header-subtitle {
    font-size: 1rem;
    margin-top: 0.6rem;
    line-height: 1.5;
}

.badge {
    display: inline-block;
    background-color: #F6A300;
    color: #142B6F;
    padding: 0.4rem 0.9rem;
    border-radius: 999px;
    font-weight: 800;
    font-size: 0.8rem;
    margin-top: 1rem;
}

.card {
    background: white;
    padding: 18px 22px;
    border-radius: 18px;
    box-shadow: 0 4px 16px rgba(20,43,111,0.08);
    margin-bottom: 1rem;
    line-height: 1.5;
}

.answer-card {
    background: white;
    border-left: 8px solid #F6A300;
    padding: 1.5rem;
    border-radius: 18px;
    box-shadow: 0 4px 16px rgba(20,43,111,0.08);
    margin-bottom: 1rem;
}

.trace-card {
    background: white;
    padding: 1.5rem;
    border-radius: 18px;
    box-shadow: 0 4px 16px rgba(20,43,111,0.08);
}

.small-muted {
    color: #555;
    font-size: 0.95rem;
}

.footer {
    text-align: center;
    color: #777;
    font-size: 0.8rem;
    padding-top: 2rem;
}

.stButton > button {
    background-color: #142B6F;
    color: white;
    border-radius: 12px;
    border: none;
    font-weight: 800;
    height: 50px;
}

.stButton > button:hover {
    background-color: #F6A300;
    color: #142B6F;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================

col_logo, col_text = st.columns([1, 3])

with col_logo:
    st.image("logo.png", width=260)

with col_text:

    header_html = (
        '<div class="header-box">'

        '<div class="header-title">Chequea360</div>'

        '<div class="header-subtitle">'

        'Chequea360 es una plataforma de inteligencia informativa que integra inteligencia artificial, '
        'la API Data360 del Banco Mundial, metodologías periodísticas de verificación de datos y procesos '
        'de capacitación y alfabetización en datos a través de ChequeaLab.<br><br>'

        'Su objetivo es permitir que periodistas, investigadores y ciudadanos '
        'puedan consultar, interpretar y validar datos de desarrollo en tiempo real.'

        '</div>'

        '<div class="badge">'
        '10 años chequeando · Periodismo con rigor · Datos verificables'
        '</div>'

        '</div>'
    )

    st.markdown(
        header_html,
        unsafe_allow_html=True
    )

# =========================================================
# INTRO
# =========================================================

st.markdown("""
<div class="card">

<p style="margin:0; font-size:1.05rem; font-weight:700; color:#1f1f1f;">
Consulta indicadores económicos y sociales oficiales.
</p>

<p style="margin-top:10px; margin-bottom:8px;" class="small-muted">
Chequea360 permite buscar, comparar e interpretar datos oficiales del Banco Mundial sobre PIB, crecimiento económico, inflación, desempleo, pobreza, desarrollo económico y social, así como comparaciones entre países, regiones y rankings globales.
</p>

<p style="margin:0;" class="small-muted">
<strong>Ejemplos:</strong> Alemania inflación · Suecia desempleo · ¿Cuál es el PIB de Japón? · Ranking mundial de inflación · Global ranking of unemployment
</p>

</div>
""", unsafe_allow_html=True)

# =========================================================
# INPUT
# =========================================================

question = st.text_input(
    "Pregunta",
    placeholder="Ejemplo: Alemania inflación",
    label_visibility="collapsed"
)

# =========================================================
# REGIONS
# =========================================================

REGIONS = {
    "america latina": [
        "Brazil",
        "Argentina",
        "Chile",
        "Colombia",
        "Ecuador",
        "Mexico",
        "Peru"
    ],

    "south america": [
        "Brazil",
        "Argentina",
        "Chile",
        "Colombia",
        "Ecuador",
        "Peru"
    ]
}

# =========================================================
# INDICATORS
# =========================================================

INDICATORS = {

    "desempleo": {
        "code": "SL.UEM.TOTL.ZS",
        "name": "Tasa de desempleo"
    },

    "unemployment": {
        "code": "SL.UEM.TOTL.ZS",
        "name": "Unemployment rate"
    },

    "inflacion": {
        "code": "FP.CPI.TOTL.ZG",
        "name": "Inflación"
    },

    "inflation": {
        "code": "FP.CPI.TOTL.ZG",
        "name": "Inflation"
    },

    "pobreza": {
        "code": "SI.POV.DDAY",
        "name": "Pobreza"
    },

    "poverty": {
        "code": "SI.POV.DDAY",
        "name": "Poverty"
    },

    "pib": {
        "code": "NY.GDP.MKTP.KD.ZG",
        "name": "Crecimiento del PIB"
    },

    "gdp": {
        "code": "NY.GDP.MKTP.KD.ZG",
        "name": "GDP growth"
    }
}

# =========================================================
# LANGUAGE
# =========================================================

def detect_language(q):

    english_words = [
        "what",
        "unemployment",
        "inflation",
        "poverty",
        "gdp"
    ]

    for word in english_words:

        if word in q:
            return "en"

    return "es"

def is_global_query(q):

    global_words = [
        "ranking mundial",
        "ranking global",
        "global ranking",
        "world ranking",
        "todos los paises",
        "all countries",
        "mundo"
    ]

    for word in global_words:

        if word in q:
            return True

    return False

# =========================================================
# LABELS
# =========================================================

def labels(lang):

    if lang == "en":

        return {
            "answer": "Answer",
            "source": "Source and traceability",
            "data": "View data",
            "year": "Year",
            "value": "Value"
        }

    return {
        "answer": "Respuesta",
        "source": "Fuente y trazabilidad",
        "data": "Ver datos",
        "year": "Año",
        "value": "Valor"
    }

# =========================================================
# BUTTON
# =========================================================

submitted = st.button(
    "📊 Consultar datos",
    use_container_width=True
)

# =========================================================
# QUERY
# =========================================================

if submitted:

    q_original = question.strip()
    q = clean_text(q_original)

    lang = detect_language(q)
    L = labels(lang)

    selected_indicator = None
    selected_countries = []

    global_query = is_global_query(q)

    country_aliases = get_country_aliases()

    for key, indicator in INDICATORS.items():

        if key in q:
            selected_indicator = indicator
            break

    if selected_indicator is None:

        st.error(
            "No pude identificar el indicador."
        )

    elif global_query:

        with st.spinner(
            "Construyendo ranking global..."
        ):

            ranking_df = fetch_global_ranking(
                selected_indicator["code"]
            )

        if ranking_df.empty:

            st.error(
                "No se encontraron datos."
            )

        else:

            st.markdown(f"""
            <div class="answer-card">
            <h3>Ranking global</h3>
            Ranking mundial construido con datos oficiales del Banco Mundial.
            </div>
            """, unsafe_allow_html=True)

            top_30 = (
                ranking_df
                .head(30)
                .sort_values(
                    "value",
                    ascending=True
                )
            )

            fig = px.bar(
                top_30,
                x="value",
                y="country",
                orientation="h",
                title=f"{selected_indicator['name']} · Top 30 países"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            col1, col2 = st.columns([1, 1])

            with col1:

                with st.expander(
                    L["data"]
                ):
                    st.dataframe(ranking_df)

            with col2:

                st.markdown(f"""
                <div class="trace-card">

                <h4>🔎 {L["source"]}</h4>

                <p>
                <strong>Fuente:</strong>
                Banco Mundial
                </p>

                <p>
                <strong>Indicador:</strong>
                {selected_indicator['name']}
                </p>

                <p>
                <strong>Código:</strong>
                {selected_indicator['code']}
                </p>

                </div>
                """, unsafe_allow_html=True)

    else:

        for alias, country_data in sorted(
            country_aliases.items(),
            key=lambda x: len(x[0]),
            reverse=True
        ):

            if alias in q:

                selected_countries.append(
                    country_data
                )

        if not selected_countries:

            st.error(
                "No pude identificar un país."
            )

        else:

            all_data = []

            for country in selected_countries:

                df = fetch_worldbank_data(
                    country["code"],
                    selected_indicator["code"]
                )

                if not df.empty:

                    df["country"] = country["name"]
                    all_data.append(df)

            if not all_data:

                st.error(
                    "No se encontraron datos."
                )

            else:

                final_df = pd.concat(
                    all_data,
                    ignore_index=True
                )

                latest_df = (
                    final_df
                    .sort_values("year")
                    .groupby("country")
                    .tail(1)
                )

                top = latest_df.iloc[0]

                answer = f"""
                Según datos del Banco Mundial,
                <strong>{selected_indicator['name']}</strong>
                en <strong>{top['country']}</strong>
                registró <strong>{round(top['value'], 2)}</strong>
                en <strong>{int(top['year'])}</strong>.
                """

                st.markdown(f"""
                <div class="answer-card">
                <h3>{L["answer"]}</h3>
                {answer}
                </div>
                """, unsafe_allow_html=True)

                fig = px.line(
                    final_df,
                    x="year",
                    y="value",
                    color="country",
                    markers=True,
                    title=selected_indicator["name"]
                )

                fig.update_layout(
                    xaxis_title=L["year"],
                    yaxis_title=L["value"],
                    height=550
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

                col1, col2 = st.columns([1, 1])

                with col1:

                    with st.expander(
                        L["data"]
                    ):
                        st.dataframe(final_df)

                with col2:

                    st.markdown(f"""
                    <div class="trace-card">

                    <h4>🔎 {L["source"]}</h4>

                    <p>
                    <strong>Fuente:</strong>
                    Banco Mundial
                    </p>

                    <p>
                    <strong>Indicador:</strong>
                    {selected_indicator['name']}
                    </p>

                    <p>
                    <strong>Código:</strong>
                    {selected_indicator['code']}
                    </p>

                    </div>
                    """, unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">
Chequea360 · Ecuador Chequea · ChequeaLab · Datos oficiales del Banco Mundial
</div>
""", unsafe_allow_html=True)