document.addEventListener('DOMContentLoaded', function() {
    const container = document.querySelector('[data-pagination-container]');
    if (!container) return;

    document.addEventListener('click', function(e) {
        const link = e.target.closest('.pagination a');
        if (!link) return;

        e.preventDefault();
        const url = link.href;

        fetch(url, {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .then(response => response.text())
        .then(data => {
            container.innerHTML = data;
            window.scrollTo({ top: 0, behavior: 'smooth' });
        })
        .catch(err => console.error(err));
    });
});