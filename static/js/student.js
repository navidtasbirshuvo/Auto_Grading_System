// Student-specific JavaScript functionality

// Sidebar toggle for mobile
const mobileMenuButton = document.getElementById('mobile-menu-btn');
const sidebar = document.querySelector('aside.sidebar');

if (mobileMenuButton) {
    mobileMenuButton.addEventListener('click', () => {
        sidebar.classList.toggle('show');
    });
}

// Close sidebar when clicking outside on mobile
document.addEventListener('click', (event) => {
    if (window.innerWidth < 768 &&
        !sidebar.contains(event.target) &&
        !mobileMenuButton.contains(event.target) &&
        sidebar.classList.contains('show')) {
        sidebar.classList.remove('show');
    }
});

// Handle window resize
window.addEventListener('resize', () => {
    if (window.innerWidth >= 768) {
        sidebar.classList.remove('show');
    }
});

// Custom dropdown hover effects for better UX
const dropdownItems = document.querySelectorAll('.dropdown-item');
dropdownItems.forEach(item => {
    item.addEventListener('mouseenter', () => {
        item.style.backgroundColor = '#4B5563';
    });
    item.addEventListener('mouseleave', () => {
        item.style.backgroundColor = 'transparent';
    });
});

// Student-specific functionality
document.addEventListener('DOMContentLoaded', function() {
    // Update active navigation item based on current page
    updateActiveNavigation();

    // Initialize dashboard widgets
    initializeDashboardWidgets();
});

function updateActiveNavigation() {
    const currentPage = window.location.pathname.split('/').pop();
    const navItems = document.querySelectorAll('.nav-item');

    navItems.forEach(item => {
        item.classList.remove('active');
        if (item.getAttribute('href') === currentPage) {
            item.classList.add('active');
        }
    });
}

function initializeDashboardWidgets() {
    // Add any student-specific dashboard initialization here
    console.log('Student dashboard initialized');
}
