document.addEventListener('DOMContentLoaded', function() {
    
    // ==================== NAVEGACIÓN PRINCIPAL ====================
    const menuBtns = document.querySelectorAll('.menu-btn');
    const views = document.querySelectorAll('.view');
    
    function cambiarVista(viewId) {
        views.forEach(view => {
            view.classList.remove('active');
        });
        
        const vistaActiva = document.getElementById(viewId);
        if (vistaActiva) {
            vistaActiva.classList.add('active');
        }
        
        menuBtns.forEach(btn => {
            btn.classList.remove('active');
            if (btn.getAttribute('data-target') === viewId) {
                btn.classList.add('active');
            }
        });
        
        // Si cambiamos a laboratorios, reiniciamos el estado
        if (viewId === 'laboratorios') {
            reiniciarLaboratorios();
        }
    }
    
    menuBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const target = this.getAttribute('data-target');
            if (target) {
                cambiarVista(target);
            }
        });
    });
    
    // ==================== CARGA DINÁMICA DE CURSOS ====================
    function reiniciarLaboratorios() {
        const contenedorLabs = document.querySelector('.contenedor-labs');
        const cursoContenedor = document.getElementById('curso-contenedor');
        
        if (contenedorLabs) {
            contenedorLabs.style.display = 'block';
        }
        if (cursoContenedor) {
            cursoContenedor.style.display = 'none';
            cursoContenedor.innerHTML = ''; // Limpiar contenido
        }
    }
    
    // Función para cargar un curso dinámicamente
    async function cargarCurso(cursoId) {
        const contenedorLabs = document.querySelector('.contenedor-labs');
        const cursoContenedor = document.getElementById('curso-contenedor');
        
        if (!cursoContenedor) return;
        
        try {
            // Ocultar laboratorios
            if (contenedorLabs) {
                contenedorLabs.style.display = 'none';
            }
            
            // Mostrar loading
            cursoContenedor.style.display = 'block';
            cursoContenedor.innerHTML = `
                <div style="text-align: center; padding: 50px;">
                    <div style="color: #00aaff;">Cargando curso...</div>
                </div>
            `;
            
            // Cargar el partial correspondiente usando fetch
            const response = await fetch(`/cargar-curso/${cursoId}/`);
            
            if (!response.ok) {
                throw new Error('Error al cargar el curso');
            }
            
            const html = await response.text();
            cursoContenedor.innerHTML = html;
            
            // Re-inicializar eventos del contenido cargado
            const backBtn = cursoContenedor.querySelector('.back-btn');
            if (backBtn) {
                backBtn.onclick = reiniciarLaboratorios;
            }
            
        } catch (error) {
            console.error('Error:', error);
            cursoContenedor.innerHTML = `
                <div style="text-align: center; padding: 50px; color: red;">
                    Error al cargar el curso. Por favor, intenta de nuevo.
                    <br><br>
                    <button class="btn back-btn" onclick="reiniciarLaboratorios()">Volver</button>
                </div>
            `;
        }
    }
    
    // Exponer funciones globalmente
    window.cargarCurso = cargarCurso;
    window.reiniciarLaboratorios = reiniciarLaboratorios;
    
    // Agregar eventos a los botones de laboratorios (con delegación de eventos)
    document.addEventListener('click', function(e) {
        const labBtn = e.target.closest('.lab-btn');
        if (labBtn && document.getElementById('laboratorios')?.classList.contains('active')) {
            const cursoId = labBtn.getAttribute('data-curso');
            if (cursoId) {
                e.preventDefault();
                cargarCurso(cursoId);
            }
        }
    });
    
    // Inicializar
    if (document.getElementById('laboratorios')?.classList.contains('active')) {
        reiniciarLaboratorios();
    }
});