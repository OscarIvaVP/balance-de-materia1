import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import random
from datetime import datetime

# ===========================
# CONFIGURACIÓN DE LA PÁGINA
# ===========================
st.set_page_config(
    page_title="Balance de Materia - °Brix",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===========================
# DATOS DE REFERENCIA
# ===========================

@st.cache_data
def obtener_frutas():
    """Retorna un diccionario con valores típicos de °Brix por fruta"""
    return {
        "Personalizado": {"brix_inicial": 7.0, "descripcion": "Ingresa tus propios valores"},
        "Manzana": {"brix_inicial": 12.0, "descripcion": "Típico para manzanas frescas"},
        "Naranja": {"brix_inicial": 11.5, "descripcion": "Jugo de naranja natural"},
        "Piña": {"brix_inicial": 13.0, "descripcion": "Pulpa de piña fresca"},
        "Mango": {"brix_inicial": 14.0, "descripcion": "Pulpa de mango maduro"},
        "Fresa": {"brix_inicial": 8.0, "descripcion": "Pulpa de fresa fresca"},
        "Durazno": {"brix_inicial": 10.5, "descripcion": "Pulpa de durazno maduro"},
        "Uva": {"brix_inicial": 16.0, "descripcion": "Jugo de uva natural"},
        "Maracuyá": {"brix_inicial": 14.5, "descripcion": "Pulpa de maracuyá"},
        "Guayaba": {"brix_inicial": 8.5, "descripcion": "Pulpa de guayaba rosa"}
    }

@st.cache_data
def obtener_casos_estudio():
    """Retorna casos de estudio reales de la industria"""
    return pd.DataFrame({
        "Producto": ["Mermelada de fresa", "Néctar de durazno", "Concentrado de manzana",
                     "Jalea de uva", "Salsa de tomate", "Jugo de naranja",
                     "Almíbar ligero", "Almíbar pesado"],
        "Fruta": ["Fresa", "Durazno", "Manzana", "Uva", "Tomate", "Naranja", "Mixto", "Mixto"],
        "°Brix Inicial": [8.0, 10.5, 12.0, 16.0, 5.0, 11.5, 8.0, 8.0],
        "°Brix Objetivo": [65.0, 14.0, 70.0, 62.0, 28.0, 12.0, 20.0, 40.0],
        "Aplicación": ["Conserva", "Bebida", "Ingrediente industrial",
                      "Conserva", "Condimento", "Bebida", "Conservas", "Conservas"],
        "Notas": [
            "Requiere cocción prolongada para gelificación",
            "Producto listo para consumo, mínimo procesamiento",
            "Se usa como edulcorante natural en industria de panificación",
            "Alta concentración para estabilidad sin refrigeración",
            "Balance entre dulzor y acidez para perfil de sabor",
            "Ajuste ligero para estandarización del producto",
            "Para frutas en conserva (duraznos, peras)",
            "Para frutas en conserva de alta calidad"
        ]
    })

# ===========================
# FUNCIONES DE CÁLCULO
# ===========================

def calcular_azucar(masa_pulpa_inicial, brix_inicial, brix_objetivo):
    """
    Calcula la cantidad de azúcar (en kg) necesaria para agregar a la pulpa
    y alcanzar los °Brix objetivo.
    """
    concentracion_inicial = brix_inicial / 100.0
    concentracion_objetivo = brix_objetivo / 100.0

    if concentracion_objetivo <= concentracion_inicial:
        return None, "Los °Brix objetivo deben ser mayores que los iniciales."

    solidos_iniciales = masa_pulpa_inicial * concentracion_inicial

    try:
        azucar_a_agregar = (masa_pulpa_inicial * concentracion_objetivo - solidos_iniciales) / (1 - concentracion_objetivo)
    except ZeroDivisionError:
        return None, "Los °Brix objetivo no pueden ser 100%."

    return azucar_a_agregar, None

def calcular_dilucion(masa_inicial, brix_inicial, brix_objetivo):
    """Calcula cantidad de agua para reducir °Brix"""
    concentracion_inicial = brix_inicial / 100.0
    concentracion_objetivo = brix_objetivo / 100.0

    if concentracion_objetivo >= concentracion_inicial:
        return None, "Los °Brix objetivo deben ser menores que los iniciales para dilución."

    if concentracion_objetivo == 0:
        return None, "Los °Brix objetivo no pueden ser 0%."

    agua_agregar = masa_inicial * (concentracion_inicial - concentracion_objetivo) / concentracion_objetivo
    return agua_agregar, None

# ===========================
# FUNCIONES DE VISUALIZACIÓN
# ===========================

def crear_grafico_comparativo(masa_pulpa, brix_inicial, cantidad_azucar, brix_objetivo):
    """Crea gráfico de barras comparando antes y después"""
    solidos_iniciales = masa_pulpa * (brix_inicial / 100)
    agua_inicial = masa_pulpa - solidos_iniciales

    masa_final = masa_pulpa + cantidad_azucar
    solidos_finales = solidos_iniciales + cantidad_azucar
    agua_final = agua_inicial

    fig = go.Figure()

    # Barras apiladas
    fig.add_trace(go.Bar(
        name='Sólidos (Azúcar)',
        x=['Antes', 'Después'],
        y=[solidos_iniciales, solidos_finales],
        marker_color='#FF6B6B',
        text=[f'{solidos_iniciales:.2f} kg', f'{solidos_finales:.2f} kg'],
        textposition='inside'
    ))

    fig.add_trace(go.Bar(
        name='Agua',
        x=['Antes', 'Después'],
        y=[agua_inicial, agua_final],
        marker_color='#4ECDC4',
        text=[f'{agua_inicial:.2f} kg', f'{agua_final:.2f} kg'],
        textposition='inside'
    ))

    fig.update_layout(
        title='Composición de la Mezcla: Antes vs Después',
        barmode='stack',
        xaxis_title='Estado',
        yaxis_title='Masa (kg)',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=400
    )

    return fig

def crear_grafico_circular(masa_pulpa, brix_inicial, cantidad_azucar):
    """Crea gráfico circular de la composición final"""
    solidos_iniciales = masa_pulpa * (brix_inicial / 100)
    agua_inicial = masa_pulpa - solidos_iniciales

    labels = ['Azúcar agregada', 'Sólidos iniciales', 'Agua']
    values = [cantidad_azucar, solidos_iniciales, agua_inicial]
    colors = ['#FF6B6B', '#FFE66D', '#4ECDC4']

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=.3,
        marker_colors=colors,
        textinfo='label+percent',
        textposition='auto'
    )])

    fig.update_layout(
        title='Composición Final de la Mezcla',
        height=400,
        showlegend=True
    )

    return fig

