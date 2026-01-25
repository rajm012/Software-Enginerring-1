// Utility Functions

// Show loading spinner
export function showLoading() {
    let spinner = document.getElementById('spinner-overlay');
    if (!spinner) {
        spinner = document.createElement('div');
        spinner.id = 'spinner-overlay';
        spinner.className = 'spinner-overlay';
        spinner.innerHTML = '<div class="spinner-border text-light" role="status" style="width: 3rem; height: 3rem;"></div>';
        document.body.appendChild(spinner);
    }
    spinner.classList.add('active');
}

// Hide loading spinner
export function hideLoading() {
    const spinner = document.getElementById('spinner-overlay');
    if (spinner) {
        spinner.classList.remove('active');
    }
}

// Show toast notification
export function showToast(message, type = 'info') {
    const toastContainer = getToastContainer();
    
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0 show`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 5000);
}

// Get or create toast container
function getToastContainer() {
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container';
        document.body.appendChild(container);
    }
    return container;
}

// Format date
export function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Get severity icon
export function getSeverityIcon(severity) {
    const icons = {
        'LOW': 'ℹ️',
        'MEDIUM': '⚠️',
        'HIGH': '🚨',
        'CRITICAL': '🔴'
    };
    return icons[severity] || '📢';
}

// Get severity color class
export function getSeverityClass(severity) {
    return `severity-${severity.toLowerCase()}`;
}

// Get status color class
export function getStatusClass(status) {
    return `status-${status.toLowerCase()}`;
}

// Validate email
export function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Validate password
export function validatePassword(password) {
    if (password.length < 6) {
        return { valid: false, message: 'Password must be at least 6 characters long' };
    }
    return { valid: true, message: '' };
}

// Store user data in session storage
export function setUserData(userData) {
    sessionStorage.setItem('user', JSON.stringify(userData));
}

// Get user data from session storage
export function getUserData() {
    const userData = sessionStorage.getItem('user');
    return userData ? JSON.parse(userData) : null;
}

// Clear user data
export function clearUserData() {
    sessionStorage.removeItem('user');
}

// Check if user is logged in
export function isLoggedIn() {
    return getUserData() !== null;
}

// Check if user is admin
export function isAdmin() {
    const user = getUserData();
    return user && user.is_admin;
}

// Redirect to login if not authenticated
export function requireAuth() {
    if (!isLoggedIn()) {
        window.location.href = '/login.html';
        return false;
    }
    return true;
}

// Redirect to admin dashboard if not admin
export function requireAdmin() {
    if (!isAdmin()) {
        window.location.href = '/user-dashboard.html';
        return false;
    }
    return true;
}

// Format location
export function formatLocation(location) {
    return location.charAt(0).toUpperCase() + location.slice(1);
}

// Escape HTML to prevent XSS
export function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Truncate text
export function truncateText(text, maxLength) {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
}

// Debounce function
export function debounce(func, wait) {
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

// Copy to clipboard
export function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('Copied to clipboard!', 'success');
    }).catch(() => {
        showToast('Failed to copy', 'danger');
    });
}

// Confirm dialog
export function confirmDialog(message) {
    return confirm(message);
}

// Get alert priority for sorting
export function getAlertPriority(severity) {
    const priorities = {
        'CRITICAL': 4,
        'HIGH': 3,
        'MEDIUM': 2,
        'LOW': 1
    };
    return priorities[severity] || 0;
}

// Sort alerts by priority
export function sortAlertsByPriority(alerts) {
    return alerts.sort((a, b) => {
        const priorityDiff = getAlertPriority(b.severity) - getAlertPriority(a.severity);
        if (priorityDiff !== 0) return priorityDiff;
        
        // If same priority, sort by date
        return new Date(b.created_at || b.sent_at) - new Date(a.created_at || a.sent_at);
    });
}


//
// Credits:
//     Raj: Logic, Code and Idea
//     AI Chatbots: Optimization, Formatting
//
