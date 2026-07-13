/**
 * Q360 - Main JavaScript File
 * Handles common functionality across the application
 */

/**
 * CSRF Token Helper - Get CSRF token from meta tag or cookie
 */
function getCSRFToken() {
    // Try meta tag first
    const metaTag = document.querySelector('meta[name="csrf-token"]');
    if (metaTag) {
        const content = metaTag.getAttribute('content');
        // Extract token from Django's {% csrf_token %} format
        const match = content.match(/value='([^']+)'/);
        if (match) {
            return match[1];
        }
        return content;
    }

    // Fallback to cookie
    const name = 'csrftoken';
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Document Ready
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

/**
 * Initialize Application
 */
function initializeApp() {
    // Initialize tooltips
    initializeTooltips();

    // Initialize popovers
    initializePopovers();

    // Load notifications
    loadNotifications();

    // Setup AJAX defaults
    setupAjaxDefaults();

    // Auto-hide alerts
    autoHideAlerts();

    // Initialize form validation
    initializeFormValidation();
}

/**
 * Initialize Bootstrap Tooltips
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Initialize Bootstrap Popovers
 */
function initializePopovers() {
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

/**
 * Load Notifications
 */
function loadNotifications() {
    fetch('/api/notifications/?limit=5')
        .then(response => response.json())
        .then(data => {
            // It should use data.unread_count instead of data.count for the badge
            updateNotificationBadge(data.unread_count || 0);
            renderNotifications(data.results || []);
        })
        .catch(error => console.error('Error loading notifications:', error));
}

/**
 * Update Notification Badge
 */
function updateNotificationBadge(count) {
    const badge = document.getElementById('notificationCount');
    if (badge) {
        badge.textContent = count;
        // Don't show badge if count is 0
        if (count > 0) {
            badge.style.display = 'inline-flex';
        } else {
            badge.style.display = 'none';
        }
    }
}

/**
 * Render Notifications
 */
function renderNotifications(notifications) {
    // navbar.html uses id="notificationItems", not "notificationList"
    const notificationList = document.getElementById('notificationItems');
    if (!notificationList) return;

    if (!notifications || notifications.length === 0) {
        notificationList.innerHTML = `
            <div class="p-4 text-center text-gray-500 dark:text-gray-400">
                <i class="fas fa-bell-slash text-2xl mb-2 text-gray-300 dark:text-gray-600"></i>
                <p class="text-sm">Bildiriş yoxdur</p>
            </div>
        `;
        return;
    }

    let html = '';

    notifications.forEach(notification => {
        // Python view returns 'type', not 'notification_type'
        const type = notification.type || notification.notification_type;
        const icon = getNotificationIcon(type);
        // Use Tailwind CSS classes matching navbar.html design
        html += `
            <a href="${notification.link || '#'}" onclick="markAsRead(${notification.id})" class="block px-4 py-3 border-b dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors ${!notification.is_read ? 'bg-blue-50/50 dark:bg-blue-900/20' : ''}">
                <div class="flex items-start">
                    <div class="flex-shrink-0 mt-1">
                        <i class="${icon}"></i>
                    </div>
                    <div class="ml-3 w-0 flex-1">
                        <p class="text-sm font-medium text-gray-900 dark:text-white ${!notification.is_read ? 'font-bold' : ''}">
                            ${notification.title}
                        </p>
                        <p class="mt-1 text-sm text-gray-500 dark:text-gray-400 line-clamp-2">
                            ${notification.message}
                        </p>
                        <p class="mt-1 text-xs text-gray-400 dark:text-gray-500">
                            ${new Date(notification.created_at).toLocaleDateString()}
                        </p>
                    </div>
                </div>
            </a>
        `;
    });

    html += `
        <li><hr class="dropdown-divider"></li>
        <li><a class="dropdown-item text-center small" href="/notifications/">Hamısını Gör</a></li>
    `;

    notificationList.innerHTML = html;
}

/**
 * Get Notification Icon
 */
function getNotificationIcon(type) {
    const icons = {
        'info': 'fas fa-info-circle text-info',
        'success': 'fas fa-check-circle text-success',
        'warning': 'fas fa-exclamation-triangle text-warning',
        'error': 'fas fa-times-circle text-danger'
    };
    return icons[type] || 'fas fa-bell';
}

/**
 * Mark Notification as Read
 */
function markAsRead(notificationId) {
    // The correct URL is /notifications/{id}/mark-read/ (no /api/ prefix)
    fetch(`/notifications/${notificationId}/mark-read/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            loadNotifications();
        }
    })
    .catch(error => console.error('Error marking notification as read:', error));
}

/**
 * Setup AJAX Defaults
 */
function setupAjaxDefaults() {
    // Add CSRF token to all AJAX requests
    const csrftoken = getCSRFToken();

    // Setup for jQuery if available
    if (window.jQuery && csrftoken) {
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafe(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
                }
            }
        });
    }

    // Setup for Fetch API (modern approach)
    if (csrftoken) {
        const originalFetch = window.fetch;
        window.fetch = function(...args) {
            let [resource, config] = args;

            // Add CSRF token to non-safe methods
            if (config && config.method && !csrfSafe(config.method)) {
                config.headers = config.headers || {};
                config.headers['X-CSRFToken'] = csrftoken;
            }

            return originalFetch(resource, config);
        };
    }
}

/**
 * Check if HTTP method is CSRF safe
 */
function csrfSafe(method) {
    return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
}

/**
 * Get Cookie by Name
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * Auto Hide Alerts
 */
function autoHideAlerts() {
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
}

/**
 * Show Toast Notification
 */
function showToast(message, type = 'info', duration = 3000) {
    const toastContainer = document.getElementById('toastContainer') || createToastContainer();

    const toastId = 'toast-' + Date.now();
    const toastHTML = `
        <div id="${toastId}" class="toast align-items-center text-white bg-${type} border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;

    toastContainer.insertAdjacentHTML('beforeend', toastHTML);

    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement, { delay: duration });
    toast.show();

    // Remove toast after it's hidden
    toastElement.addEventListener('hidden.bs.toast', () => {
        toastElement.remove();
    });
}

/**
 * Create Toast Container
 */
function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toastContainer';
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    container.style.zIndex = '9999';
    document.body.appendChild(container);
    return container;
}

