async function cargarCurso(cursoId) {
    // 1. Buscamos los DOS contenedores
    const contenedorLabs = document.getElementById('contenedor-labs'); // El que tiene las cards
    const cursoContenedor = document.getElementById('curso-contenedor'); // Donde se cargará el detalle

    try {
        // 2. Efecto de carga (Ocultamos labs, mostramos curso)
        if (contenedorLabs) contenedorLabs.style.display = 'none';
        cursoContenedor.style.display = 'block';
        cursoContenedor.innerHTML = '<div class="loading">Cargando secuencia...</div>';

        // 3. Petición al servidor (Asegúrate del guion medio como en tu urls.py)
        const response = await fetch(`/cargar-curso/${cursoId}/`);
        if (!response.ok) throw new Error('Error en la respuesta');
        
        const html = await response.text();

        // 4. Insertar contenido y asegurar que se vea
        cursoContenedor.innerHTML = html;
        window.scrollTo(0, 0); // Sube al inicio de la página

    } catch (error) {
        console.error('Error:', error);
        if (contenedorLabs) contenedorLabs.style.display = 'block'; // Si falla, que vuelvan los labs
    }
}