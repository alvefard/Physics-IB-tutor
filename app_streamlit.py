
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from tutor_ib import tutor_ib_fisica
from ecuaciones_ib import ecuaciones_ib
from cliente_openai import preguntar_chatgpt


# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Tutor IB Física", layout="wide")

st.title("🚀 Plataforma IB de Física")
col1, col2 = st.columns([1, 3])

with col1:
st.image("logo-colegio-nueva-york.png", width=400)
with col2:
st.image("imagen2.png", width=400)

tabs = st.tabs(["🧠 Tutor", "📊 Graficador", "🎛️ Simulador", "🧪 Generador"])

st.markdown("""
<hr>
<p style='text-align: center; color: gray;'>
Desarrollado por <b>Jhon Jairo Galán Rincón</b> 🚀
</p>
""", unsafe_allow_html=True)
# =========================
# 🧠 TUTOR
# =========================
with tabs[0]:

    st.header("🧠 Tutor IB")

    pregunta = st.text_area("Escribe tu pregunta:")

    if st.button("Analizar"):
        if pregunta.strip():
            with st.spinner("Analizando..."):
                respuesta = tutor_ib_fisica(pregunta)
            st.write(respuesta)
        else:
            st.warning("Escribe una pregunta")


# =========================
# 📊 GRAFICADOR
# =========================
with tabs[1]:

    st.header("📊 Graficador IB")

    pregunta = st.text_input("Contexto (ej: movimiento con aceleración)")

    def obtener_ecuaciones(pregunta):
        resultados = []
        for tema, lista in ecuaciones_ib.items():
            for eq in lista:
                if eq["graficable"]:
                    for var in eq["variables"]:
                        if var.lower() in pregunta.lower():
                            resultados.append(eq)
        return resultados

    ecuaciones = obtener_ecuaciones(pregunta)

    if ecuaciones:
        opciones = [eq["eq"] for eq in ecuaciones]
        seleccion = st.selectbox("Ecuación", opciones)

        eq = ecuaciones[opciones.index(seleccion)]
        izquierda, derecha = eq["eq"].split("=")

        var_x = st.selectbox("Variable eje x", eq["variables"])

        params = {}
        for var in eq["variables"]:
            if var != var_x:
                params[var] = st.slider(var, -10.0, 10.0, 1.0)

        x_vals = np.linspace(0, 10, 100)
        entorno = {var_x: x_vals}
        entorno.update(params)

        try:
            y_vals = eval(derecha, {"np": np}, entorno)

            if np.isscalar(y_vals):
                y_vals = np.full_like(x_vals, y_vals)

            fig, ax = plt.subplots()
            ax.plot(x_vals, y_vals)
            ax.set_xlabel(var_x)
            ax.set_ylabel(izquierda)
            ax.set_title(eq["eq"])
            ax.grid()

            st.pyplot(fig)

        except Exception as e:
            st.error(f"Error: {e}")


# =========================
# 🎛️ SIMULADOR
# =========================
with tabs[2]:

    st.header("🎛️ Simulación MUA")

    u = st.slider("Velocidad inicial (u)", -10.0, 20.0, 0.0)
    a = st.slider("Aceleración (a)", -10.0, 10.0, 1.0)
    t_max = st.slider("Tiempo máximo", 1.0, 20.0, 10.0)

    t_vals = np.linspace(0, t_max, 100)
    s_vals = u * t_vals + 0.5 * a * t_vals**2

    fig, ax = plt.subplots()

    ax.plot(t_vals, s_vals, label="Trayectoria")
    ax.set_xlabel("Tiempo")
    ax.set_ylabel("Posición")
    ax.set_title("Movimiento Uniformemente Acelerado")
    ax.grid()
    ax.legend()

    st.pyplot(fig)


# =========================
# 🧪 GENERADOR
# =========================
with tabs[3]:

    st.header("🧪 Generador de preguntas IB")

    tema = st.text_input("Tema")

    if st.button("Generar pregunta"):
        if tema.strip():
            prompt = f"""
Genera una pregunta tipo examen de Física IB sobre {tema}.
Incluye:
- Enunciado
- Tipo (Paper 1 o Paper 2)
- Nivel
Sin solución.
"""
            respuesta = preguntar_chatgpt(prompt)
            st.write(respuesta)
        else:
            st.warning("Escribe un tema")
