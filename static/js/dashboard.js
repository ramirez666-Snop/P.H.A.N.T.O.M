document.addEventListener('DOMContentLoaded', function () {
  const menuButtons = document.querySelectorAll('.menu-btn');
  const views = document.querySelectorAll('.view');

  function showView(name) {
    views.forEach(v => {
      if (v.id === name) {
        v.classList.add('active');
      } else {
        v.classList.remove('active');
      }
    });
    menuButtons.forEach(b => {
      b.classList.toggle('active', b.dataset.target === name);
    });
  }

  menuButtons.forEach(btn => {
    btn.addEventListener('click', function () {
      const section = btn.dataset.target;
      showView(section);
      // Actualiza el hash en la URL sin recargar
      window.location.hash = section;
    });
  });

  // Si hay hash en la URL, mostrar esa sección
  if (window.location.hash) {
    showView(window.location.hash.substring(1));
  } else {
    showView('panel');
  }
});



