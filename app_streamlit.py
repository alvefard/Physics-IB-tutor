
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

from tutor_ib import tutor_ib_fisica
from ecuaciones_ib import ecuaciones_ib
from cliente_openai import preguntar_chatgpt

plt.rcParams["figure.figsize"] = (6, 3)
# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Tutor IB Física", layout="wide")

st.title("🚀 Plataforma IB de Física")

col1, col2 = st.columns([1, 3])

with col1:
    st.image("logo-colegio-nueva-york.png", width=300)

with col2:
    st.image("FISICA.png", width=200)

tabs = st.tabs(["🧠 Tutor", "📊 Graficador", "🎛️ Simulador MUA", "🎯 Simulador Tiro parabólico", "🌌 Estrellas", "📡 Espectro EM", "🌊 Onda", "🧪 Generador", "📋 Investigación Interna"])

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

    st.header("🎛️ Simulación animada MUA")

    u = st.slider("Velocidad inicial (u)", -10.0, 20.0, 0.0)
    a = st.slider("Aceleración (a)", -10.0, 10.0, 1.0)
    t_max = st.slider("Tiempo máximo", 1.0, 20.0, 10.0)

    iniciar = st.button("▶ Iniciar simulación")

    placeholder = st.empty()

    if iniciar:

        t_vals = np.linspace(0, t_max, 100)
        s_vals = u * t_vals + 0.5 * a * t_vals**2

        for i in range(len(t_vals)):

            fig, ax = plt.subplots()

            ax.plot(t_vals, s_vals, linestyle="--", alpha=0.3)
            ax.plot(t_vals[i], s_vals[i], "ro")

            ax.set_xlim(0, t_max)
            ax.set_ylim(min(0, np.min(s_vals)), max(1, np.max(s_vals)))

            ax.set_xlabel("Tiempo")
            ax.set_ylabel("Posición")
            ax.set_title("Movimiento Uniformemente Acelerado")
            ax.grid()

            placeholder.pyplot(fig)
            plt.close(fig)

            time.sleep(0.03)

# =========================
# 🎯 Simulación: Tiro Parabólico
# =========================

with tabs[3]:

    st.header("🎯 Simulación: Tiro Parabólico")

    v0 = st.slider("Velocidad inicial (m/s)", 1.0, 50.0, 20.0)
    angulo = st.slider("Ángulo (grados)", 0.0, 90.0, 45.0)
    g = st.slider("Gravedad (m/s²)", 1.0, 20.0, 9.8)

    iniciar = st.button("▶ Iniciar simulación parabólica")

    placeholder = st.empty()

    if iniciar:

        theta = np.radians(angulo)

        t_total = (2 * v0 * np.sin(theta)) / g
        t_vals = np.linspace(0, t_total, 100)

        x_vals = v0 * np.cos(theta) * t_vals
        y_vals = v0 * np.sin(theta) * t_vals - 0.5 * g * t_vals**2

        for i in range(len(t_vals)):

            fig, ax = plt.subplots()

            ax.plot(x_vals, y_vals, linestyle="--", alpha=0.3)
            ax.plot(x_vals[i], y_vals[i], "ro")

            ax.set_xlim(0, max(x_vals) * 1.1)
            ax.set_ylim(0, max(y_vals) * 1.1)

            ax.set_xlabel("Distancia (m)")
            ax.set_ylabel("Altura (m)")
            ax.set_title("Tiro Parabólico")
            ax.grid()

            placeholder.pyplot(fig)
            plt.close(fig)

            time.sleep(0.03)

