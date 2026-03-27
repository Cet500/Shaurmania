document.addEventListener('DOMContentLoaded', function () {
    function upsertToast(message) {
        let toast = document.querySelector('[data-cart-toast]');
        if (!toast) {
            toast = document.createElement('div');
            toast.setAttribute('data-cart-toast', '1');
            toast.className = 'cart-toast';
            document.body.appendChild(toast);
        }

        toast.textContent = message;
        toast.classList.add('is-visible');
        clearTimeout(toast._timer);
        toast._timer = setTimeout(function () {
            toast.classList.remove('is-visible');
        }, 1300);
    }

    function updateCartSummary(data) {
        const totalEl = document.querySelector('[data-cart-total]');
        if (totalEl && typeof data.total !== 'undefined') {
            totalEl.textContent = data.total + '₽';
        }

        const countBadges = document.querySelectorAll('[data-cart-count]');
        countBadges.forEach(function (badge) {
            if (typeof data.count !== 'undefined') {
                badge.textContent = data.count;
                badge.style.display = data.count > 0 ? '' : 'none';
            }
        });

        if (data.items) {
            const qtyById = {};
            data.items.forEach(function (item) {
                qtyById[item.id] = item.quantity;

                const row = document.querySelector('[data-cart-item="' + item.id + '"]');
                if (!row) return;

                const qtyEl = row.querySelector('[data-cart-item-qty]');
                const rowTotalEl = row.querySelector('[data-cart-item-total]');

                if (qtyEl) {
                    qtyEl.textContent = item.quantity;
                }
                if (rowTotalEl) {
                    rowTotalEl.textContent = item.total + '₽';
                }
            });

            document.querySelectorAll('[data-cart-inline-qty]').forEach(function (counterEl) {
                const itemId = parseInt(counterEl.getAttribute('data-cart-item'), 10);
                const qty = qtyById[itemId] || 0;
                counterEl.textContent = qty;
                counterEl.style.display = qty > 0 ? 'inline-flex' : 'none';
            });

            document.querySelectorAll('[data-cart-item]').forEach(function (row) {
                const itemId = parseInt(row.getAttribute('data-cart-item'), 10);
                if (!qtyById[itemId] && row.classList.contains('cart-item')) {
                    row.remove();
                }
            });

            const cartContainer = document.querySelector('[data-cart-items]');
            const emptyState = document.querySelector('[data-cart-empty]');
            if (cartContainer && emptyState) {
                const hasItems = data.items.length > 0;
                emptyState.style.display = hasItems ? 'none' : 'block';
            }
        }
    }

    function handleCartClick(e) {
        const link = e.target.closest('[data-cart-action]');
        if (!link) return;

        e.preventDefault();
        const url = link.getAttribute('href');
        const action = link.getAttribute('data-cart-action') || 'add';
        if (!url) return;

        fetch(url, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'Accept': 'application/json'
            },
            credentials: 'same-origin'
        })
            .then(function (response) {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(function (data) {
                updateCartSummary(data);
                upsertToast(action === 'remove' ? 'Товар убран из корзины' : 'Товар добавлен в корзину');
            })
            .catch(function (err) {
                console.error('Cart AJAX error:', err);
                window.location.href = url;
            });
    }

    document.addEventListener('click', handleCartClick);
});

