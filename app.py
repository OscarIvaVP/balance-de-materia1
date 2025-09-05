import streamlit as st

def calcular_azucar(masa_pulpa_inicial, brix_inicial, brix_objetivo):
    """
    Calcula la cantidad de azúcar (en kg) necesaria para agregar a la pulpa 
    y alcanzar los °Brix objetivo.

    La fórmula se deriva del balance de masa:
    Brix_objetivo = (Sólidos_iniciales + Azúcar_agregada) / (Masa_inicial + Azúcar_agregada)
    """
    # Convertir porcentajes a decimales para los cálculos
    concentracion_inicial = brix_inicial / 100.0
    concentracion_objetivo = brix_objetivo / 100.0

    # Validar que el objetivo sea lógicamente alcanzable
    if concentracion_objetivo <= concentracion_inicial:
        return None, "Los °Brix objetivo deben ser mayores que los iniciales."

    # Calcular la masa inicial de sólidos (azúcar) en la pulpa
    solidos_iniciales = masa_pulpa_inicial * concentracion_inicial
    
    # Despejar la cantidad de azúcar a agregar ('A') de la ecuación de balance
    # A = (Masa_inicial * Conc_objetivo - Sólidos_iniciales) / (1 - Conc_objetivo)
    try:
        azucar_a_agregar = (masa_pulpa_inicial * concentracion_objetivo - solidos_iniciales) / (1 - concentracion_objetivo)
    except ZeroDivisionError:
        return None, "Los °Brix objetivo no pueden ser 100%."
        
    return azucar_a_agregar, None

# --- Configuración de la página de Streamlit ---
st.set_page_config(layout="wide", page_title="Calculadora de °Brix")

# --- Interfaz de la aplicación ---
st.title("Calculadora de Balance de Masa para Ajuste de °Brix")

st.write("""
Esta aplicación web resuelve un problema común en la industria de alimentos: determinar cuánta azúcar se debe agregar a una pulpa de fruta para alcanzar una concentración de sólidos (°Brix) deseada.
""")
st.markdown("---")

# Columnas para una mejor distribución de los elementos
col1, col2 = st.columns([1, 1])

with col1:
    st.header("Datos de Entrada")
    masa_pulpa = st.number_input(
        "Masa inicial de la pulpa (kg)", 
        min_value=0.1, 
        value=50.0, 
        step=1.0,
        help="Introduce la cantidad total de pulpa que tienes actualmente."
    )
    brix_inicial = st.number_input(
        "°Brix iniciales (%)", 
        min_value=0.0, 
        max_value=99.9,
        value=7.0, 
        step=0.1,
        help="Introduce el porcentaje de sólidos disueltos medido en la pulpa."
    )
    brix_objetivo = st.number_input(
        "°Brix objetivo (%)", 
        min_value=0.0, 
        max_value=99.9,
        value=10.0, 
        step=0.1,
        help="Introduce el porcentaje de sólidos disueltos que deseas alcanzar."
    )

    if st.button("Calcular Azúcar a Agregar", type="primary"):
        cantidad_azucar, error = calcular_azucar(masa_pulpa, brix_inicial, brix_objetivo)
        
        # Almacenar el resultado en el estado de la sesión para mostrarlo en la otra columna
        st.session_state.cantidad_azucar = cantidad_azucar
        st.session_state.error = error
        st.session_state.run_calculation = True

with col2:
    st.header("Resultados")
    # Verificar si el cálculo se ha ejecutado
    if 'run_calculation' in st.session_state and st.session_state.run_calculation:
        cantidad_azucar = st.session_state.cantidad_azucar
        error = st.session_state.error

        if error:
            st.error(f"**Error:** {error}")
        else:
            st.success(f"Se deben agregar **{cantidad_azucar:.3f} kg** de azúcar.")
            
            st.subheader("Verificación del Resultado")
            
            solidos_iniciales = masa_pulpa * (brix_inicial / 100)
            masa_final = masa_pulpa + cantidad_azucar
            solidos_finales = solidos_iniciales + cantidad_azucar
            brix_final_verificado = (solidos_finales / masa_final) * 100

            st.write(f"""
            - **Masa total final:** {masa_pulpa:.2f} kg (pulpa) + {cantidad_azucar:.3f} kg (azúcar) = **{masa_final:.3f} kg**
            - **Sólidos totales finales:** {solidos_iniciales:.3f} kg (en pulpa) + {cantidad_azucar:.3f} kg (azúcar) = **{solidos_finales:.3f} kg**
            - **°Brix finales verificados:** ({solidos_finales:.3f} kg / {masa_final:.3f} kg) * 100 = **{brix_final_verificado:.2f} %**
            """)
    else:
        st.info("Ingresa los datos y haz clic en el botón para ver el resultado.")
