/* ============================================================
   HANGARIN — JavaScript Module
   Modal system, filters, toasts, animations
   ============================================================ */

// ==================== MODAL SYSTEM ====================

function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }
}

function openEditModal(taskId, title, description, dueDate, priority) {
    document.getElementById('edit-title').value = title;
    document.getElementById('edit-description').value = description;
    document.getElementById('edit-due-date').value = dueDate || '';
    document.getElementById('edit-priority').value = priority || 'low';
    document.getElementById('edit-form').action = '/update/' + taskId + '/';
    openModal('edit-modal');
}

function openDeleteModal(taskId, taskTitle) {
    document.getElementById('delete-task-title').textContent = taskTitle;
    document.getElementById('delete-form').action = '/delete/' + taskId + '/';
    openModal('delete-modal');
}

// Close modal on backdrop click
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('modal-overlay')) {
        e.target.classList.remove('active');
        document.body.style.overflow = '';
    }
});

// Close modal on ESC
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        const activeModals = document.querySelectorAll('.modal-overlay.active');
        activeModals.forEach(function(modal) {
            modal.classList.remove('active');
        });
        document.body.style.overflow = '';
    }
});


// ==================== TOAST SYSTEM ====================

function showToast(message, type) {
    type = type || 'info';
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = 'toast toast--' + type;

    // Icon based on type
    const icons = {
        success: 'fa-check-circle',
        error: 'fa-exclamation-circle',
        warning: 'fa-exclamation-triangle',
        info: 'fa-info-circle'
    };
    const iconClass = icons[type] || icons.info;

    toast.innerHTML = '<i class="fas ' + iconClass + '"></i><span>' + message + '</span>';
    container.appendChild(toast);

    // Auto-remove after 4 seconds
    setTimeout(function() {
        toast.classList.add('toast-fade-out');
        setTimeout(function() {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 300);
    }, 4000);
}

// Convert Django messages to toasts on page load
document.addEventListener('DOMContentLoaded', function() {
    const djangoMessages = document.querySelectorAll('.django-message');
    djangoMessages.forEach(function(msg, index) {
        const type = msg.getAttribute('data-type') || 'info';
        const text = msg.textContent.trim();

        // Map Django message tags to toast types
        let toastType = 'info';
        if (type.includes('success')) toastType = 'success';
        else if (type.includes('error')) toastType = 'error';
        else if (type.includes('warning')) toastType = 'warning';
        else if (type.includes('info')) toastType = 'info';

        // Stagger toasts
        setTimeout(function() {
            showToast(text, toastType);
        }, index * 200);
    });
});


// ==================== ANIMATION OBSERVER ====================

document.addEventListener('DOMContentLoaded', function() {
    // Staggered card entrance
    const taskCards = document.querySelectorAll('.task-card');
    taskCards.forEach(function(card, index) {
        if (!card.style.animationDelay) {
            card.style.animationDelay = (index * 0.08) + 's';
        }
    });

    // Intersection observer for scroll animations
    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-fade-in');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });

        document.querySelectorAll('.animate-on-scroll').forEach(function(el) {
            observer.observe(el);
        });
    }
});
