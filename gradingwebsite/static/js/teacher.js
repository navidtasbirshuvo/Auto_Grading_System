
const mobileMenuButton = document.getElementById('mobile-menu-btn');
const sidebar = document.querySelector('aside.sidebar');

if (mobileMenuButton) {
    mobileMenuButton.addEventListener('click', () => {
        sidebar.classList.toggle('show');
    });
}


document.addEventListener('click', (event) => {
    if (window.innerWidth < 768 &&
        !sidebar.contains(event.target) &&
        !mobileMenuButton.contains(event.target) &&
        sidebar.classList.contains('show')) {
        sidebar.classList.remove('show');
    }
});


window.addEventListener('resize', () => {
    if (window.innerWidth >= 768) {
        sidebar.classList.remove('show');
    }
});


const dropdownItems = document.querySelectorAll('.dropdown-item');
dropdownItems.forEach(item => {
    item.addEventListener('mouseenter', () => {
        item.style.backgroundColor = '#4B5563';
    });
    item.addEventListener('mouseleave', () => {
        item.style.backgroundColor = 'transparent';
    });
});


document.addEventListener('DOMContentLoaded', function() {
    
    updateActiveNavigation();

    initializeDashboardWidgets();

    initializeExamManagement();
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

    console.log('Teacher dashboard initialized');
}

function initializeExamManagement() {
 
    console.log('Exam management initialized');
}