# =========================
# 🌌 Estrellas
# =========================
with tabs[4]:

    st.header("🌌 Temperatura de Estrellas (Cuerpo Negro)")

    T = st.slider("Temperatura (K)", 3000, 10000, 5500)

    # Constantes
    h = 6.626e-34
    c = 3e8
    k = 1.38e-23
    b = 2.898e-3  # Wien

    # Longitudes de onda
    lambda_vals = np.linspace(1e-7, 3e-6, 500)

    def planck(l, T):
        return (2*h*c**2)/(l**5) * (1/(np.exp((h*c)/(l*k*T)) - 1))

    intensidad = planck(lambda_vals, T)

    # Wien
    lambda_max = b / T
    lambda_max_nm = lambda_max * 1e9

    # 🎨 función color visible
    def wavelength_to_rgb(wavelength):
        if wavelength < 380 or wavelength > 780:
            return (0, 0, 0)

        if wavelength < 440:
            r = -(wavelength - 440) / (440 - 380)
            g = 0.0
            b = 1.0
        elif wavelength < 490:
            r = 0.0
            g = (wavelength - 440) / (490 - 440)
            b = 1.0
        elif wavelength < 510:
            r = 0.0
            g = 1.0
            b = -(wavelength - 510) / (510 - 490)
        elif wavelength < 580:
            r = (wavelength - 510) / (580 - 510)
            g = 1.0
            b = 0.0
        elif wavelength < 645:
            r = 1.0
            g = -(wavelength - 645) / (645 - 580)
            b = 0.0
        else:
            r = 1.0
            g = 0.0
            b = 0.0

        return (r, g, b)

    # 📊 Gráfica
    fig, ax = plt.subplots(figsize=(8,5))

    ax.plot(lambda_vals * 1e9, intensidad, color="black")

    # Línea pico
    ax.axvline(lambda_max_nm, linestyle="--", color="red", label="λ pico")

    # 🌈 ESPECTRO VISIBLE
    visible_range = np.linspace(380, 780, 200)

    for wl in visible_range:
        color = wavelength_to_rgb(wl)
        ax.axvspan(wl, wl+2, color=color, alpha=0.3)

    ax.set_xlabel("Longitud de onda (nm)")
    ax.set_ylabel("Intensidad")
    ax.set_title(f"Cuerpo negro a {T} K")
    ax.legend()
    ax.grid()

    st.pyplot(fig)

    # 📊 Resultados
    st.write(f"🔬 Longitud de onda pico: {lambda_max_nm:.0f} nm")

    # 🌈 Interpretación IB
    if lambda_max_nm < 450:
        st.write("🔵 Estrella azul (alta temperatura)")
    elif lambda_max_nm < 600:
        st.write("🟡 Estrella tipo Sol")
    else:
        st.write("🔴 Estrella roja (más fría)")
# =========================
# 📡 Espectro Electromagnético
# =========================
with tabs[5]:

    st.header("📡 Simulación: Espectro Electromagnético")

    c = 3e8
    h = 6.626e-34

    # Slider logarítmico (clave IB)
    log_lambda = st.slider("log10(Longitud de onda en metros)", -12.0, 3.0, -7.0)

    lambda_val = 10**log_lambda
    frecuencia = c / lambda_val
    energia = h * frecuencia

    lambda_nm = lambda_val * 1e9

    # Clasificación del espectro
    def region_em(lambda_m):
        if lambda_m > 1:
            return "Radio 📻"
        elif lambda_m > 1e-3:
            return "Microondas 📡"
        elif lambda_m > 7e-7:
            return "Infrarrojo 🔥"
        elif lambda_m > 4e-7:
            return "Visible 🌈"
        elif lambda_m > 1e-8:
            return "Ultravioleta ☀️"
        elif lambda_m > 1e-11:
            return "Rayos X 🩻"
        else:
            return "Rayos Gamma ☢️"

    region = region_em(lambda_val)

    st.write(f"📍 Región: **{region}**")
    st.write(f"📏 Longitud de onda: {lambda_val:.2e} m")
    st.write(f"🔁 Frecuencia: {frecuencia:.2e} Hz")
    st.write(f"⚡ Energía: {energia:.2e} J")

    # 📊 Visualización tipo barra
    fig, ax = plt.subplots(figsize=(10, 2))

    regiones = [
        ("Radio", 1e3),
        ("Microondas", 1e-2),
        ("Infrarrojo", 1e-5),
        ("Visible", 5e-7),
        ("UV", 1e-8),
        ("X", 1e-10),
        ("Gamma", 1e-12)
    ]

    posiciones = list(range(len(regiones)))

    ax.barh(posiciones, [1]*len(regiones), color="lightgray")

    nombres = [r[0] for r in regiones]
    ax.set_yticks(posiciones)
    ax.set_yticklabels(nombres)

    # Encontrar región actual
    for i, (_, val) in enumerate(regiones):
        if lambda_val >= val:
            idx = i
            break
    else:
        idx = len(regiones) - 1

    ax.barh(idx, 1, color="red")

    ax.set_title("Ubicación en el espectro EM")
    ax.set_xticks([])

    st.pyplot(fig)
