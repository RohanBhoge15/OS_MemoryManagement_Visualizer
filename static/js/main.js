// Main JavaScript file for common functionality

// Show/Hide loading spinner
function showLoading() {
    document.getElementById('loadingSpinner').style.display = 'flex';
}

function hideLoading() {
    document.getElementById('loadingSpinner').style.display = 'none';
}

// Mobile Navigation Toggle
document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');

    if (hamburger) {
        hamburger.addEventListener('click', () => {
            navMenu.classList.toggle('active');
        });

        // Close menu when clicking on a link
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => {
                navMenu.classList.remove('active');
            });
        });
    }
});

// API Helper Functions
async function makeAPIRequest(url, method = 'POST', data = null) {
    showLoading();
    try {
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            }
        };

        if (data) {
            options.body = JSON.stringify(data);
        }

        const response = await fetch(url, options);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        hideLoading();
        return result;
    } catch (error) {
        hideLoading();
        console.error('API Request Error:', error);
        showNotification('Error: ' + error.message, 'error');
        throw error;
    }
}

// Notification System
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${getNotificationIcon(type)}"></i>
        <span>${message}</span>
    `;
    
    // Style the notification
    Object.assign(notification.style, {
        position: 'fixed',
        top: '20px',
        right: '20px',
        padding: '1rem 1.5rem',
        background: getNotificationColor(type),
        color: 'white',
        borderRadius: '8px',
        boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
        zIndex: '10000',
        display: 'flex',
        alignItems: 'center',
        gap: '0.5rem',
        fontWeight: '600',
        animation: 'slideIn 0.3s ease-out'
    });
    
    document.body.appendChild(notification);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'fadeOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

function getNotificationIcon(type) {
    const icons = {
        'success': 'check-circle',
        'error': 'exclamation-circle',
        'warning': 'exclamation-triangle',
        'info': 'info-circle'
    };
    return icons[type] || 'info-circle';
}

function getNotificationColor(type) {
    const colors = {
        'success': '#4CAF50',
        'error': '#F44336',
        'warning': '#FF9800',
        'info': '#2196F3'
    };
    return colors[type] || '#2196F3';
}

// Format bytes to human readable
function formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Parse reference string
function parseReferenceString(str) {
    return str.split(',')
        .map(s => s.trim())
        .filter(s => s !== '')
        .map(s => parseInt(s))
        .filter(n => !isNaN(n));
}

// Validate positive number
function validatePositiveNumber(value, fieldName) {
    const num = parseInt(value);
    if (isNaN(num) || num <= 0) {
        showNotification(`${fieldName} must be a positive number`, 'error');
        return false;
    }
    return true;
}

// Clear all results
function clearResults() {
    const resultElements = [
        'metricsDisplay',
        'visualizationDisplay',
        'allocationDetails',
        'pageTableDisplay',
        'segmentTableDisplay',
        'executionTrace',
        'accessLogDisplay',
        'comparisonResults'
    ];
    
    resultElements.forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.style.display = 'none';
        }
    });
}

// Display metrics in cards
function displayMetrics(metrics) {
    const metricsDisplay = document.getElementById('metricsDisplay');
    if (!metricsDisplay) return;
    
    metricsDisplay.style.display = 'block';
    
    // Update metric values based on available data
    Object.keys(metrics).forEach(key => {
        const element = document.getElementById(key);
        if (element) {
            element.textContent = metrics[key];
        }
    });
}

// Scroll to element smoothly
function scrollToElement(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

// Create table row
function createTableRow(data, isHeader = false) {
    const row = document.createElement('tr');
    const tag = isHeader ? 'th' : 'td';
    
    data.forEach(cell => {
        const cellElement = document.createElement(tag);
        cellElement.textContent = cell;
        row.appendChild(cellElement);
    });
    
    return row;
}

// Add fade-in animation to elements
function animateElement(element) {
    element.classList.add('fade-in');
}

// Debounce function for input events
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

// Export for use in other files
window.appUtils = {
    showLoading,
    hideLoading,
    makeAPIRequest,
    showNotification,
    formatBytes,
    parseReferenceString,
    validatePositiveNumber,
    clearResults,
    displayMetrics,
    scrollToElement,
    createTableRow,
    animateElement,
    debounce
};