/* ========================================================== */
/* SCRIPT DE REPASO INTERACTIVO - StudyAI (Corregido)         */
/* ========================================================== */

document.addEventListener('DOMContentLoaded', () => {
    let todosLosCuestionarios = [];
    let cuestionariosFiltrados = [];
    let indiceActual = 0;

    const elCategoria = document.getElementById('flashcard-categoria');
    const elProgreso = document.getElementById('flashcard-progreso');
    const elTituloTema = document.getElementById('flashcard-titulo-tema');
    const elPregunta = document.getElementById('flashcard-pregunta');
    const elRespuestaContainer = document.getElementById('flashcard-respuesta-container');
    const elRespuesta = document.getElementById('flashcard-respuesta');
    
    const btnRevelar = document.getElementById('btn-revelar');
    const btnAnterior = document.getElementById('btn-anterior');
    const btnSiguiente = document.getElementById('btn-siguiente');
    const inputBusqueda = document.getElementById('input-busqueda-repaso');
    const selectFiltro = document.getElementById('select-filtro-categoria');

    fetch('/api/cuestionarios')
        .then(res => res.json())
        .then(data => {
            todosLosCuestionarios = data;
            cuestionariosFiltrados = data;
            poblarCategorias(data);
            if (cuestionariosFiltrados.length > 0) {
                mostrarTarjeta(indiceActual);
            } else {
                mostrarEstadoVacio();
            }
        })
        .catch(err => {
            console.error("Error al cargar cuestionarios para repaso:", err);
            elPregunta.textContent = "Error al cargar los datos de repaso.";
        });

    function poblarCategorias(data) {
        const categorias = [...new Set(data.map(item => item.categoria || "General"))];
        selectFiltro.innerHTML = '<option value="todas">Todas las categorías</option>';
        categorias.forEach(cat => {
            const option = document.createElement('option');
            option.value = cat;
            option.textContent = cat;
            selectFiltro.appendChild(option);
        });
    }

    function aplicarFiltros() {
        const termino = inputBusqueda.value.toLowerCase().trim();
        const categoriaSeleccionada = selectFiltro.value;

        cuestionariosFiltrados = todosLosCuestionarios.filter(item => {
            const coincideTexto = item.titulo_cuestionario.toLowerCase().includes(termino) || 
                                  item.contenido_pregunta.toLowerCase().includes(termino);
            const coincideCategoria = categoriaSeleccionada === 'todas' || (item.categoria || "General") === categoriaSeleccionada;

            return coincideTexto && coincideCategoria;
        });

        indiceActual = 0;
        if (cuestionariosFiltrados.length > 0) {
            mostrarTarjeta(indiceActual);
        } else {
            mostrarEstadoVacio();
        }
    }

    function mostrarEstadoVacio() {
        elCategoria.textContent = "Sin resultados";
        elProgreso.textContent = "0 / 0";
        elTituloTema.textContent = "";
        elPregunta.textContent = "No se encontraron tarjetas que coincidan con la búsqueda o categoría seleccionada.";
        elRespuestaContainer.classList.add('oculto');
        btnRevelar.style.display = 'none';
        btnAnterior.disabled = true;
        btnSiguiente.disabled = true;
    }

    function mostrarTarjeta(indice) {
        btnRevelar.style.display = 'block';
        const item = cuestionariosFiltrados[indice];
        elCategoria.textContent = item.categoria || "General";
        elProgreso.textContent = `${indice + 1} de ${cuestionariosFiltrados.length}`;
        elTituloTema.textContent = `Tema: ${item.titulo_cuestionario}`;

        // Separar la pregunta de la explicación buscando palabras clave comunes
        let textoCompleto = item.contenido_pregunta;
        let partes = textoCompleto.split(/(Explicaci[oó]n|Respuesta T[eé]cnica|Breve explicaci[oó]n)/i);

        let textoPregunta = partes[0] || textoCompleto;
        let textoExplicacion = partes.length > 1 ? partes.slice(1).join('') : "No hay explicación adicional detallada.";

        // Limpieza de formato y LaTeX
        const limpiarTexto = (txt) => txt
            .replace(/\\sum_\{([^}]+)\}\^\{([^}]+)\}/g, 'Suma desde $1 hasta $2 de')
            .replace(/\\sum/g, 'Suma')
            .replace(/\^\{([^}]+)\}/g, '^($1)')
            .replace(/[{}]/g, '')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\n/g, '<br>');

        elPregunta.innerHTML = limpiarTexto(textoPregunta);
        elRespuesta.innerHTML = `<strong>Explicación / Respuesta:</strong><br>${limpiarTexto(textoExplicacion)}`;
        
        elRespuestaContainer.classList.add('oculto');
        btnRevelar.textContent = "🔍 Mostrar Respuesta";

        btnAnterior.disabled = indice === 0;
        btnSiguiente.disabled = indice === cuestionariosFiltrados.length - 1;
    }

    btnRevelar.addEventListener('click', () => {
        const estaOculto = elRespuestaContainer.classList.contains('oculto');
        if (estaOculto) {
            elRespuestaContainer.classList.remove('oculto');
            btnRevelar.textContent = "🔒 Ocultar Respuesta";
        } else {
            elRespuestaContainer.classList.add('oculto');
            btnRevelar.textContent = "🔍 Mostrar Respuesta";
        }
    });

    btnSiguiente.addEventListener('click', () => {
        if (indiceActual < cuestionariosFiltrados.length - 1) {
            indiceActual++;
            mostrarTarjeta(indiceActual);
        }
    });

    btnAnterior.addEventListener('click', () => {
        if (indiceActual > 0) {
            indiceActual--;
            mostrarTarjeta(indiceActual);
        }
    });

    inputBusqueda.addEventListener('input', aplicarFiltros);
    selectFiltro.addEventListener('change', aplicarFiltros);
});