# =========================
# 🌊 Onda Viajera
# =========================

with tabs[6]:

    st.header("🌊 Simulación: Onda Viajera")

    # Parámetros
    A = st.slider("Amplitud (A)", 0.1, 5.0, 1.0)
    f = st.slider("Frecuencia (Hz)", 0.1, 5.0, 1.0)
    lam = st.slider("Longitud de onda (λ)", 0.5, 10.0, 2.0)
    phi = st.slider("Fase (φ)", 0.0, 2*np.pi, 0.0)

    animar = st.button("▶ Animar onda")

    omega = 2 * np.pi * f
    k = 2 * np.pi / lam

    x = np.linspace(0, 10, 500)

    placeholder = st.empty()

    if animar:

        t_vals = np.linspace(0, 2, 100)

        for t in t_vals:

            y = A * np.sin(k * x - omega * t + phi)

            fig, ax = plt.subplots()

            ax.plot(x, y)

            ax.set_ylim(-A*1.2, A*1.2)
            ax.set_xlim(0, 10)

            ax.set_xlabel("Posición (x)")
            ax.set_ylabel("Desplazamiento")
            ax.set_title("Onda viajera")
            ax.grid()

            placeholder.pyplot(fig)
            plt.close(fig)

            time.sleep(0.03)

    v = f * lam

    st.write(f"⚡ Velocidad de la onda: {v:.2f} m/s")

# =========================
# 🧪 GENERADOR PREGUNTAS
# =========================
with tabs[7]:

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

# =========================
# 📋 Autoevaluación Investigación Interna (IB)
# =========================