/**
 * Confirm Action
 */
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

/**
 * Delete Item with Confirmation
 */
function deleteItem(url, itemName, redirectUrl) {
    if (confirm(`${itemName} silmək istədiyinizdən əminsiniz?`)) {
        fetch(url, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => {
            if (response.ok) {
                showToast('Uğurla silindi', 'success');
                if (redirectUrl) {
                    window.location.href = redirectUrl;
                } else {
                    location.reload();
                }
            } else {
                showToast('Xəta baş verdi', 'danger');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('Xəta baş verdi', 'danger');
        });
    }
}

/**
 * Initialize Form Validation
 */
function initializeFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');

    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }

            form.classList.add('was-validated');
        }, false);
    });
}

/**
 * Format Date
 */
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('az-AZ', options);
}

/**
 * Format DateTime
 */
function formatDateTime(dateTimeString) {
    const options = {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    return new Date(dateTimeString).toLocaleDateString('az-AZ', options);
}

/**
 * Debounce Function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Copy to Clipboard
 */
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('Kopyalandı!', 'success', 2000);
    }).catch(err => {
        console.error('Failed to copy:', err);
        showToast('Kopyalama xətası', 'danger');
    });
}

/**
 * Export Table to CSV
 */
function exportTableToCSV(tableId, filename) {
    const table = document.getElementById(tableId);
    let csv = [];
    const rows = table.querySelectorAll('tr');

    for (let i = 0; i < rows.length; i++) {
        const row = [], cols = rows[i].querySelectorAll('td, th');

        for (let j = 0; j < cols.length; j++) {
            row.push(cols[j].innerText);
        }

        csv.push(row.join(','));
    }

    downloadCSV(csv.join('\n'), filename);
}

/**
 * Download CSV
 */
function downloadCSV(csv, filename) {
    const csvFile = new Blob([csv], { type: 'text/csv' });
    const downloadLink = document.createElement('a');

    downloadLink.download = filename;
    downloadLink.href = window.URL.createObjectURL(csvFile);
    downloadLink.style.display = 'none';

    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
}

/**
 * Show Loading Spinner
 */
function showLoading() {
    const spinner = document.createElement('div');
    spinner.id = 'loadingSpinner';
    spinner.className = 'spinner-wrapper';
    spinner.innerHTML = `
        <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Yüklənir...</span>
        </div>
    `;
    document.body.appendChild(spinner);
}

/**
 * Hide Loading Spinner
 */
function hideLoading() {
    const spinner = document.getElementById('loadingSpinner');
    if (spinner) {
        spinner.remove();
    }
}

// Global Error Handler
window.addEventListener('error', function(event) {
    console.error('Global error:', event.error);
    // Optionally send to error tracking service
});

/**
 * Global AJAX Form Submission
 */
window.apiSubmit = async function(formElement, successCallback = null) {
    const formData = new FormData(formElement);
    const url = formElement.action || window.location.href;
    const method = formElement.method || 'POST';

    try {
        const response = await fetch(url, {
            method: method,
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCSRFToken()
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            showToast(data.message || 'Uğurlu əməliyyat', 'success');
            if (successCallback) {
                successCallback(data);
            } else if (data.redirect_url) {
                window.location.href = data.redirect_url;
            }
        } else {
            showToast(data.message || 'Xəta baş verdi', 'danger');
        }
        return data;
    } catch (error) {
        console.error('API Submit Error:', error);
        showToast('Serverlə əlaqə xətası', 'danger');
        return { success: false, message: 'Server error' };
    }
};

// Expose functions globally
window.Q360 = {
    showToast,
    confirmAction,
    deleteItem,
    formatDate,
    formatDateTime,
    copyToClipboard,
    exportTableToCSV,
    showLoading,
    hideLoading,
    getCookie
};
