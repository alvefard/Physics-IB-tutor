
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
from streamlit_autorefresh import st_autorefresh
import datetime
from zoneinfo import ZoneInfo

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

tabs = st.tabs(["🧠 Tutor", "📊 Graficador", "🎛️ Simulador MUA", "🎯 Simulador Tiro parabólico", "🌌 Estrellas", "📡 Espectro EM", "🌊 Onda", "🧪 Generador", "📋 Investigación Interna", "⏱️ Exámenes IB"])

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

    col1, col2 = st.columns([1, 2])  # 👈 izquierda pequeña, derecha grande

    with col1:

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

    # 👉 GRÁFICA A LA DERECHA
    with col2:

        if ecuaciones:

            x_vals = np.linspace(0, 10, 100)
            entorno = {var_x: x_vals}
            entorno.update(params)

            try:
                y_vals = eval(derecha, {"np": np}, entorno)

                if np.isscalar(y_vals):
                    y_vals = np.full_like(x_vals, y_vals)

                fig, ax = plt.subplots(figsize=(6, 3))  # 👈 tamaño optimizado

                ax.plot(x_vals, y_vals)
                ax.set_xlabel(var_x)
                ax.set_ylabel(izquierda)
                ax.set_title(eq["eq"])
                ax.grid()

                plt.tight_layout()

                st.pyplot(fig, use_container_width=True)

            except Exception as e:
                st.error(f"Error: {e}")


# =========================
# 🎛️ SIMULADOR
# =========================
with tabs[2]:

    st.header("🎛️ Simulación animada MUA")

    col1, col2 = st.columns([1, 2])  # 👈 layout

    # =========================
    # 🎛️ CONTROLES (IZQUIERDA)
    # =========================
    with col1:

        u = st.slider("Velocidad inicial (u)", -10.0, 20.0, 0.0)
        a = st.slider("Aceleración (a)", -10.0, 10.0, 1.0)
        t_max = st.slider("Tiempo máximo", 1.0, 20.0, 10.0)

        iniciar = st.button("▶ Iniciar simulación")

    # =========================
    # 📊 SIMULACIÓN (DERECHA)
    # =========================
    with col2:

        placeholder = st.empty()

        if iniciar:

            t_vals = np.linspace(0, t_max, 100)
            s_vals = u * t_vals + 0.5 * a * t_vals**2

            for i in range(len(t_vals)):

                fig, ax = plt.subplots(figsize=(6, 2.5))  # 👈 compacto

                ax.plot(t_vals, s_vals, linestyle="--", alpha=0.3)
                ax.plot(t_vals[i], s_vals[i], "ro")

                ax.set_xlim(0, t_max)
                ax.set_ylim(min(0, np.min(s_vals)), max(1, np.max(s_vals)))

                ax.set_xlabel("Tiempo")
                ax.set_ylabel("Posición")
                ax.set_title("Movimiento Uniformemente Acelerado")
                ax.grid()

                plt.tight_layout()

                placeholder.pyplot(fig, use_container_width=True)

                plt.close(fig)

                time.sleep(0.03)

# =========================
# 🎯 Simulación: Tiro Parabólico
# =========================

