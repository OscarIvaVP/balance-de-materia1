# 🧪 Sistema Interactivo de Balance de Materia

## Ajuste de °Brix en Pulpas de Frutas

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

Una aplicación web interactiva y educativa para calcular balances de materia en el procesamiento de pulpas de frutas, específicamente para el ajuste de concentración de sólidos solubles (°Brix). Desarrollada con Streamlit y diseñada para profesionales de la industria alimentaria y estudiantes de ingeniería agroindustrial.

---

## 📋 Tabla de Contenidos

- [Características Principales](#-características-principales)
- [Demo en Vivo](#-demo-en-vivo)
- [Tecnologías Utilizadas](#-tecnologías-utilizadas)
- [Instalación](#-instalación)
- [Uso de la Aplicación](#-uso-de-la-aplicación)
- [Funcionalidades Detalladas](#-funcionalidades-detalladas)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Casos de Uso](#-casos-de-uso)
- [Fundamento Técnico](#-fundamento-técnico)
- [Contribución](#-contribución)
- [Licencia](#-licencia)
- [Autor](#-autor)

---

## ✨ Características Principales

### 🎯 Calculadora Profesional
- **Selector de frutas precargadas**: 10 frutas con valores típicos de °Brix
- **Cálculos precisos**: Balance de materia completo con verificación
- **Visualizaciones interactivas**: Gráficos comparativos, circulares y de sensibilidad
- **Diagrama de flujo**: Representación visual del proceso
- **Calculadora de dilución**: Para reducir °Brix agregando agua
- **Historial de cálculos**: Registro de todas las operaciones con exportación a CSV

### 📚 Contenido Educativo
- **Fundamentos teóricos**: Explicación completa de °Brix y balance de materia
- **Deducción matemática**: Paso a paso de la fórmula con notación LaTeX
- **Ejemplos resueltos**: Casos prácticos completamente desarrollados
- **Aplicaciones industriales**: Casos reales de la industria alimentaria

### ✏️ Sistema de Ejercicios
- **Generador de problemas**: Ejercicios aleatorios con 3 niveles de dificultad
- **Validación automática**: Verificación inmediata de respuestas
- **Soluciones detalladas**: Explicación paso a paso de cada ejercicio
- **Sistema de puntuación**: Contador de precisión y progreso

### 📁 Biblioteca de Casos
- **8 casos reales**: Mermeladas, néctares, concentrados, almíbares
- **Filtros inteligentes**: Por tipo de fruta y aplicación
- **Análisis completo**: Gráficos y cálculos para cada caso
- **Notas técnicas**: Consideraciones prácticas de cada proceso

---

## 🌐 Demo en Vivo

**Accede a la aplicación desplegada:**
[Sistema de Balance de Materia en Streamlit Cloud](https://tu-app.streamlit.app) *(Actualiza con tu URL una vez desplegada)*

---

## 🛠 Tecnologías Utilizadas

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **Python** | 3.8+ | Lenguaje de programación principal |
| **Streamlit** | 1.28+ | Framework para la interfaz web interactiva |
| **Plotly** | 5.0+ | Gráficos interactivos y visualizaciones |
| **Pandas** | 2.0+ | Manejo y análisis de datos |
| **NumPy** | 1.24+ | Cálculos numéricos y arrays |

---

## 📦 Instalación

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git (opcional, para clonar el repositorio)

### Paso 1: Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/balance-de-materia1.git
cd balance-de-materia1
```

### Paso 2: Crear un Entorno Virtual (Recomendado)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Paso 3: Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Ejecutar la Aplicación

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

---

## 🚀 Uso de la Aplicación

### Navegación Principal

La aplicación está organizada en **4 pestañas principales**:

#### 1️⃣ Calculadora Profesional
1. **Selecciona una fruta** del menú lateral (o usa "Personalizado")
2. **Ingresa los parámetros**:
   - Masa inicial de la pulpa (kg)
   - °Brix inicial (%)
   - °Brix objetivo (%)
3. **Haz clic en "Calcular Balance"**
4. **Visualiza los resultados**:
   - Cantidad de azúcar necesaria
   - Métricas clave
   - Gráficos interactivos
   - Diagrama de flujo del proceso

#### 2️⃣ Fundamentos Teóricos
- Explora conceptos de °Brix y balance de materia
- Revisa la deducción matemática de las fórmulas
- Consulta valores típicos por tipo de fruta
- Aprende sobre aplicaciones industriales

#### 3️⃣ Ejercicios Prácticos
1. Selecciona el nivel de dificultad
2. Genera un nuevo ejercicio
3. Ingresa tu respuesta
4. Verifica y aprende de la solución detallada
5. Mejora tu precisión con la práctica

#### 4️⃣ Biblioteca de Casos
1. Filtra por fruta o aplicación
2. Selecciona un caso de estudio
3. Analiza los parámetros y resultados
4. Visualiza gráficos comparativos

---

## 📊 Funcionalidades Detalladas

### Tab 1: Calculadora Profesional

**Panel de Control (Sidebar)**
- Selector de frutas con valores precargados:
  - Manzana, Naranja, Piña, Mango, Fresa
  - Durazno, Uva, Maracuyá, Guayaba
  - Modo Personalizado
- Inputs numéricos con validación
- Calculadora adicional de dilución

**Visualizaciones**
- **Métricas Destacadas**: 4 tarjetas con valores clave
- **Diagrama de Flujo**: Entrada → Proceso → Salida
- **Gráfico de Barras**: Composición antes vs después
- **Gráfico Circular**: Distribución de componentes
- **Gráfico de Sensibilidad**: Análisis interactivo con Plotly

**Historial**
- Registro de todos los cálculos
- Muestra últimos 5 cálculos
- Exportación a CSV con timestamp
- Limpieza de historial

### Tab 2: Fundamentos Teóricos

**Sección 1: ¿Qué son los °Brix?**
- Definición técnica y práctica
- Importancia en la industria
- Métodos de medición
- Tabla de valores típicos por fruta

**Sección 2: Balance de Materia**
- Ley de conservación de la masa
- Deducción matemática paso a paso
- Ecuaciones en formato LaTeX
- Ejemplo numérico completo

**Sección 3: Aplicaciones Industriales**
- Mermeladas (60-70°Brix)
- Néctares (12-16°Brix)
- Concentrados (60-72°Brix)
- Jarabes y almíbares (20-50°Brix)
- Estándares de calidad (CODEX, FDA, INVIMA)
- Tips prácticos para profesionales

### Tab 3: Ejercicios Prácticos

**Generador de Ejercicios**
- **Básico**: Masas 10-100 kg, incrementos 3-10°Brix
- **Intermedio**: Masas 50-500 kg, incrementos 5-20°Brix
- **Avanzado**: Masas 100-1000 kg, incrementos 10-40°Brix

**Sistema de Validación**
- Tolerancia del 2% en las respuestas
- Feedback visual inmediato
- Animación de celebración para respuestas correctas
- Contador de precisión en tiempo real

**Soluciones Detalladas**
- Cálculo de sólidos iniciales
- Aplicación de la fórmula
- Verificación del resultado
- Todos los pasos explicados

### Tab 4: Biblioteca de Casos

**Casos de Estudio Incluidos**
1. **Mermelada de fresa** (8% → 65%)
2. **Néctar de durazno** (10.5% → 14%)
3. **Concentrado de manzana** (12% → 70%)
4. **Jalea de uva** (16% → 62%)
5. **Salsa de tomate** (5% → 28%)
6. **Jugo de naranja** (11.5% → 12%)
7. **Almíbar ligero** (8% → 20%)
8. **Almíbar pesado** (8% → 40%)

**Análisis de Casos**
- Parámetros del proceso
- Notas técnicas específicas
- Cálculos para 100 kg de referencia
- Gráficos comparativos y circulares
- Proporciones y rendimientos

---

## 📁 Estructura del Proyecto

```
balance-de-materia1/
│
├── app.py                  # Aplicación principal de Streamlit
├── requirements.txt        # Dependencias del proyecto
├── README.md              # Este archivo
│
└── .streamlit/            # (Opcional) Configuración de Streamlit
    └── config.toml        # Tema y configuraciones personalizadas
```

### Estructura del Código (app.py)

```python
# 1. Imports y configuración
# 2. Datos de referencia (frutas, casos de estudio)
# 3. Funciones de cálculo
#    - calcular_azucar()
#    - calcular_dilucion()
# 4. Funciones de visualización
#    - crear_grafico_comparativo()
#    - crear_grafico_circular()
#    - crear_grafico_interactivo()
#    - crear_diagrama_flujo()
# 5. Generador de ejercicios
# 6. Inicialización de session_state
# 7. Interfaz principal con 4 tabs
# 8. Historial y footer
```

---

## 🎯 Casos de Uso

### Para Estudiantes
- Aprender los fundamentos de balance de materia
- Practicar con ejercicios de diferentes niveles
- Visualizar conceptos abstractos con gráficos
- Verificar cálculos de tareas y exámenes

### Para Profesionales de la Industria
- Calcular formulaciones de productos
- Estandarizar procesos de producción
- Consultar casos de referencia
- Exportar datos para reportes
- Optimizar el uso de materias primas

### Para Docentes
- Herramienta de enseñanza interactiva
- Generador automático de ejercicios
- Ejemplos visuales para clases
- Casos de estudio reales

### Para Investigadores
- Calcular formulaciones experimentales
- Documentar procesos con exportación de datos
- Analizar sensibilidad de variables
- Comparar diferentes escenarios

---

## 🔬 Fundamento Técnico

### Fórmula Principal

La aplicación utiliza la siguiente ecuación para calcular la cantidad de azúcar a agregar:

$$A = \frac{M_i \cdot C_f - M_i \cdot C_i}{1 - C_f}$$

Donde:
- **A** = Azúcar a agregar (kg)
- **M<sub>i</sub>** = Masa inicial de pulpa (kg)
- **C<sub>i</sub>** = Concentración inicial (decimal)
- **C<sub>f</sub>** = Concentración final objetivo (decimal)

### Principios del Balance de Materia

1. **Conservación de la masa total**:
   M<sub>final</sub> = M<sub>inicial</sub> + A

2. **Conservación de sólidos**:
   S<sub>final</sub> = S<sub>inicial</sub> + A

3. **Definición de concentración**:
   C = S / M

### Calculadora de Dilución

Para reducir °Brix agregando agua:

$$W = M_i \cdot \frac{C_i - C_f}{C_f}$$

Donde:
- **W** = Agua a agregar (kg)
- **M<sub>i</sub>** = Masa inicial (kg)
- **C<sub>i</sub>** = Concentración inicial (decimal)
- **C<sub>f</sub>** = Concentración final (decimal)

---

## 🤝 Contribución

Las contribuciones son bienvenidas. Si deseas contribuir:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

### Ideas para Contribuir
- Agregar más frutas a la base de datos
- Incluir más casos de estudio
- Agregar calculadoras adicionales (evaporación, mezclas)
- Mejorar visualizaciones
- Traducción a otros idiomas
- Optimizaciones de rendimiento

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

## 👨‍💻 Autor

**Curso de Producción Agroindustrial**
Universidad Santo Tomás - USTA
Periodo: 2025-2

### Contacto
- **Institución**: Universidad Santo Tomás
- **Programa**: Ingeniería Agroindustrial
- **Curso**: Balance de Materia

---

## 🙏 Agradecimientos

- A la comunidad de Streamlit por el excelente framework
- A Plotly por las herramientas de visualización
- A todos los estudiantes y profesionales que utilizan esta herramienta

---

## 📝 Notas de Versión

### v2.0 (Actual)
- ✅ Interfaz completamente rediseñada con tabs
- ✅ 4 módulos principales: Calculadora, Teoría, Ejercicios, Casos
- ✅ Visualizaciones interactivas con Plotly
- ✅ Sistema de ejercicios con validación automática
- ✅ Biblioteca de 8 casos de estudio reales
- ✅ Historial de cálculos con exportación
- ✅ Calculadora de dilución adicional

### v1.0 (Anterior)
- Calculadora básica de balance de materia
- Interfaz simple de 2 columnas
- Cálculo y verificación básica

---

## 🔗 Enlaces Útiles

- [Documentación de Streamlit](https://docs.streamlit.io/)
- [Plotly Python](https://plotly.com/python/)
- [CODEX Alimentarius](http://www.fao.org/fao-who-codexalimentarius/)
- [Balance de Materia - Wikipedia](https://es.wikipedia.org/wiki/Balance_de_materia)

---

## ❓ Preguntas Frecuentes

**P: ¿Puedo usar esta aplicación para calcular otros tipos de mezclas?**
R: Actualmente está optimizada para ajuste de °Brix en pulpas, pero los principios son aplicables a otros balances de materia similares.

**P: ¿Los datos de frutas son precisos?**
R: Los valores de °Brix son rangos típicos. Las frutas reales pueden variar según variedad, madurez y condiciones de cultivo.

**P: ¿Cómo exporto mis cálculos?**
R: En el historial lateral, haz clic en "Exportar Historial (CSV)" para descargar todos tus cálculos.

**P: ¿La aplicación funciona offline?**
R: Sí, si la ejecutas localmente. La versión web requiere conexión a internet.

**P: ¿Puedo agregar mis propias frutas?**
R: Usa la opción "Personalizado" para ingresar cualquier valor de °Brix inicial.

---

<div align="center">

**⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub ⭐**

Desarrollado con ❤️ para la comunidad de ingeniería agroindustrial

[Reportar un problema](https://github.com/tu-usuario/balance-de-materia1/issues) • [Solicitar una funcionalidad](https://github.com/tu-usuario/balance-de-materia1/issues)

</div>
