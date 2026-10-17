/* ========================================================== */
/* SCRIPT PRINCIPAL - StudyAI (Grid y Categorías Dinámicas)   */
/* ========================================================== */

document.addEventListener('DOMContentLoaded', () => {
    console.log("¡StudyAI cargado correctamente con JavaScript vainilla!");

    const contenedorDinamico = document.getElementById('lista-cuestionarios-dinamica');
    
    if (contenedorDinamico) {
        fetch('/api/cuestionarios')
            .then(response => response.json())
            .then(data => {
                contenedorDinamico.innerHTML = ''; 
                
                if (data.length === 0) {
                    contenedorDinamico.innerHTML = `<p class="texto-vacio-cuestionarios" style="grid-column: 1 / -1;">Aún no tienes cuestionarios guardados. ¡Crea el primero abajo!</p>`;
                    return;
                }

                // Agrupación limpia y transparente basada estrictamente en la base de datos
                const categoriasMap = {};

                data.forEach(item => {
                    const categoria = item.categoria || "General";

                    if (!categoriasMap[categoria]) {
                        categoriasMap[categoria] = [];
                    }
                    categoriasMap[categoria].push(item);
                });

                // 2. Renderizar tarjetas cuadradas en grid
                for (const [nombreCategoria, items] of Object.entries(categoriasMap)) {
                    const seccionCat = document.createElement('div');
                    seccionCat.className = 'seccion-categoria';

                    const cabeceraCat = document.createElement('div');
                    cabeceraCat.className = 'cabecera-categoria';
                    cabeceraCat.innerHTML = `
                        <div style="font-size: 1.5rem;">📚</div>
                        <h3>${nombreCategoria}</h3>
                        <span style="font-size: 0.75rem; background: var(--color-background); padding: 0.15rem 0.4rem; border-radius: 10px; color: var(--color-text-muted);">${items.length} preg.</span>
                        <span class="icono-minimizar" style="font-size: 0.75rem; color: var(--color-primary); font-weight: bold;">▼ Ver</span>
                    `;

                    const contenidoCat = document.createElement('div');
                    contenidoCat.className = 'contenido-categoria minimizado';

                    // Lógica para expandir/contraer la categoría en la cuadrícula
                    cabeceraCat.addEventListener('click', () => {
                        const estaMinimizado = contenidoCat.classList.contains('minimizado');
                        
                        document.querySelectorAll('.contenido-categoria').forEach(el => el.classList.add('minimizado'));
                        document.querySelectorAll('.seccion-categoria').forEach(el => el.classList.remove('activa'));
                        document.querySelectorAll('.icono-minimizar').forEach(el => el.textContent = '▼ Ver');

                        if (estaMinimizado) {
                            contenidoCat.classList.remove('minimizado');
                            seccionCat.classList.add('activa');
                            cabeceraCat.querySelector('.icono-minimizar').textContent = '▲ Ocultar';
                        }
                    });

                    items.forEach(item => {
                        const tarjeta = document.createElement('div');
                        tarjeta.className = 'tarjeta-cuestionario-item';
                        
                        let contenidoFormateado = item.contenido_pregunta
                            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                            .replace(/\n/g, '<br>');

                        tarjeta.innerHTML = `
                            <h4 style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; cursor: pointer;">
                                <span style="font-size: 0.95rem; color: var(--color-primary);">${item.titulo_cuestionario}</span>
                                <div style="display: flex; gap: 0.75rem; align-items: center;">
                                    <span class="icono-minimizar-tarjeta" style="font-size: 0.85rem; color: var(--color-primary); font-weight: bold;" title="Minimizar/Expandir">▲</span>
                                    <form action="/eliminar-cuestionario/${item.id_cuestionario}" method="POST" style="display: inline;" onsubmit="event.stopPropagation();">
                                        <button type="submit" style="background: none; border: none; color: #ef4444; font-size: 1.1rem; font-weight: bold; cursor: pointer;" title="Eliminar pregunta">×</button>
                                    </form>
                                </div>
                            </h4>
                            <div class="cuerpo-tarjeta minimizado" style="font-size: 0.9rem; color: var(--color-text-muted); line-height: 1.5; margin-top: 0.5rem; border-top: 1px dashed var(--color-border); padding-top: 0.5rem;">
                                ${contenidoFormateado}
                            </div>
                        `;

                        // Funcionalidad para minimizar/expandir cada pregunta individualmente con ▲ y ▼
                        const btnMinimizarTarjeta = tarjeta.querySelector('.icono-minimizar-tarjeta');
                        const cuerpoTarjeta = tarjeta.querySelector('.cuerpo-tarjeta');
                        const cabeceraTarjeta = tarjeta.querySelector('h4');

                        const toggleTarjeta = (e) => {
                            e.stopPropagation();
                            cuerpoTarjeta.classList.toggle('minimizado');
                            btnMinimizarTarjeta.textContent = cuerpoTarjeta.classList.contains('minimizado') ? '▲' : '▼';
                        };

                        btnMinimizarTarjeta.addEventListener('click', toggleTarjeta);
                        cabeceraTarjeta.addEventListener('click', toggleTarjeta);

                        contenidoCat.appendChild(tarjeta);
                    });

                    seccionCat.appendChild(cabeceraCat);
                    seccionCat.appendChild(contenidoCat);
                    contenedorDinamico.appendChild(seccionCat);
                }
            })
            .catch(error => {
                console.error('Error al cargar los cuestionarios:', error);
                contenedorDinamico.innerHTML = `<p class="texto-vacio-cuestionarios" style="grid-column: 1 / -1;">Error al cargar los datos.</p>`;
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

    // Prevenir doble envío en formulario de IA
    const formularioIa = document.querySelector('form[action="/generar-cuestionario-ia"]');
    if (formularioIa) {
        formularioIa.addEventListener('submit', (e) => {
            const boton = formularioIa.querySelector('button[type="submit"]');
            if (boton.dataset.enviando === 'true') {
                e.preventDefault();
                return;
            }
            boton.dataset.enviando = 'true';
            boton.disabled = true;
            boton.textContent = 'Generando con IA... (Espere un momento)';
            boton.style.opacity = '0.7';
            boton.style.cursor = 'not-allowed';
        });
    }
});