with tabs[3]:

    st.header("🎯 Simulación: Tiro Parabólico")

    col1, col2 = st.columns([1, 2])  # 👈 layout

    # =========================
    # 🎛️ CONTROLES (IZQUIERDA)
    # =========================
    with col1:

        v0 = st.slider("Velocidad inicial (m/s)", 1.0, 50.0, 20.0)
        angulo = st.slider("Ángulo (grados)", 0.0, 90.0, 45.0)
        g = st.slider("Gravedad (m/s²)", 1.0, 20.0, 9.8)

        iniciar = st.button("▶ Iniciar simulación parabólica")

    # =========================
    # 📊 SIMULACIÓN (DERECHA)
    # =========================
    with col2:

        placeholder = st.empty()

        if iniciar:

            theta = np.radians(angulo)

            t_total = (2 * v0 * np.sin(theta)) / g
            t_vals = np.linspace(0, t_total, 100)

            x_vals = v0 * np.cos(theta) * t_vals
            y_vals = v0 * np.sin(theta) * t_vals - 0.5 * g * t_vals**2

            for i in range(len(t_vals)):

                fig, ax = plt.subplots(figsize=(6, 2.5))  # 👈 compacto

                ax.plot(x_vals, y_vals, linestyle="--", alpha=0.3)
                ax.plot(x_vals[i], y_vals[i], "ro")

                ax.set_xlim(0, max(x_vals) * 1.1)
                ax.set_ylim(0, max(y_vals) * 1.1)

                ax.set_xlabel("Distancia (m)")
                ax.set_ylabel("Altura (m)")
                ax.set_title("Tiro Parabólico")
                ax.grid()

                plt.tight_layout()

                placeholder.pyplot(fig, use_container_width=True)

                plt.close(fig)

                time.sleep(0.03)

# =========================
# 🌌 Estrellas
# =========================
with tabs[4]:

    st.header("🌌 Temperatura de Estrellas (Cuerpo Negro)")

    col1, col2 = st.columns([1, 2])  # 👈 layout profesional

    # =========================
    # 🎛️ CONTROLES (IZQUIERDA)
    # =========================
    with col1:

        T = st.slider("Temperatura (K)", 3000, 10000, 5500)

        # Constantes
        h = 6.626e-34
        c = 3e8
        k = 1.38e-23
        b = 2.898e-3

        # Wien
        lambda_max = b / T
        lambda_max_nm = lambda_max * 1e9

        st.write(f"🔬 λ pico: {lambda_max_nm:.0f} nm")

        if lambda_max_nm < 450:
            st.write("🔵 Estrella azul")
        elif lambda_max_nm < 600:
            st.write("🟡 Estrella tipo Sol")
        else:
            st.write("🔴 Estrella roja")

    # =========================
    # 📊 GRÁFICA (DERECHA)
    # =========================
    with col2:

        lambda_vals = np.linspace(1e-7, 3e-6, 500)

        def planck(l, T):
            return (2*h*c**2)/(l**5) * (1/(np.exp((h*c)/(l*k*T)) - 1))

        intensidad = planck(lambda_vals, T)

        # 🎨 función color visible
        def wavelength_to_rgb(wavelength):

            if wavelength < 380 or wavelength > 780:
                return (0, 0, 0)

            if wavelength < 440:
                r = -(wavelength - 440) / (440 - 380)
                g = 0
                b = 1
            elif wavelength < 490:
                r = 0
                g = (wavelength - 440) / (490 - 440)
                b = 1
            elif wavelength < 510:
                r = 0
                g = 1
                b = -(wavelength - 510) / (510 - 490)
            elif wavelength < 580:
                r = (wavelength - 510) / (580 - 510)
                g = 1
                b = 0
            elif wavelength < 645:
                r = 1
                g = -(wavelength - 645) / (645 - 580)
                b = 0
            else:
                r = 1
                g = 0
                b = 0

            return (r, g, b)

        # 📊 Gráfica compacta
        fig, ax = plt.subplots(figsize=(6, 2.5))  # 👈 tamaño optimizado

        ax.plot(lambda_vals * 1e9, intensidad, color="black")

        ax.axvline(lambda_max_nm, linestyle="--", color="red", label="λ pico")

        # 🌈 espectro visible
        visible_range = np.linspace(380, 780, 200)

        for wl in visible_range:
            color = wavelength_to_rgb(wl)
            ax.axvspan(wl, wl+2, color=color, alpha=0.3)

        ax.set_xlabel("Longitud de onda (nm)")
        ax.set_ylabel("Intensidad")
        ax.set_title(f"Cuerpo negro a {T} K")
        ax.legend()
        ax.grid()

        plt.tight_layout()

        st.pyplot(fig, use_container_width=True)
