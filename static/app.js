document.addEventListener('DOMContentLoaded', function () {
  // Theme toggle
  document.querySelectorAll('#theme-toggle').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var html = document.documentElement;
      html.classList.toggle('dark');
      localStorage.setItem('theme', html.classList.contains('dark') ? 'dark' : 'light');
      lucide.createIcons();
    });
  });

  // Auto-dismiss toasts
  document.querySelectorAll('.toast').forEach(function (toast) {
    setTimeout(function () {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(100%)';
      toast.style.transition = 'all 300ms';
      setTimeout(function () { toast.remove(); }, 300);
    }, 4000);
  });

  // Sidebar toggle
  var sidebarToggle = document.getElementById('sidebar-toggle');
  var sidebar = document.getElementById('sidebar');
  var sidebarOverlay = document.getElementById('sidebar-overlay');
  if (sidebarToggle && sidebar) {
    sidebarToggle.addEventListener('click', function () {
      sidebar.classList.toggle('-translate-x-full');
      if (sidebarOverlay) sidebarOverlay.classList.toggle('hidden');
    });
    if (sidebarOverlay) {
      sidebarOverlay.addEventListener('click', function () {
        sidebar.classList.add('-translate-x-full');
        sidebarOverlay.classList.add('hidden');
      });
    }
  }
});
