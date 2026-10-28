# 🧠 StudyAI - Asistente Inteligente de Estudio y Repaso

**StudyAI** es una aplicación web minimalista, modular y segura desarrollada con **Flask** y **SQLite nativo**, diseñada para potenciar el aprendizaje mediante la generación automática de tarjetas de estudio (*flashcards*) potenciadas por la Inteligencia Artificial de Google Gemini, un modo repaso interactivo con mezcla aleatoria, y análisis estadístico avanzado.

---

## 🛠️ Tecnologías y Arquitectura

El proyecto sigue una estricta filosofía modular con archivos limpios y legibles:
* **Backend**: Python con Flask, gestión de sesiones seguras y base de datos relacional SQLite nativa (`sqlite3`).
* **Inteligencia Artificial**: SDK oficial de Google GenAI (`google-genai`) para la generación de contenido estructurado.
* **Frontend**: HTML5, CSS3 modular (diseño adaptativo con soporte para modo claro y oscuro persistente) y JavaScript vainilla (`fetch API`).
* **Control de Versiones**: Jujutsu (`jj`) y Git.
* **Gestión de Entorno**: `uv` para la ejecución rápida de dependencias.

---

## 🚀 Funcionalidades Principales

1. **Autenticación Segura**: Sistema nativo de registro y acceso de usuarios con contraseñas cifradas (*Werkzeug security*) y control de sesiones.
2. **Generación con Gemini IA**: Creación automática de cuestionarios y tarjetas técnicas precisas con clasificación automática por categorías.
3. **Panel de Control Dinámico**: Cuadrícula interactiva con búsqueda en tiempo real, tarjetas desplegables/minimizables y eliminación de registros.
4. **Modo Repaso Interactivo (`/repaso`)**: Tarjetas de estudio con filtrado por categorías, búsqueda instantánea, revelación de respuestas y mezcla aleatoria (*Fisher-Yates*).
5. **Panel de Estadísticas Avanzadas**: Métricas globales de estudio y desglose visual con barras de distribución porcentual por categoría.
6. **Portabilidad de Datos**: Herramientas integradas para exportar respaldos seguros en formato JSON y cargar nuevos lotes mediante importación validada.
7. **Diseño Global de Temas**: Alternancia fluida entre Modo Claro y Modo Oscuro con persistencia automática en `localStorage`.

---

## ⚙️ Instrucciones de Instalación y Ejecución

Sigue estos pasos para poner en marcha el proyecto en tu entorno local:

1. **Clonar o situarse en la carpeta del repositorio**:
   ```bash
   cd ~/Documents/ai-study-assistant