# =========================
# 📡 Espectro Electromagnético
# =========================
with tabs[5]:

    st.header("📡 Simulación: Espectro Electromagnético")

    col1, col2 = st.columns([1, 2])

    # =========================
    # IZQUIERDA
    # =========================
    with col1:

        c = 3e8
        h = 6.626e-34

        log_lambda = st.slider(
            "log10(Longitud de onda en metros)", -12.0, 3.0, -7.0
        )

        lambda_val = 10**log_lambda
        frecuencia = c / lambda_val
        energia = h * frecuencia

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
        st.write(f"📏 λ: {lambda_val:.2e} m")
        st.write(f"🔁 f: {frecuencia:.2e} Hz")
        st.write(f"⚡ E: {energia:.2e} J")

    # =========================
    # DERECHA (ONDA)
    # =========================
    with col2:

        x = np.linspace(0, 10, 1000)

        escala = 1e6
        lambda_plot = lambda_val * escala

        if lambda_plot == 0:
            lambda_plot = 1e-6

        k = 2 * np.pi / lambda_plot

        y = np.sin(k * x)

        fig, ax = plt.subplots(figsize=(6, 2.5))

        color = "blue"
        if "Visible" in region:
            color = "orange"
        elif "Gamma" in region:
            color = "purple"
        elif "Radio" in region:
            color = "green"

        ax.plot(x, y, color=color)

        ax.set_ylim(-1.2, 1.2)
        ax.set_xlim(0, 10)

        ax.set_title(f"Onda EM ({region})")
        ax.set_xlabel("Espacio")
        ax.set_ylabel("Amplitud")

        ax.grid()

        plt.tight_layout()

        st.pyplot(fig, use_container_width=True)
# =========================
# 🌊 Onda Viajera
# =========================

with tabs[6]:

    st.header("🌊 Simulación: Onda Viajera")

    col1, col2 = st.columns([1, 2])  # 👈 layout

    # =========================
    # 🎛️ CONTROLES (IZQUIERDA)
    # =========================
    with col1:

        A = st.slider("Amplitud (A)", 0.1, 5.0, 1.0)
        f = st.slider("Frecuencia (Hz)", 0.1, 5.0, 1.0)
        lam = st.slider("Longitud de onda (λ)", 0.5, 10.0, 2.0)
        phi = st.slider("Fase (φ)", 0.0, 2*np.pi, 0.0)

        animar = st.button("▶ Animar onda")

        v = f * lam
        st.write(f"⚡ Velocidad de la onda: {v:.2f} m/s")

    # =========================
    # 📊 GRÁFICA (DERECHA)
    # =========================
    with col2:

        omega = 2 * np.pi * f
        k = 2 * np.pi / lam

        x = np.linspace(0, 10, 500)

        placeholder = st.empty()

        if animar:

            t_vals = np.linspace(0, 2, 100)

            for t in t_vals:

                y = A * np.sin(k * x - omega * t + phi)

                fig, ax = plt.subplots(figsize=(6, 2.5))  # 👈 compacto

                ax.plot(x, y)

                ax.set_ylim(-A*1.2, A*1.2)
                ax.set_xlim(0, 10)

                ax.set_xlabel("Posición (x)")
                ax.set_ylabel("Desplazamiento")
                ax.set_title("Onda viajera")
                ax.grid()

                plt.tight_layout()

                placeholder.pyplot(fig, use_container_width=True)

                plt.close(fig)

                time.sleep(0.03)

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
        
# =========================
# ⏱️ Gestión de Exámenes IB"
# =========================

