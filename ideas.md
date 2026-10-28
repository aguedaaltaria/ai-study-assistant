# 💡 Ideas y Mejoras Futuras para StudyAI (Roadmap v2.0)

Este documento recopila posibles características, optimizaciones y expansiones para implementar en futuras versiones del asistente de estudio.

---

## 🚀 1. Mejoras de Inteligencia Artificial (Gemini API)
- [ ] **Generación de cuestionarios por lotes**: Permitir que la IA genere un conjunto de 5 o 10 tarjetas relacionadas a partir de un documento PDF o un texto largo pegado por el usuario.
- [ ] **Modo Explicación Profunda**: Añadir un botón en el Modo Repaso que utilice la API de Gemini para reexplicar o dar ejemplos adicionales sobre una pregunta en la que el usuario haya fallado.
- [ ] **Sugerencia de Categorías Inteligentes**: Mejorar el prompt para que la IA clasifique automáticamente el contenido dentro de una taxonomía más amplia predefinida por el sistema.

---

## 📊 2. Analítica y Gamificación
- [ ] **Gráficos Estadísticos Interactivos**: Integrar una librería ligera (como Chart.js o gráficos SVG personalizados) para mostrar la evolución semanal de estudio y el porcentaje de aciertos en el tiempo.
- [ ] **Sistema de Rachas (Streak Counter)**: Rastrear los días consecutivos que el usuario entra a repasar y mostrar una insignia de fuego con animación en el panel principal.
- [ ] **Niveles de Dominio por Tarjeta**: Implementar un algoritmo de repetición espaciada simple (tipo Leitner o SM-2) clasificado por niveles de dificultad (Fácil, Medio, Difícil).

---

## 🛠️ 3. Experiencia de Usuario y Accesibilidad (UX / UI)
- [ ] **Atajos de Teclado en Modo Repaso**: Permitir usar la barra espaciadora para voltear la tarjeta y las flechas del teclado o teclas numéricas para marcar "Lo sé" o "Repasar luego".
- [ ] **Editor de Cuestionarios Manuales**: Añadir un formulario flotante o vista dedicada para que el usuario pueda editar directamente el texto, título o categoría de una tarjeta guardada sin tener que borrarla y recrearla.
- [ ] **Soporte Multiidioma**: Traducir la interfaz completa al inglés y otros idiomas mediante archivos de configuración locales.

---

## 📦 4. Portabilidad y Sincronización Avanzada
- [ ] **Respaldo Automático en SQLite Local**: Añadir una opción de configuración para descargar copias de seguridad automáticas de la base de datos completa con un solo clic.
- [ ] **Soporte para Importación CSV**: Permitir importar cuestionarios masivamente no solo desde JSON, sino también desde archivos planos CSV o tablas de Excel.

---
*Documento creado para la expansión continua de StudyAI.*