def crear_grafico_interactivo(masa_pulpa, brix_inicial, brix_objetivo):
    """Crea gráfico interactivo mostrando sensibilidad"""
    cantidad_azucar_objetivo, _ = calcular_azucar(masa_pulpa, brix_inicial, brix_objetivo)

    # Generar rango de azúcar alrededor del objetivo
    if cantidad_azucar_objetivo:
        azucar_min = max(0, cantidad_azucar_objetivo * 0.5)
        azucar_max = cantidad_azucar_objetivo * 1.5
        azucar_range = np.linspace(azucar_min, azucar_max, 100)

        brix_resultante = []
        for azucar in azucar_range:
            solidos_iniciales = masa_pulpa * (brix_inicial / 100)
            masa_final = masa_pulpa + azucar
            solidos_finales = solidos_iniciales + azucar
            brix = (solidos_finales / masa_final) * 100
            brix_resultante.append(brix)

        fig = go.Figure()

        # Línea principal
        fig.add_trace(go.Scatter(
            x=azucar_range,
            y=brix_resultante,
            mode='lines',
            name='°Brix resultante',
            line=dict(color='#4ECDC4', width=3)
        ))

        # Línea objetivo
        fig.add_hline(
            y=brix_objetivo,
            line_dash="dash",
            line_color="#FF6B6B",
            annotation_text=f"Objetivo: {brix_objetivo}°Brix"
        )

        # Punto óptimo
        fig.add_trace(go.Scatter(
            x=[cantidad_azucar_objetivo],
            y=[brix_objetivo],
            mode='markers',
            name='Punto óptimo',
            marker=dict(size=15, color='#FF6B6B', symbol='star')
        ))

        fig.update_layout(
            title='Análisis de Sensibilidad: Azúcar vs °Brix',
            xaxis_title='Azúcar Agregada (kg)',
            yaxis_title='°Brix Resultante (%)',
            hovermode='x unified',
            height=400
        )

        return fig
    return None