with tabs[8]:

    # =========================
    # 🎨 ESTILO (LETRA GRANDE)
    # =========================
    st.markdown("""
        <style>
        .big-text {
            font-size: 42px !important;
            font-weight: bold;
            text-align: center;
        }
        .medium-text {
            font-size: 22px !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.header("⏱️ Gestión de Exámenes IB")

    # =========================
    # 🕒 HORA COLOMBIA (SIN BUCLE)
    # =========================
    ahora = datetime.datetime.now(ZoneInfo("America/Bogota"))

    # =========================
    # 📐 COLUMNAS
    # =========================
    col1, col2 = st.columns([1, 1])

    # =========================
    # 🧠 IZQUIERDA (CONFIGURACIÓN)
    # =========================
    with col1:

        st.markdown("### 🧪 Configuración")

        examenes = [
            ("Biology NM P1", "Estructurado", 90),
            ("Biology NM P2", "Estructurado", 90),
            ("Gestión NM NS P1", "No estructurado", 90),
            ("Gestión NS P3", "No estructurado", 75),
            ("Gestión Empresarial NM P2", "Estructurado", 90),
            ("Gestión Empresarial NS P2", "No estructurado", 105),
            ("Lengua y Lit. NS P1", "No estructurado", 135),
            ("Lengua y Lit. NS P2", "No estructurado", 105),
            ("Chemistry NM P1", "Estructurado", 90),
            ("Chemistry NM P2", "Estructurado", 90),
            ("Historia NM P2", "No estructurado", 90),
            ("Historia NS P3", "No estructurado", 150),
            ("Física NM P1", "Estructurado", 90),
            ("Física NM P2", "Estructurado", 90),
            ("Inglés B NS P1", "Estructurado", 90),
            ("Inglés B NS Lectura", "Estructurado", 60),
            ("Inglés B NS Auditiva", "Estructurado", 60),
            ("Análisis NM P1", "Semiestructurado", 90),
            ("Aplicaciones NM P1", "Estructurado", 90),
            ("Política Global NS P2", "No estructurado", 165),
            ("ESS NM P1", "Estructurado", 60),
            ("ESS NM P2", "Estructurado", 120),
            ("Filosofía NS P3", "No estructurado", 75),
        ]

        nombres = [e[0] for e in examenes]

        seleccion = st.selectbox("Selecciona el examen", nombres)
        examen = examenes[nombres.index(seleccion)]

        tipo = examen[1]
        duracion = examen[2]

        st.markdown(f"<p class='medium-text'>🧪 Tipo: {tipo}</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='medium-text'>⏱️ Duración: {duracion} min</p>", unsafe_allow_html=True)

        hora_inicio = st.time_input("Hora de inicio")

        inicio_dt = datetime.datetime.combine(datetime.date.today(), hora_inicio)
        inicio_dt = inicio_dt.replace(tzinfo=ZoneInfo("America/Bogota"))

        fin_dt = inicio_dt + datetime.timedelta(minutes=duracion)

        st.markdown(f"<p class='medium-text'>🕒 Fin: {fin_dt.time()}</p>", unsafe_allow_html=True)

        # =========================
        # 🚻 BAÑO
        # =========================
        if duracion > 60:

            st.markdown("### 🚻 Baño")

            salida_permitida = st.checkbox("Permitir salida")

            if salida_permitida:

                salida_inicio = inicio_dt + datetime.timedelta(minutes=60)
                salida_fin = fin_dt - datetime.timedelta(minutes=15)

                st.success(f"Ventana: {salida_inicio.time()} → {salida_fin.time()}")

        else:
            st.warning("🚫 Sin salida al baño")

    # =========================
    # ⏱️ DERECHA (RELOJ + ESTADO)
    # =========================
    with col2:

        st.markdown("### 🕒 Hora oficial (Colombia)")

        st.markdown(
            f"<p class='big-text'>{ahora.strftime('%H:%M:%S')}</p>",
            unsafe_allow_html=True
        )

        st.markdown("---")

        st.markdown("### 📊 Estado del examen")

        if ahora >= fin_dt:
            st.error("⛔ FINALIZADO")

        elif ahora >= (fin_dt - datetime.timedelta(minutes=15)):
            st.warning("⚠️ Últimos 15 minutos")

        elif ahora >= inicio_dt:
            st.success("🟢 En curso")

        else:
            st.info("⏳ No inicia")
