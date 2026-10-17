document.addEventListener('DOMContentLoaded', () => {
    console.log("¡StudyAI cargado correctamente con JavaScript vainilla!");

    // Cargar y renderizar cuestionarios dinámicamente si estamos en el panel
    const contenedorDinamico = document.getElementById('lista-cuestionarios-dinamica');
    
    if (contenedorDinamico) {
        fetch('/api/cuestionarios')
            .then(response => response.json())
            .then(data => {
                contenedorDinamico.innerHTML = ''; // Limpiamos el texto de carga
                
                if (data.length === 0) {
                    contenedorDinamico.innerHTML = `<p class="texto-vacio-cuestionarios">Aún no tienes cuestionarios guardados. ¡Crea el primero abajo!</p>`;
                    return;
                }

                data.forEach(item => {
                    const tarjeta = document.createElement('div');
                    tarjeta.className = 'tarjeta-cuestionario-item';
                    tarjeta.innerHTML = `
                        <h4>${item.titulo_cuestionario}</h4>
                        <p>${item.contenido_pregunta}</p>
                    `;
                    contenedorDinamico.appendChild(tarjeta);
                });
            })
            .catch(error => {
                console.error('Error al cargar los cuestionarios:', error);
                contenedorDinamico.innerHTML = `<p class="texto-vacio-cuestionarios">Error al cargar los datos.</p>`;
            });
    }

    // Efecto de realce en inputs de formularios
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
});