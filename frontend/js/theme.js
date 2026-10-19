/* ========================================================== */
/* GESTOR GLOBAL DE TEMAS (Modo Claro / Oscuro) - StudyAI     */
/* ========================================================== */

document.addEventListener('DOMContentLoaded', () => {
    const htmlElement = document.documentElement;
    
    // 1. Cargar preferencia guardada previamente en el navegador
    const temaGuardado = localStorage.getItem('studyai_theme') || 'light';
    htmlElement.setAttribute('data-theme', temaGuardado);
    
    // 2. Buscar todos los botones de toggle de tema en la página actual
    const botonesTema = document.querySelectorAll('#btn-toggle-theme, .btn-toggle-theme');

    botonesTema.forEach(boton => {
        actualizarTextoBoton(boton, temaGuardado);

        boton.addEventListener('click', () => {
            const temaActual = htmlElement.getAttribute('data-theme');
            const nuevoTema = temaActual === 'dark' ? 'light' : 'dark';

            // Aplicar nuevo tema y guardar preferencia
            htmlElement.setAttribute('data-theme', nuevoTema);
            localStorage.setItem('studyai_theme', nuevoTema);

            // Actualizar texto e ícono en todos los botones de la vista
            botonesTema.forEach(b => actualizarTextoBoton(b, nuevoTema));
        });
    });
});

function actualizarTextoBoton(boton, tema) {
    if (tema === 'dark') {
        boton.innerHTML = '☀️ Modo Claro';
    } else {
        boton.innerHTML = '🌙 Modo Oscuro';
    }
}