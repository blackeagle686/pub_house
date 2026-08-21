// Theme Initialization (Runs immediately to prevent FOUC)
const savedTheme = localStorage.getItem('theme');
if (savedTheme) {
    document.documentElement.setAttribute('data-theme', savedTheme);
} else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    document.documentElement.setAttribute('data-theme', 'dark');
}

// DOM Dependent Logic
document.addEventListener('DOMContentLoaded', () => {
    // Theme Toggle Logic
    const themeBtns = document.querySelectorAll('.theme-toggle-btn');

    function updateIcons() {
        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        themeBtns.forEach(btn => {
            const icon = btn.querySelector('i');
            if (icon) {
                if (isDark) {
                    icon.classList.replace('fa-moon', 'fa-sun');
                } else {
                    icon.classList.replace('fa-sun', 'fa-moon');
                }
            }
        });
    }

    updateIcons();

    themeBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const targetTheme = currentTheme === 'dark' ? 'light' : 'dark';

            document.documentElement.setAttribute('data-theme', targetTheme);
            localStorage.setItem('theme', targetTheme);
            updateIcons();
        });
    });

    // Report Modal Logic
    const reportModal = document.getElementById('reportModal');
    if (reportModal) {
        reportModal.addEventListener('show.bs.modal', event => {
            const button = event.relatedTarget;
            const modelName = button.getAttribute('data-bs-model');
            const objectId = button.getAttribute('data-bs-id');

            const modelInput = reportModal.querySelector('#report_model_name');
            const idInput = reportModal.querySelector('#report_object_id');

            if (modelInput) modelInput.value = modelName;
            if (idInput) idInput.value = objectId;
        });
    }
});