with tabs[8]:

    st.header("📋 Autoevaluación Investigación Interna (IB)")

    st.markdown("Marca los indicadores que cumple tu trabajo:")

    # =========================
    # 🧠 CRITERIO A: DISEÑO
    # =========================

    st.subheader("A. Diseño de la investigación")

    A_checks = [
        st.checkbox("Pregunta clara y contextualizada"),
        st.checkbox("Variables identificadas correctamente"),
        st.checkbox("Variables controladas adecuadamente"),
        st.checkbox("Instrumentos con precisión definida"),
        st.checkbox("Procedimiento detallado y reproducible"),
        st.checkbox("Método permite recolectar datos suficientes"),
        st.checkbox("Contexto físico bien justificado")
    ]

    A_score = sum(A_checks)

    if A_score <= 2:
        A_level = 1
    elif A_score <= 4:
        A_level = 3
    elif A_score <= 6:
        A_level = 5
    else:
        A_level = 6

    st.write(f"🔢 Nivel estimado: {A_level}/6")

    # =========================
    # 📊 CRITERIO B: ANÁLISIS
    # =========================

    st.subheader("B. Análisis de datos")

    B_checks = [
        st.checkbox("Tablas con unidades correctas"),
        st.checkbox("Gráficas bien construidas"),
        st.checkbox("Procesamiento de datos correcto"),
        st.checkbox("Cálculo de incertidumbres"),
        st.checkbox("Propagación de incertidumbres"),
        st.checkbox("Ajuste de curvas / pendiente"),
        st.checkbox("Interpretación física de resultados")
    ]

    B_score = sum(B_checks)

    if B_score <= 2:
        B_level = 1
    elif B_score <= 4:
        B_level = 3
    elif B_score <= 6:
        B_level = 5
    else:
        B_level = 6

    st.write(f"🔢 Nivel estimado: {B_level}/6")

    # =========================
    # 🧾 CRITERIO C: CONCLUSIONES
    # =========================

    st.subheader("C. Conclusiones")

    C_checks = [
        st.checkbox("Conclusión responde la pregunta"),
        st.checkbox("Uso de datos en la conclusión"),
        st.checkbox("Relación con teoría física"),
        st.checkbox("Análisis de error porcentual"),
        st.checkbox("Discusión de discrepancias"),
        st.checkbox("Argumentación científica clara")
    ]

    C_score = sum(C_checks)

    if C_score <= 2:
        C_level = 1
    elif C_score <= 3:
        C_level = 3
    elif C_score <= 5:
        C_level = 5
    else:
        C_level = 6

    st.write(f"🔢 Nivel estimado: {C_level}/6")

    # =========================
    # 🔍 CRITERIO D: EVALUACIÓN
    # =========================

    st.subheader("D. Evaluación")

    D_checks = [
        st.checkbox("Identifica limitaciones reales"),
        st.checkbox("Explica impacto de errores"),
        st.checkbox("Propone mejoras específicas"),
        st.checkbox("Relaciona errores con resultados"),
        st.checkbox("Análisis cuantitativo del error"),
        st.checkbox("Propuestas científicamente justificadas")
    ]

    D_score = sum(D_checks)

    if D_score <= 2:
        D_level = 1
    elif D_score <= 3:
        D_level = 3
    elif D_score <= 5:
        D_level = 5
    else:
        D_level = 6

    st.write(f"🔢 Nivel estimado: {D_level}/6")

    # =========================
    # 🎯 NOTA FINAL
    # =========================

    st.markdown("---")

    total = A_level + B_level + C_level + D_level

    st.subheader("🎯 Resultado final")

    st.write(f"📊 Diseño: {A_level}/6")
    st.write(f"📊 Análisis: {B_level}/6")
    st.write(f"📊 Conclusiones: {C_level}/6")
    st.write(f"📊 Evaluación: {D_level}/6")

    st.success(f"🏆 Puntaje total estimado: {total}/24")

    # Interpretación
    if total >= 20:
        st.success("Nivel IB: Excelente 🔥")
    elif total >= 16:
        st.info("Nivel IB: Bueno 👍")
    elif total >= 10:
        st.warning("Nivel IB: Básico ⚠️")
    else:
        st.error("Nivel IB: Bajo ❌")
        st.markdown("---")
st.subheader("🧠 Retroalimentación automática")

if st.button("Generar retroalimentación con IA"):

    with st.spinner("Analizando tu investigación..."):

        prompt = f"""
Eres un profesor experto del Bachillerato Internacional (IB) en Física.

Un estudiante ha realizado una autoevaluación de su Investigación Interna con los siguientes resultados:

Diseño: {A_level}/6
Análisis de datos: {B_level}/6
Conclusiones: {C_level}/6
Evaluación: {D_level}/6

Genera una retroalimentación estructurada que incluya:

1. Fortalezas del trabajo
2. Debilidades específicas
3. Qué le falta para subir al siguiente nivel IB en cada criterio
4. Recomendaciones concretas de mejora (tipo acción)
5. Lenguaje claro para estudiante de bachillerato

NO seas genérico. Sé específico como un evaluador IB.
"""

        feedback = preguntar_chatgpt(prompt)

        st.markdown("### 📊 Retroalimentación IA")
        st.write(feedback)
