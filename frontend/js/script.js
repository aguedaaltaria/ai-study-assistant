/* ========================================================== */
/* SCRIPT PRINCIPAL - StudyAI (Vanilla JS)                    */
/* ========================================================== */

document.addEventListener('DOMContentLoaded', () => {
    console.log("¡StudyAI cargado correctamente con JavaScript vainilla!");

    // 1. Efecto de realce dinámico en inputs de formularios
    const inputsFormulario = document.querySelectorAll('.grupo-formulario input');
    
    inputsFormulario.forEach(input => {
        input.addEventListener('focus', () => {
            input.style.borderColor = 'var(--color-primary)';
        });
        
        input.addEventListener('blur', () => {
            if (!input.value) {
                input.style.borderColor = 'var(--color-border)';
            }
        });
    });

    // 2. Validación simple en tiempo real para contraseñas o campos obligatorios
    const formularios = document.querySelectorAll('form');
    
    formularios.forEach(form => {
        form.addEventListener('submit', (evento) => {
            const inputsRequeridos = form.querySelectorAll('input[required]');
            let formularioValido = true;

            inputsRequeridos.forEach(input => {
                if (!input.value.trim()) {
                    formularioValido = false;
                    input.style.borderColor = '#ef4444'; // Color de alerta sutil
                }
            });

            if (!formularioValido) {
                evento.preventDefault();
                alert('Por favor, completa todos los campos requeridos antes de continuar.');
            }
        });
    });
});