// Sidebar Toggle
const sidebar = document.getElementById('sidebar');
const menuToggle = document.getElementById('menuToggle');
const sidebarToggle = document.getElementById('sidebarToggle');

if (menuToggle) {
    menuToggle.addEventListener('click', () => {
        sidebar.classList.toggle('active');
    });
}

if (sidebarToggle) {
    sidebarToggle.addEventListener('click', () => {
        sidebar.classList.toggle('active');
    });
}

// Close sidebar when clicking outside on mobile
document.addEventListener('click', (e) => {
    if (window.innerWidth <= 768) {
        if (!sidebar.contains(e.target) && !menuToggle.contains(e.target)) {
            sidebar.classList.remove('active');
        }
    }
});

// Close alert messages
document.querySelectorAll('.close-alert').forEach(btn => {
    btn.addEventListener('click', function() {
        this.closest('.alert').style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            this.closest('.alert').remove();
        }, 300);
    });
});

// Auto-hide alerts after 5 seconds
setTimeout(() => {
    document.querySelectorAll('.alert').forEach(alert => {
        alert.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => alert.remove(), 300);
    });
}, 5000);

// Add slideOut animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        to {
            opacity: 0;
            transform: translateX(20px);
        }
    }
`;
document.head.appendChild(style);

// Confirm delete actions
document.querySelectorAll('form[method="post"]').forEach(form => {
    if (form.querySelector('input[type="submit"][value*="Delete"]') || 
        form.querySelector('.btn-danger')) {
        form.addEventListener('submit', function(e) {
            if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    }
});

