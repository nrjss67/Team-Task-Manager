document.addEventListener('DOMContentLoaded', function() {
    const collapseBtn = document.querySelector('.sidebar-collapse-btn');
    const sidebar = document.querySelector('.sidebar');

    collapseBtn?.addEventListener('click', function() {
        sidebar.classList.toggle('collapsed');
    });
});