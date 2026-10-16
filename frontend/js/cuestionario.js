/* ========================================================== */
/* MÓDULO DE CUESTIONARIOS - StudyAI (Vanilla JS)             */
/* ========================================================== */

document.addEventListener('DOMContentLoaded', () => {
    const contenedorCuestionario = document.querySelector('.contenedor-principal');
    
    if (contenedorCuestionario && window.location.pathname.includes('/cuestionario')) {
        console.log("Módulo de cuestionario interactivo inicializado.");
        
        // Lógica sencilla para alternar estados o verificar respuestas interactivas
        const opcionesRespuesta = document.querySelectorAll('.opcion-respuesta');
        opcionesRespuesta.forEach(opcion => {
            opcion.addEventListener('click', () => {
                opcionesRespuesta.forEach(o => o.style.borderColor = 'var(--color-border)');
                opcion.style.borderColor = 'var(--color-primary)';
            });
        });
    }
});