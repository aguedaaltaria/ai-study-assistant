/* ========================================================== */
/* SCRIPT PRINCIPAL - StudyAI (Día 9, 10 y 11)               */
/* ========================================================== */

let listaGlobalCuestionarios = [];

document.addEventListener('DOMContentLoaded', () => {
    console.log("¡StudyAI cargado correctamente con JavaScript vainilla!");

    const contenedorDinamico = document.getElementById('lista-cuestionarios-dinamica');
    const inputBusqueda = document.getElementById('input-busqueda');

    if (contenedorDinamico) {
        fetch('/api/cuestionarios')
            .then(response => response.json())
            .then(data => {
                listaGlobalCuestionarios = data;
                renderizarCuestionarios(listaGlobalCuestionarios);
            })
            .catch(error => {
                console.error('Error al cargar los cuestionarios:', error);
                contenedorDinamico.innerHTML = `<p class="texto-vacio-cuestionarios" style="grid-column: 1 / -1;">Error al cargar los datos.</p>`;
            });
    }

    if (inputBusqueda) {
        inputBusqueda.addEventListener('input', (e) => {
            const termino = e.target.value.toLowerCase().trim();
            const resultadosFiltrados = listaGlobalCuestionarios.filter(item => {
                const titulo = item.titulo_cuestionario.toLowerCase();
                const categoria = (item.categoria || "General").toLowerCase();
                const contenido = item.contenido_pregunta.toLowerCase();
                return titulo.includes(termino) || categoria.includes(termino) || contenido.includes(termino);
            });
            renderizarCuestionarios(resultadosFiltrados);
        });
    }

    // Cargar estadísticas, métricas y desglose por categorías del usuario
    const statTotalPreguntas = document.getElementById('stat-total-preguntas');
    const statTotalCategorias = document.getElementById('stat-total-categorias');
    const contenedorDesgloseStats = document.getElementById('lista-desglose-stats');

    if (statTotalPreguntas && statTotalCategorias) {
        fetch('/api/estadisticas')
            .then(response => response.json())
            .then(stats => {
                statTotalPreguntas.textContent = stats.total_preguntas;
                statTotalCategorias.textContent = stats.total_categorias;

                // Renderizar el desglose por categorías si existe el contenedor
                if (contenedorDesgloseStats && stats.desglose) {
                    contenedorDesgloseStats.innerHTML = '';
                    
                    if (stats.desglose.length === 0) {
                        contenedorDesgloseStats.innerHTML = `<p style="font-size: 0.85rem; color: var(--color-text-muted);">No hay categorías registradas aún.</p>`;
                        return;
                    }

                    stats.desglose.forEach(item => {
                        let porcentaje = stats.total_preguntas > 0 ? Math.round((item.cantidad / stats.total_preguntas) * 100) : 0;

                        let filaCategoria = document.createElement('div');
                        filaCategoria.style.display = 'flex';
                        filaCategoria.style.flexDirection = 'column';
                        filaCategoria.style.gap = '0.2rem';

                        filaCategoria.innerHTML = `
                            <div style="display: flex; justify-content: space-between; font-size: 0.85rem; color: var(--color-text-main);">
                                <span><strong>${item.categoria}</strong></span>
                                <span style="color: var(--color-text-muted);">${item.cantidad} preguntas (${porcentaje}%)</span>
                            </div>
                            <div style="width: 100%; background: var(--color-border); height: 8px; border-radius: 4px; overflow: hidden;">
                                <div style="width: ${porcentaje}%; background: var(--color-primary); height: 100%; border-radius: 4px; transition: width 0.4s ease;"></div>
                            </div>
                        `;
                        contenedorDesgloseStats.appendChild(filaCategoria);
                    });
                }
            })
            .catch(error => console.error('Error al cargar estadísticas:', error));
    }

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

// Función centralizada de renderizado en cuadrícula fija de 4 botones
function renderizarCuestionarios(data) {
    const contenedorDinamico = document.getElementById('lista-cuestionarios-dinamica');
    if (!contenedorDinamico) return;

    contenedorDinamico.innerHTML = ''; 
    
    if (data.length === 0) {
        contenedorDinamico.innerHTML = `<p class="texto-vacio-cuestionarios" style="grid-column: 1 / -1;">No se encontraron cuestionarios que coincidan con la búsqueda.</p>`;
        return;
    }

    const categoriasMap = {};
    data.forEach(item => {
        const categoria = item.categoria || "General";
        if (!categoriasMap[categoria]) {
            categoriasMap[categoria] = [];
        }
        categoriasMap[categoria].push(item);
    });

    for (const [nombreCategoria, items] of Object.entries(categoriasMap)) {
        const seccionCat = document.createElement('div');
        seccionCat.className = 'seccion-categoria';
        seccionCat.id = `cat-${nombreCategoria.replace(/\s+/g, '-')}`;

        seccionCat.innerHTML = `
            <div style="font-size: 1.5rem;">📚</div>
            <h3>${nombreCategoria}</h3>
            <span style="font-size: 0.75rem; background: var(--color-background); padding: 0.15rem 0.4rem; border-radius: 10px; color: var(--color-text-muted);">${items.length} preg.</span>
            <div style="font-size: 0.75rem; color: var(--color-primary); font-weight: bold; margin-top: 0.3rem;" class="indicador-estado">▼ Ver</div>
        `;

        seccionCat.addEventListener('click', () => {
            manejarClicCategoria(nombreCategoria, items);
        });

        contenedorDinamico.appendChild(seccionCat);
    }
}

function manejarClicCategoria(nombreCategoria, cuestionariosDeLaCat) {
    const idCatSafe = `cat-${nombreCategoria.replace(/\s+/g, '-')}`;
    const cardSeleccionada = document.getElementById(idCatSafe);
    const contenedorDetalle = document.getElementById('contenedor-detalle-categoria');

    const yaEstaActiva = cardSeleccionada && cardSeleccionada.classList.contains('activa');

    document.querySelectorAll('.seccion-categoria').forEach(card => {
        card.classList.remove('activa');
        const indicador = card.querySelector('.indicador-estado');
        if (indicador) indicador.textContent = '▼ Ver';
    });

    if (yaEstaActiva) {
        if (contenedorDetalle) contenedorDetalle.classList.add('oculto');
        return;
    }

    if (cardSeleccionada) {
        cardSeleccionada.classList.add('activa');
        const indicador = cardSeleccionada.querySelector('.indicador-estado');
        if (indicador) indicador.textContent = '▲ Ocultar';
    }

    let detalle = contenedorDetalle;
    if (!detalle) {
        const gridCategorias = document.getElementById('lista-cuestionarios-dinamica');
        detalle = document.createElement('div');
        detalle.id = 'contenedor-detalle-categoria';
        gridCategorias.after(detalle);
    }

    detalle.className = 'panel-desplegable-flotante';
    detalle.innerHTML = `
        <div class="header-desplegable">
            <h3>Cuestionarios de: ${nombreCategoria}</h3>
            <button onclick="cerrarDetalle()" class="boton-secundario" style="padding: 0.25rem 0.6rem; font-size: 0.8rem; cursor: pointer;">✕ Cerrar</button>
        </div>
        <div class="grid-tarjetas-desplegadas">
            ${cuestionariosDeLaCat.map((quest, index) => {
                let contenidoFormateado = (quest.contenido_pregunta || "")
                    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                    .replace(/\n/g, '<br>');

                return `
                    <div class="tarjeta-cuestionario-item-cuadro" id="tarjeta-quest-${index}">
                        <div style="display: flex; justify-content: space-between; align-items: center; cursor: pointer;" onclick="togglePregunta(${index})">
                            <h4 style="color: var(--color-text-main); margin: 0; font-size: 1rem;">${quest.titulo_cuestionario}</h4>
                            <span id="flecha-quest-${index}" style="font-size: 0.85rem; color: var(--color-primary); font-weight: bold;">▼ Ver</span>
                        </div>
                        <div id="cuerpo-quest-${index}" class="cuerpo-texto-desplegable" style="display: none;">
                            ${contenidoFormateado}
                        </div>
                        <div style="display: flex; gap: 0.5rem; margin-top: 0.75rem; padding-top: 0.5rem; border-top: 1px solid var(--color-border);">
                            <a href="/repaso" class="boton-primario" style="font-size: 0.8rem; padding: 0.3rem 0.6rem; text-align: center; flex: 1; text-decoration: none;">🎯 Repasar</a>
                            <form action="/eliminar-cuestionario/${quest.id_cuestionario}" method="POST" style="margin: 0;">
                                <button type="submit" class="boton-evaluacion boton-rojo" style="padding: 0.3rem 0.6rem; font-size: 0.8rem; cursor: pointer;">🗑</button>
                            </form>
                        </div>
                    </div>
                `;
            }).join('')}
        </div>
    `;
    detalle.classList.remove('oculto');
    detalle.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Función global para minimizar/expandir una tarjeta de pregunta individual
function togglePregunta(index) {
    const cuerpo = document.getElementById(`cuerpo-quest-${index}`);
    const flecha = document.getElementById(`flecha-quest-${index}`);
    
    if (cuerpo.style.display === 'none') {
        cuerpo.style.display = 'block';
        flecha.textContent = '▲ Ocultar';
    } else {
        cuerpo.style.display = 'none';
        flecha.textContent = '▼ Ver';
    }
}

function cerrarDetalle() {
    const contenedorDetalle = document.getElementById('contenedor-detalle-categoria');
    if (contenedorDetalle) {
        contenedorDetalle.classList.add('oculto');
    }
    document.querySelectorAll('.seccion-categoria').forEach(card => {
        card.classList.remove('activa');
        const indicador = card.querySelector('.indicador-estado');
        if (indicador) indicador.textContent = '▼ Ver';
    });
}

/* ========================================================== */
/* VALIDACIÓN Y CONTROL DE PORTABILIDAD (Día 15)              */
/* ========================================================== */

document.addEventListener('DOMContentLoaded', () => {
    const formularioImportar = document.querySelector('.formulario-importar');
    
    if (formularioImportar) {
        formularioImportar.addEventListener('submit', (evento) => {
            const inputArchivo = formularioImportar.querySelector('input[type="file"]');
            if (inputArchivo && inputArchivo.files.length > 0) {
                const nombreArchivo = inputArchivo.files[0].name;
                if (!nombreArchivo.endsWith('.json')) {
                    evento.preventDefault();
                    alert('Por favor, selecciona un archivo con extensión .json válido.');
                }
            }
        });
    }
});