// Main JavaScript file for Milk Delivery Seller Dashboard

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Add smooth scrolling to anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.remove();
            }, 300);
        }, 5000);
    });

    // Add loading state to forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.innerHTML = '<span class="loading"></span> Processing...';
                submitBtn.disabled = true;
            }
        });
    });

    // Add confirmation for delete actions
    const deleteButtons = document.querySelectorAll('button[type="submit"]');
    deleteButtons.forEach(btn => {
        if (btn.textContent.includes('Remove') || btn.textContent.includes('Delete')) {
            btn.addEventListener('click', function(e) {
                if (!confirm('Are you sure you want to delete this item?')) {
                    e.preventDefault();
                }
            });
        }
    });

    // Real-time search functionality for tables
    const searchInputs = document.querySelectorAll('.search-input');
    searchInputs.forEach(input => {
        input.addEventListener('keyup', function() {
            const filter = this.value.toLowerCase();
            const table = this.closest('.card').querySelector('table tbody');
            const rows = table.querySelectorAll('tr');

            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(filter) ? '' : 'none';
            });
        });
    });

    // Auto-save form data to localStorage
    const formInputs = document.querySelectorAll('input, textarea, select');
    formInputs.forEach(input => {
        // Load saved data
        const savedValue = localStorage.getItem(`form_${input.name}`);
        if (savedValue && input.type !== 'password') {
            input.value = savedValue;
        }

        // Save data on change
        input.addEventListener('change', function() {
            if (this.type !== 'password') {
                localStorage.setItem(`form_${this.name}`, this.value);
            }
        });
    });

    // Clear saved form data on successful submission
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const inputs = this.querySelectorAll('input, textarea, select');
            inputs.forEach(input => {
                localStorage.removeItem(`form_${input.name}`);
            });
        });
    });
});

// Utility Functions
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    document.querySelector('main').insertAdjacentElement('afterbegin', alertDiv);
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function formatDate(dateString) {
    const options = { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
    };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

// Stock level checker
function checkStockLevels() {
    const stockBadges = document.querySelectorAll('.badge');
    stockBadges.forEach(badge => {
        const stockText = badge.textContent;
        const stockNumber = parseInt(stockText.match(/\d+/));
        
        if (stockNumber < 10) {
            showAlert(`Low stock alert: ${stockText}`, 'warning');
        }
    });
}

// Call stock checker on page load
document.addEventListener('DOMContentLoaded', checkStockLevels);

// Export functions for global use
window.milkDeliveryUtils = {
    showAlert,
    formatCurrency,
    formatDate,
    checkStockLevels
};