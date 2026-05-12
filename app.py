import streamlit as st
import plotly.express as px
from data360_client import fetch_worldbank_data

st.set_page_config(
    page_title="Chequea360",
    page_icon="🔎",
    layout="wide"
)

# ---------------------------------------------------
# ESTILOS ECUADOR CHEQUEA
# ---------------------------------------------------

st.markdown("""
<style>
.main {
    background-color: #FAF7F2;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1150px;
}

.header-box {
    background: linear-gradient(135deg, #142B6F 0%, #1C3F95 100%);
    padding: 2rem;
    border-radius: 20px;
    margin-bottom: 1.5rem;
    color: white;
    box-shadow: 0 8px 24px rgba(20, 43, 111, 0.18);
}

.header-title {
    font-size: 3rem;
    font-weight: 900;
    color: #F6A300;
    margin-bottom: 0.2rem;
}

.header-subtitle {
    font-size: 1.05rem;
    color: #ffffff;
    opacity: 0.95;
}

.badge {
    display: inline-block;
    background-color: #F6A300;
    color: #142B6F;
    padding: 0.35rem 0.8rem;
    border-radius: 999px;
    font-weight: 800;
    font-size: 0.78rem;
    margin-top: 1rem;
}

.card {
    background: white;
    padding: 1.4rem;
    border-radius: 16px;
    box-shadow: 0 4px 16px rgba(20, 43, 111, 0.08);
    margin-bottom: 1rem;
}

.answer-card {
    background: white;
    border-left: 7px solid #F6A300;
    padding: 1.4rem;
    border-radius: 14px;
    box-shadow: 0 4px 14px rgba(20, 43, 111, 0.08);
    margin-bottom: 1rem;
}

.trace-card {
    background: #ffffff;
    border: 1px solid #E8E2D8;
    padding: 1.2rem;
    border-radius: 14px;
    margin-top: 1rem;
}

.small-muted {
    color: #666;
    font-size: 0.9rem;
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
}

.stButton > button:hover {
    background-color: #F6A300;
    color: #142B6F;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# HEADER CON LOGO
# ---------------------------------------------------

col_logo, col_text = st.columns([1, 3])

with col_logo:
    st.image("logo.png", width=250)

with col_text:
    st.markdown("""
    <div class="header-box">
        <div class="header-title">Chequea360</div>
        <div class="header-subtitle">
            Plataforma de inteligencia informativa impulsada por Ecuador Chequea y ChequeaLab.
        </div>
        <div class="badge">
            10 años chequeando · Periodismo con rigor · Datos verificables
        </div>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------
# INTRO
# ---------------------------------------------------

st.markdown("""
<div class="card">
    <strong>Haz una pregunta en español, inglés o portugués.</strong><br>
    <span class="small-muted">
    Ejemplos: ¿Cuál es el desempleo en Ecuador? · What is poverty in India? · Qual é a inflação na Argentina?
    </span>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# INPUT
# ---------------------------------------------------

question = st.text_input(
    "Pregunta",
    placeholder="Ejemplo: ¿Cuál es el desempleo en Ecuador?",
    label_visibility="collapsed"
)

# ---------------------------------------------------
# PAÍSES
# ---------------------------------------------------

countries = {
    "ecuador": "ECU",
    "equador": "ECU",
    "colombia": "COL",
    "perú": "PER",
    "peru": "PER",
    "brasil": "BRA",
    "brazil": "BRA",
    "méxico": "MEX",
    "mexico": "MEX",
    "argentina": "ARG",
    "chile": "CHL",
    "venezuela": "VEN",
    "bolivia": "BOL",
    "paraguay": "PRY",
    "uruguay": "URY",
    "united states": "USA",
    "usa": "USA",
    "canada": "CAN",
    "japan": "JPN",
    "japón": "JPN",
    "germany": "DEU",
    "alemania": "DEU",
    "france": "FRA",
    "francia": "FRA",
    "spain": "ESP",
    "españa": "ESP",
    "india": "IND",
    "china": "CHN"
}

# ---------------------------------------------------
# INDICADORES
# ---------------------------------------------------

indicators = {
    "desempleo": {
        "code": "SL.UEM.TOTL.ZS",
        "name": "Tasa de desempleo"
    },
    "unemployment": {
        "code": "SL.UEM.TOTL.ZS",
        "name": "Unemployment rate"
    },
    "desemprego": {
        "code": "SL.UEM.TOTL.ZS",
        "name": "Taxa de desemprego"
    },
    "pobreza": {
        "code": "SI.POV.DDAY",
        "name": "Pobreza"
    },
    "poverty": {
        "code": "SI.POV.DDAY",
        "name": "Poverty"
    },
    "inflación": {
        "code": "FP.CPI.TOTL.ZG",
        "name": "Inflación"
    },
    "inflation": {
        "code": "FP.CPI.TOTL.ZG",
        "name": "Inflation"
    },
    "inflação": {
        "code": "FP.CPI.TOTL.ZG",
        "name": "Inflação"
    },
    "pib": {
        "code": "NY.GDP.MKTP.KD.ZG",
        "name": "Crecimiento del PIB"
    },
    "gdp": {
        "code": "NY.GDP.MKTP.KD.ZG",
        "name": "GDP growth"
    },
    "esperanza de vida": {
        "code": "SP.DYN.LE00.IN",
        "name": "Esperanza de vida"
    },
    "life expectancy": {
        "code": "SP.DYN.LE00.IN",
        "name": "Life expectancy"
    },
    "expectativa de vida": {
        "code": "SP.DYN.LE00.IN",
        "name": "Expectativa de vida"
    },
    "mortalidad infantil": {
        "code": "SP.DYN.IMRT.IN",
        "name": "Mortalidad infantil"
    },
    "infant mortality": {
        "code": "SP.DYN.IMRT.IN",
        "name": "Infant mortality"
    },
    "mortalidade infantil": {
        "code": "SP.DYN.IMRT.IN",
        "name": "Mortalidade infantil"
    }
}

# ---------------------------------------------------
# BOTÓN
# ---------------------------------------------------

submitted = st.button("🔎 Consultar datos", use_container_width=True)

if submitted:

    q = question.lower()

    selected_country = None
    selected_country_name = None
    selected_indicator = None

    for country_name, country_code in countries.items():
        if country_name in q:
            selected_country = country_code
            selected_country_name = country_name.title()

    for keyword, indicator in indicators.items():
        if keyword in q:
            selected_indicator = indicator

    if not question.strip():
        st.warning("Por favor escribe una pregunta.")

    elif selected_country is None:
        st.error("No pude identificar el país. Prueba con Ecuador, Colombia, Brasil, Argentina, India o Alemania.")

    elif selected_indicator is None:
        st.error("No pude identificar el indicador. Prueba con desempleo, pobreza, inflación, PIB o esperanza de vida.")

    else:
        with st.spinner("Consultando datos oficiales del Banco Mundial..."):
            df = fetch_worldbank_data(
                selected_country,
                selected_indicator["code"]
            )

        if df.empty:
            st.error("No se encontraron datos para esa consulta.")

        else:
            latest = df.iloc[-1]
            latest_year = int(latest["year"])
            latest_value = round(latest["value"], 2)

            st.markdown(f"""
            <div class="answer-card">
                <h3>Respuesta</h3>
                Según datos del Banco Mundial, el indicador
                <strong>{selected_indicator['name']}</strong>
                en <strong>{selected_country_name}</strong>
                registró un valor de
                <strong>{latest_value}</strong>
                en el año <strong>{latest_year}</strong>.
            </div>
            """, unsafe_allow_html=True)

            fig = px.line(
                df,
                x="year",
                y="value",
                markers=True,
                title=f"{selected_indicator['name']} · {selected_country_name}"
            )

            fig.update_layout(
                xaxis_title="Año",
                yaxis_title="Valor",
                height=460
            )

            st.plotly_chart(fig, use_container_width=True)

            col1, col2 = st.columns([1, 1])

            with col1:
                with st.expander("Ver datos"):
                    st.dataframe(df)

            with col2:
                st.markdown(f"""
                <div class="trace-card">
                    <h4>🔎 Fuente y trazabilidad</h4>
                    <p><strong>Fuente:</strong> Banco Mundial</p>
                    <p><strong>Indicador:</strong> {selected_indicator['name']}</p>
                    <p><strong>Código:</strong> {selected_indicator['code']}</p>
                    <p><strong>País:</strong> {selected_country_name}</p>
                    <p><a href="https://data.worldbank.org/" target="_blank">World Bank Open Data</a></p>
                </div>
                """, unsafe_allow_html=True)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("""
<div class="footer">
    Chequea360 · Ecuador Chequea · ChequeaLab · Datos oficiales del Banco Mundial
</div>
""", unsafe_allow_html=True)