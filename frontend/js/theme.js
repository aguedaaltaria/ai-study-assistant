/* ========================================================== */
/* GESTOR GLOBAL DE TEMAS (Modo Claro / Oscuro) - StudyAI     */
/* ========================================================== */

document.addEventListener('DOMContentLoaded', () => {
    const elementoHtmlRaiz = document.documentElement;
    
    // 1. Cargar la preferencia de tema guardada previamente en el navegador
    let temaGuardadoEnNavegador = window.localStorage.getItem('studyai_theme');
    
    if (temaGuardadoEnNavegador === null) {
        temaGuardadoEnNavegador = 'light';
    }
    
    elementoHtmlRaiz.setAttribute('data-theme', temaGuardadoEnNavegador);
    
    // 2. Buscar todos los botones de alternancia de tema en la página actual
    const coleccionBotonesDeTema = document.querySelectorAll('#btn-toggle-theme, .btn-toggle-theme');

    coleccionBotonesDeTema.forEach(botonActual => {
        actualizarTextoYAparienciaDelBoton(botonActual, temaGuardadoEnNavegador);

        botonActual.addEventListener('click', () => {
            const temaActualEnDocumento = elementoHtmlRaiz.getAttribute('data-theme');
            let nuevoTemaAConfigurar;

            if (temaActualEnDocumento === 'dark') {
                nuevoTemaAConfigurar = 'light';
            } else {
                nuevoTemaAConfigurar = 'dark';
            }

            // Aplicar el nuevo tema al documento HTML y guardar la preferencia
            elementoHtmlRaiz.setAttribute('data-theme', nuevoTemaAConfigurar);
            window.localStorage.setItem('studyai_theme', nuevoTemaAConfigurar);

            // Actualizar el texto y la apariencia en todos los botones de tema de la vista
            coleccionBotonesDeTema.forEach(botonIndividual => {
                actualizarTextoYAparienciaDelBoton(botonIndividual, nuevoTemaAConfigurar);
            });
        });
    });
});

function actualizarTextoYAparienciaDelBoton(botonObjetivo, temaActual) {
    if (temaActual === 'dark') {
        botonObjetivo.innerHTML = '☀️ Modo Claro';
    } else {
        botonObjetivo.innerHTML = '🌙 Modo Oscuro';
    }
}