def crear_diagrama_flujo(masa_pulpa, brix_inicial, cantidad_azucar, brix_final):
    """Crea diagrama de flujo del proceso"""
    fig = go.Figure()

    # Cuadros del diagrama
    boxes = [
        {"x": 0.15, "y": 0.5, "text": f"ENTRADA<br>Pulpa: {masa_pulpa:.1f} kg<br>°Brix: {brix_inicial:.1f}%", "color": "#4ECDC4"},
        {"x": 0.5, "y": 0.5, "text": f"PROCESO<br>+ Azúcar: {cantidad_azucar:.2f} kg<br>Mezclado", "color": "#FFE66D"},
        {"x": 0.85, "y": 0.5, "text": f"SALIDA<br>Total: {masa_pulpa + cantidad_azucar:.2f} kg<br>°Brix: {brix_final:.1f}%", "color": "#95E1D3"}
    ]

    # Dibujar cuadros
    for box in boxes:
        fig.add_shape(
            type="rect",
            x0=box["x"]-0.08, y0=box["y"]-0.15,
            x1=box["x"]+0.08, y1=box["y"]+0.15,
            fillcolor=box["color"],
            line=dict(color="black", width=2)
        )

        fig.add_annotation(
            x=box["x"], y=box["y"],
            text=box["text"],
            showarrow=False,
            font=dict(size=11, color="black"),
            align="center"
        )

    # Flechas
    arrows = [
        {"x0": 0.23, "x1": 0.42, "y": 0.5},
        {"x0": 0.58, "x1": 0.77, "y": 0.5}
    ]

    for arrow in arrows:
        fig.add_annotation(
            x=arrow["x1"], y=arrow["y"],
            ax=arrow["x0"], ay=arrow["y"],
            xref='x', yref='y',
            axref='x', ayref='y',
            showarrow=True,
            arrowhead=2,
            arrowsize=1.5,
            arrowwidth=2,
            arrowcolor='black'
        )

    fig.update_layout(
        showlegend=False,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 1]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 1]),
        height=250,
        margin=dict(l=20, r=20, t=30, b=20),
        plot_bgcolor='white'
    )

    return fig

def generar_ejercicio(dificultad):
    """Genera un ejercicio aleatorio según el nivel de dificultad"""
    if dificultad == "Básico":
        masa = round(random.uniform(10, 100), 1)
        brix_inicial = round(random.uniform(5, 15), 1)
        brix_objetivo = round(brix_inicial + random.uniform(3, 10), 1)
    elif dificultad == "Intermedio":
        masa = round(random.uniform(50, 500), 1)
        brix_inicial = round(random.uniform(8, 18), 1)
        brix_objetivo = round(brix_inicial + random.uniform(5, 20), 1)
    else:  # Avanzado
        masa = round(random.uniform(100, 1000), 1)
        brix_inicial = round(random.uniform(6, 20), 1)
        brix_objetivo = round(brix_inicial + random.uniform(10, 40), 1)

    azucar, _ = calcular_azucar(masa, brix_inicial, brix_objetivo)

    return {
        "masa": masa,
        "brix_inicial": brix_inicial,
        "brix_objetivo": brix_objetivo,
        "respuesta_correcta": azucar
    }

# ===========================
# INICIALIZACIÓN DE SESSION STATE
# ===========================

if 'historial' not in st.session_state:
    st.session_state.historial = []

if 'ejercicios_correctos' not in st.session_state:
    st.session_state.ejercicios_correctos = 0

if 'ejercicios_totales' not in st.session_state:
    st.session_state.ejercicios_totales = 0

if 'ejercicio_actual' not in st.session_state:
    st.session_state.ejercicio_actual = None

# ===========================
# INTERFAZ PRINCIPAL
# ===========================

st.title("🧪 Sistema Interactivo de Balance de Materia")
st.markdown("### Ajuste de °Brix en Pulpas de Frutas")
st.markdown("---")

# Crear tabs principales
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Calculadora Profesional",
    "📚 Fundamentos Teóricos",
    "✏️ Ejercicios Prácticos",
    "📁 Biblioteca de Casos"
])

# ===========================
# TAB 1: CALCULADORA PROFESIONAL
# ===========================

with tab1:
    # Sidebar para inputs
    with st.sidebar:
        st.header("⚙️ Parámetros de Entrada")

        frutas = obtener_frutas()
        fruta_seleccionada = st.selectbox(
            "Selecciona el tipo de fruta",
            options=list(frutas.keys()),
            help="Selecciona una fruta para cargar valores típicos o 'Personalizado' para ingresar tus propios valores"
        )

        st.caption(frutas[fruta_seleccionada]["descripcion"])

        st.markdown("---")

        # Inputs con valores predeterminados
        masa_pulpa = st.number_input(
            "Masa inicial de la pulpa (kg)",
            min_value=0.1,
            value=50.0,
            step=1.0,
            help="Cantidad total de pulpa disponible"
        )

        if fruta_seleccionada == "Personalizado":
            brix_inicial = st.number_input(
                "°Brix iniciales (%)",
                min_value=0.0,
                max_value=99.9,
                value=7.0,
                step=0.1
            )
        else:
            brix_inicial = st.number_input(
                "°Brix iniciales (%)",
                min_value=0.0,
                max_value=99.9,
                value=frutas[fruta_seleccionada]["brix_inicial"],
                step=0.1
            )

        brix_objetivo = st.number_input(
            "°Brix objetivo (%)",
            min_value=0.0,
            max_value=99.9,
            value=min(65.0, brix_inicial + 10.0),
            step=0.1,
            help="Concentración deseada de sólidos solubles"
        )

        st.markdown("---")

        calcular = st.button("🔬 Calcular Balance", type="primary", use_container_width=True)

        # Calculadora de dilución
        st.markdown("---")
        st.subheader("💧 Calculadora de Dilución")
        st.caption("Para reducir °Brix")

        brix_objetivo_dilucion = st.number_input(
            "°Brix objetivo para dilución (%)",
            min_value=0.1,
            max_value=99.9,
            value=max(0.1, brix_inicial - 2.0),
            step=0.1,
            key="dilucion_objetivo"
        )

        calcular_dilucion_btn = st.button("💧 Calcular Dilución", use_container_width=True)

    # Área principal
    if calcular:
        cantidad_azucar, error = calcular_azucar(masa_pulpa, brix_inicial, brix_objetivo)

        if error:
            st.error(f"❌ {error}")
        else:
            # Guardar en historial
            st.session_state.historial.append({
                "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Fruta": fruta_seleccionada,
                "Masa Pulpa (kg)": masa_pulpa,
                "°Brix Inicial": brix_inicial,
                "°Brix Objetivo": brix_objetivo,
                "Azúcar a Agregar (kg)": round(cantidad_azucar, 3)
            })

            # Métricas principales
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Azúcar a Agregar", f"{cantidad_azucar:.3f} kg", help="Cantidad de azúcar pura necesaria")

            with col2:
                masa_final = masa_pulpa + cantidad_azucar
                st.metric("Masa Total Final", f"{masa_final:.2f} kg", f"+{cantidad_azucar:.2f} kg")

            with col3:
                incremento = brix_objetivo - brix_inicial
                st.metric("Incremento °Brix", f"+{incremento:.1f}%", f"{brix_inicial:.1f}% → {brix_objetivo:.1f}%")

            with col4:
                porcentaje_azucar = (cantidad_azucar / masa_final) * 100
                st.metric("% Azúcar Agregada", f"{porcentaje_azucar:.1f}%", help="Porcentaje de azúcar en la mezcla final")

            st.markdown("---")

            # Diagrama de flujo
            st.subheader("📈 Diagrama de Flujo del Proceso")
            solidos_iniciales = masa_pulpa * (brix_inicial / 100)
            solidos_finales = solidos_iniciales + cantidad_azucar
            masa_final = masa_pulpa + cantidad_azucar
            brix_final_verificado = (solidos_finales / masa_final) * 100

            fig_flujo = crear_diagrama_flujo(masa_pulpa, brix_inicial, cantidad_azucar, brix_final_verificado)
            st.plotly_chart(fig_flujo, use_container_width=True)

            # Gráficos comparativos
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("📊 Composición Comparativa")
                fig_barras = crear_grafico_comparativo(masa_pulpa, brix_inicial, cantidad_azucar, brix_objetivo)
                st.plotly_chart(fig_barras, use_container_width=True)

            with col2:
                st.subheader("🥧 Composición Final")
                fig_circular = crear_grafico_circular(masa_pulpa, brix_inicial, cantidad_azucar)
                st.plotly_chart(fig_circular, use_container_width=True)

            # Gráfico interactivo de sensibilidad
            st.subheader("📉 Análisis de Sensibilidad")
            fig_interactivo = crear_grafico_interactivo(masa_pulpa, brix_inicial, brix_objetivo)
            if fig_interactivo:
                st.plotly_chart(fig_interactivo, use_container_width=True)

            # Verificación detallada
            with st.expander("🔍 Ver Verificación Detallada del Cálculo"):
                st.markdown(f"""
                **Balance de Masa Completo:**

                1. **Composición Inicial:**
                   - Masa de pulpa: {masa_pulpa:.2f} kg
                   - Concentración inicial: {brix_inicial:.2f}%
                   - Sólidos iniciales: {masa_pulpa:.2f} kg × {brix_inicial/100:.4f} = {solidos_iniciales:.3f} kg
                   - Agua inicial: {masa_pulpa:.2f} kg - {solidos_iniciales:.3f} kg = {masa_pulpa - solidos_iniciales:.3f} kg

                2. **Adición de Azúcar:**
                   - Azúcar agregada: {cantidad_azucar:.3f} kg

                3. **Composición Final:**
                   - Masa total: {masa_pulpa:.2f} kg + {cantidad_azucar:.3f} kg = **{masa_final:.3f} kg**
                   - Sólidos totales: {solidos_iniciales:.3f} kg + {cantidad_azucar:.3f} kg = **{solidos_finales:.3f} kg**
                   - Agua: {masa_pulpa - solidos_iniciales:.3f} kg (sin cambio)

                4. **Verificación de °Brix:**
                   - °Brix final = (Sólidos totales / Masa total) × 100
                   - °Brix final = ({solidos_finales:.3f} / {masa_final:.3f}) × 100 = **{brix_final_verificado:.2f}%**
                   - Objetivo: {brix_objetivo:.2f}%
                   - ✅ Diferencia: {abs(brix_final_verificado - brix_objetivo):.4f}% (despreciable)
                """)

    elif calcular_dilucion_btn:
        agua_necesaria, error = calcular_dilucion(masa_pulpa, brix_inicial, brix_objetivo_dilucion)

        if error:
            st.error(f"❌ {error}")
        else:
            st.success(f"💧 Se deben agregar **{agua_necesaria:.3f} kg** de agua para reducir a {brix_objetivo_dilucion}°Brix")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Agua a Agregar", f"{agua_necesaria:.3f} kg")
            with col2:
                masa_final_dil = masa_pulpa + agua_necesaria
                st.metric("Masa Final", f"{masa_final_dil:.2f} kg")
            with col3:
                reduccion = brix_inicial - brix_objetivo_dilucion
                st.metric("Reducción °Brix", f"-{reduccion:.1f}%")

    else:
        st.info("👈 Configura los parámetros en el panel lateral y haz clic en **Calcular Balance**")

        # Mostrar información útil mientras no hay cálculo
        st.markdown("### 🎯 Guía Rápida de Uso")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            **1️⃣ Selecciona la fruta**
            - Valores típicos precargados
            - O usa modo personalizado
            """)

        with col2:
            st.markdown("""
            **2️⃣ Ingresa los datos**
            - Masa de pulpa disponible
            - °Brix inicial medido
            - °Brix objetivo deseado
            """)

        with col3:
            st.markdown("""
            **3️⃣ Obtén resultados**
            - Cantidad exacta de azúcar
            - Visualizaciones completas
            - Análisis de sensibilidad
            """)

# ===========================
# TAB 2: FUNDAMENTOS TEÓRICOS
# ===========================

with tab2:
    st.header("📚 Fundamentos de Balance de Materia")

    # Sección 1: ¿Qué son los °Brix?
    st.subheader("1️⃣ ¿Qué son los Grados Brix (°Brix)?")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        Los **grados Brix (°Brix)** son una medida de la concentración de sólidos solubles en un líquido,
        expresada como porcentaje en masa. En la industria alimentaria, principalmente representan
        el contenido de azúcares en jugos, pulpas y néctares de frutas.

        **Definición práctica:**
        - 1°Brix = 1 gramo de sólidos solubles en 100 gramos de solución
        - A 20°C, 1°Brix ≈ 1% de sacarosa en peso

        **Importancia en la industria:**
        - ✅ Control de calidad del producto
        - ✅ Estandarización de procesos
        - ✅ Predicción de rendimientos
        - ✅ Determinación de punto final en concentración
        - ✅ Cálculo de formulaciones
        """)

    with col2:
        st.info("""
        **📏 Medición**

        Se mide con un **refractómetro**,
        que aprovecha la relación
        entre la concentración de
        azúcares y el índice de
        refracción de la luz.

        **Rango típico:**
        - Frutas frescas: 8-20°Brix
        - Néctares: 12-16°Brix
        - Mermeladas: 60-70°Brix
        """)

    st.markdown("---")

    # Tabla de valores típicos
    st.subheader("📊 Valores Típicos de °Brix por Fruta")

    frutas_tabla = obtener_frutas()
    datos_tabla = []
    for fruta, info in frutas_tabla.items():
        if fruta != "Personalizado":
            datos_tabla.append({
                "Fruta": fruta,
                "°Brix Típico": info["brix_inicial"],
                "Categoría": "Alta" if info["brix_inicial"] >= 14 else "Media" if info["brix_inicial"] >= 10 else "Baja"
            })

    df_frutas = pd.DataFrame(datos_tabla)
    st.dataframe(df_frutas, use_container_width=True, hide_index=True)

    st.markdown("---")

    # Sección 2: Balance de Materia
    st.subheader("2️⃣ Principio de Balance de Materia")

    st.markdown("""
    El **balance de materia** se basa en la **Ley de Conservación de la Masa**:

    > *"La masa no se crea ni se destruye, solo se transforma"*

    En nuestro caso específico:
    """)

    st.latex(r"\text{Masa Total Entrada} = \text{Masa Total Salida}")
    st.latex(r"\text{Sólidos Entrada} = \text{Sólidos Salida}")

    st.markdown("### 🔬 Deducción de la Fórmula")

    with st.expander("Ver deducción matemática paso a paso"):
        st.markdown("""
        **Datos conocidos:**
        - $M_i$ = Masa inicial de pulpa (kg)
        - $C_i$ = Concentración inicial (°Brix como decimal)
        - $C_f$ = Concentración final objetivo (°Brix como decimal)
        - $A$ = Azúcar a agregar (kg) - **INCÓGNITA**

        **Paso 1:** Calcular sólidos iniciales en la pulpa
        """)

        st.latex(r"S_i = M_i \times C_i")

        st.markdown("**Paso 2:** Plantear balance de materia total")
        st.latex(r"M_f = M_i + A")

        st.markdown("**Paso 3:** Plantear balance de sólidos")
        st.latex(r"S_f = S_i + A")

        st.markdown("**Paso 4:** Aplicar definición de concentración final")
        st.latex(r"C_f = \frac{S_f}{M_f} = \frac{S_i + A}{M_i + A}")

        st.markdown("**Paso 5:** Despejar A (azúcar a agregar)")
        st.latex(r"C_f(M_i + A) = S_i + A")
        st.latex(r"C_f \cdot M_i + C_f \cdot A = S_i + A")
        st.latex(r"C_f \cdot A - A = S_i - C_f \cdot M_i")
        st.latex(r"A(C_f - 1) = S_i - C_f \cdot M_i")

        st.markdown("**Fórmula final:**")
        st.latex(r"A = \frac{M_i \cdot C_f - S_i}{1 - C_f} = \frac{M_i \cdot C_f - M_i \cdot C_i}{1 - C_f}")

        st.success("✅ Esta es la fórmula implementada en la calculadora")

    # Ejemplo numérico
    st.markdown("### 🧮 Ejemplo Numérico Resuelto")

    with st.expander("Ver ejemplo completo"):
        st.markdown("""
        **Problema:**
        Se tienen 100 kg de pulpa de fresa con 8°Brix. Se desea llevarla a 65°Brix para elaborar mermelada.
        ¿Cuánta azúcar se debe agregar?

        **Solución:**

        **Datos:**
        - $M_i = 100$ kg
        - $C_i = 8\\% = 0.08$
        - $C_f = 65\\% = 0.65$

        **Paso 1:** Sólidos iniciales
        """)
        st.latex(r"S_i = 100 \times 0.08 = 8 \text{ kg}")

        st.markdown("**Paso 2:** Aplicar fórmula")
        st.latex(r"A = \frac{100 \times 0.65 - 8}{1 - 0.65} = \frac{65 - 8}{0.35} = \frac{57}{0.35} = 162.86 \text{ kg}")

        st.markdown("**Paso 3:** Verificación")
        st.latex(r"M_f = 100 + 162.86 = 262.86 \text{ kg}")
        st.latex(r"S_f = 8 + 162.86 = 170.86 \text{ kg}")
        st.latex(r"C_f = \frac{170.86}{262.86} \times 100 = 65.0\%")

        st.success("✅ Verificado: Se necesitan 162.86 kg de azúcar")

    st.markdown("---")

    # Sección 3: Aplicaciones Industriales
    st.subheader("3️⃣ Aplicaciones en la Industria Alimentaria")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **🏭 Casos de Uso Comunes:**

        1. **Elaboración de Mermeladas**
           - Concentración: 60-70°Brix
           - Propósito: Conservación y textura

        2. **Producción de Néctares**
           - Concentración: 12-16°Brix
           - Propósito: Estandarización del sabor

        3. **Concentrados de Fruta**
           - Concentración: 60-72°Brix
           - Propósito: Reducción de volumen para transporte

        4. **Jarabes y Almíbares**
           - Ligero: 20-30°Brix
           - Pesado: 40-50°Brix
           - Propósito: Conservación de frutas
        """)

    with col2:
        st.markdown("""
        **📋 Estándares de Calidad:**

        - **CODEX Alimentarius:** Normas internacionales
        - **FDA:** Regulaciones en Estados Unidos
        - **INVIMA:** Normativa en Colombia

        **💡 Tips Prácticos:**

        - Siempre medir °Brix a 20°C para precisión
        - Considerar pérdidas por evaporación
        - Ajustar según acidez de la fruta
        - Verificar °Brix en producto final
        - Registrar todos los parámetros del proceso
        """)

    st.info("""
    **⚠️ Consideraciones Importantes:**

    - Los °Brix representan TODOS los sólidos solubles, no solo azúcares (incluyen ácidos, sales, proteínas)
    - En frutas, típicamente 80-90% de los sólidos son azúcares
    - La temperatura afecta la medición: calibrar refractómetro a 20°C
    - Durante la cocción, hay pérdida de agua por evaporación que aumenta la concentración
    """)

# ===========================
# TAB 3: EJERCICIOS PRÁCTICOS
# ===========================

with tab3:
    st.header("✏️ Ejercicios Prácticos")
    st.markdown("Pon a prueba tus conocimientos resolviendo problemas de balance de materia")

    col1, col2 = st.columns([2, 1])

    with col1:
        dificultad = st.selectbox(
            "Selecciona el nivel de dificultad",
            ["Básico", "Intermedio", "Avanzado"],
            help="Básico: valores simples | Intermedio: valores moderados | Avanzado: valores complejos"
        )

    with col2:
        if st.session_state.ejercicios_totales > 0:
            porcentaje = (st.session_state.ejercicios_correctos / st.session_state.ejercicios_totales) * 100
            st.metric(
                "Precisión",
                f"{porcentaje:.1f}%",
                f"{st.session_state.ejercicios_correctos}/{st.session_state.ejercicios_totales}"
            )

    st.markdown("---")

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("🎲 Generar Nuevo Ejercicio", type="primary", use_container_width=True):
            st.session_state.ejercicio_actual = generar_ejercicio(dificultad)
            st.session_state.mostrar_solucion = False

    with col2:
        if st.button("🔄 Reiniciar Contador", use_container_width=True):
            st.session_state.ejercicios_correctos = 0
            st.session_state.ejercicios_totales = 0
            st.rerun()

    if st.session_state.ejercicio_actual:
        ejercicio = st.session_state.ejercicio_actual

        st.markdown("### 📝 Problema:")
        st.info(f"""
        Se tienen **{ejercicio['masa']} kg** de pulpa de fruta con una concentración de
        **{ejercicio['brix_inicial']}°Brix**. Se desea ajustar la concentración a
        **{ejercicio['brix_objetivo']}°Brix** agregando azúcar.

        **¿Cuántos kilogramos de azúcar se deben agregar?**
        """)

        col1, col2 = st.columns([2, 1])

        with col1:
            respuesta_usuario = st.number_input(
                "Tu respuesta (kg de azúcar):",
                min_value=0.0,
                step=0.1,
                format="%.3f",
                key=f"respuesta_{id(ejercicio)}"
            )

        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            verificar = st.button("✅ Verificar Respuesta", use_container_width=True)

        if verificar:
            respuesta_correcta = ejercicio['respuesta_correcta']
            tolerancia = respuesta_correcta * 0.02  # 2% de tolerancia

            st.session_state.ejercicios_totales += 1

            if abs(respuesta_usuario - respuesta_correcta) <= tolerancia:
                st.session_state.ejercicios_correctos += 1
                st.success(f"🎉 ¡Correcto! La respuesta es {respuesta_correcta:.3f} kg de azúcar")
                st.balloons()
            else:
                st.error(f"❌ Incorrecto. La respuesta correcta es {respuesta_correcta:.3f} kg de azúcar")
                st.markdown(f"Tu respuesta: {respuesta_usuario:.3f} kg | Diferencia: {abs(respuesta_usuario - respuesta_correcta):.3f} kg")

            # Mostrar solución detallada
            with st.expander("📖 Ver solución detallada"):
                solidos_iniciales = ejercicio['masa'] * (ejercicio['brix_inicial'] / 100)
                masa_final = ejercicio['masa'] + respuesta_correcta
                solidos_finales = solidos_iniciales + respuesta_correcta
                brix_final = (solidos_finales / masa_final) * 100

                st.markdown(f"""
                **Solución paso a paso:**

                1. **Calcular sólidos iniciales:**
                   - Sólidos = {ejercicio['masa']} kg × {ejercicio['brix_inicial']/100:.3f} = {solidos_iniciales:.3f} kg

                2. **Aplicar fórmula:**
                   - A = (Mi × Cf - Si) / (1 - Cf)
                   - A = ({ejercicio['masa']} × {ejercicio['brix_objetivo']/100:.3f} - {solidos_iniciales:.3f}) / (1 - {ejercicio['brix_objetivo']/100:.3f})
                   - A = **{respuesta_correcta:.3f} kg**

                3. **Verificación:**
                   - Masa final = {ejercicio['masa']} + {respuesta_correcta:.3f} = {masa_final:.3f} kg
                   - Sólidos finales = {solidos_iniciales:.3f} + {respuesta_correcta:.3f} = {solidos_finales:.3f} kg
                   - °Brix final = ({solidos_finales:.3f} / {masa_final:.3f}) × 100 = {brix_final:.2f}%
                   - ✅ Objetivo: {ejercicio['brix_objetivo']}%
                """)
    else:
        st.info("👆 Haz clic en 'Generar Nuevo Ejercicio' para comenzar")

# ===========================
# TAB 4: BIBLIOTECA DE CASOS
# ===========================

with tab4:
    st.header("📁 Biblioteca de Casos de Estudio")
    st.markdown("Casos reales de la industria alimentaria con datos típicos de procesamiento")

    casos_df = obtener_casos_estudio()

    # Filtros
    col1, col2 = st.columns(2)

    with col1:
        filtro_fruta = st.multiselect(
            "Filtrar por fruta",
            options=casos_df["Fruta"].unique(),
            default=None
        )

    with col2:
        filtro_aplicacion = st.multiselect(
            "Filtrar por aplicación",
            options=casos_df["Aplicación"].unique(),
            default=None
        )

    # Aplicar filtros
    df_filtrado = casos_df.copy()
    if filtro_fruta:
        df_filtrado = df_filtrado[df_filtrado["Fruta"].isin(filtro_fruta)]
    if filtro_aplicacion:
        df_filtrado = df_filtrado[df_filtrado["Aplicación"].isin(filtro_aplicacion)]

    st.markdown("---")

    # Mostrar tabla
    st.dataframe(
        df_filtrado,
        use_container_width=True,
        hide_index=True,
        column_config={
            "°Brix Inicial": st.column_config.NumberColumn(format="%.1f%%"),
            "°Brix Objetivo": st.column_config.NumberColumn(format="%.1f%%")
        }
    )

    st.markdown("---")

    # Selector de caso para cargar en calculadora
    st.subheader("🔬 Probar un Caso")

    caso_seleccionado = st.selectbox(
        "Selecciona un caso para analizar",
        options=df_filtrado["Producto"].tolist()
    )

    if st.button("📊 Analizar Caso Seleccionado", type="primary"):
        caso = df_filtrado[df_filtrado["Producto"] == caso_seleccionado].iloc[0]

        st.markdown(f"### 📋 Análisis: {caso['Producto']}")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"""
            **Parámetros del Caso:**
            - **Fruta:** {caso['Fruta']}
            - **°Brix Inicial:** {caso['°Brix Inicial']}%
            - **°Brix Objetivo:** {caso['°Brix Objetivo']}%
            - **Aplicación:** {caso['Aplicación']}
            """)

        with col2:
            st.info(f"**Nota Técnica:**\n\n{caso['Notas']}")

        # Realizar cálculo para masa ejemplo de 100 kg
        masa_ejemplo = 100.0
        azucar_necesaria, _ = calcular_azucar(
            masa_ejemplo,
            caso['°Brix Inicial'],
            caso['°Brix Objetivo']
        )

        st.markdown("---")
        st.markdown(f"### 📊 Resultados para {masa_ejemplo} kg de pulpa")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Azúcar Necesaria", f"{azucar_necesaria:.2f} kg")

        with col2:
            masa_final = masa_ejemplo + azucar_necesaria
            st.metric("Masa Final", f"{masa_final:.2f} kg")

        with col3:
            proporcion = (azucar_necesaria / masa_ejemplo) * 100
            st.metric("Proporción", f"{proporcion:.1f}%", help="% de azúcar respecto a la pulpa inicial")

        # Gráficos
        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:
            fig_barras = crear_grafico_comparativo(
                masa_ejemplo,
                caso['°Brix Inicial'],
                azucar_necesaria,
                caso['°Brix Objetivo']
            )
            st.plotly_chart(fig_barras, use_container_width=True)

        with col2:
            fig_circular = crear_grafico_circular(
                masa_ejemplo,
                caso['°Brix Inicial'],
                azucar_necesaria
            )
            st.plotly_chart(fig_circular, use_container_width=True)

# ===========================
# HISTORIAL (SIDEBAR AL FINAL)
# ===========================

with st.sidebar:
    st.markdown("---")
    st.subheader("📜 Historial de Cálculos")

    if st.session_state.historial:
        st.caption(f"Total de cálculos: {len(st.session_state.historial)}")

        # Mostrar últimos 5 cálculos
        for i, calc in enumerate(reversed(st.session_state.historial[-5:])):
            with st.expander(f"{calc['Fruta']} - {calc['Fecha']}", expanded=False):
                st.text(f"Masa: {calc['Masa Pulpa (kg)']} kg")
                st.text(f"°Brix: {calc['°Brix Inicial']}% → {calc['°Brix Objetivo']}%")
                st.text(f"Azúcar: {calc['Azúcar a Agregar (kg)']} kg")

        if len(st.session_state.historial) > 0:
            # Exportar historial
            df_historial = pd.DataFrame(st.session_state.historial)
            csv = df_historial.to_csv(index=False).encode('utf-8')

            st.download_button(
                label="📥 Exportar Historial (CSV)",
                data=csv,
                file_name=f"historial_balance_materia_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )

        if st.button("🗑️ Limpiar Historial", use_container_width=True):
            st.session_state.historial = []
            st.rerun()
    else:
        st.caption("No hay cálculos en el historial")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>🧪 Sistema Interactivo de Balance de Materia v2.0</p>
    <p>Desarrollado para profesionales de la industria alimentaria</p>
</div>
""", unsafe_allow_html=True)
