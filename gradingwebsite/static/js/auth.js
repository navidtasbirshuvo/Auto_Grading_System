
// Global variables
let loginTab, signupTab, loginForm, signupForm;

// Global functions that can be called from HTML onclick
window.showTab = function(tab) {
  // Get elements if not already initialized
  if (!loginTab) {
    loginTab = document.getElementById('login-tab');
    signupTab = document.getElementById('signup-tab');
    loginForm = document.getElementById('login-form');
    signupForm = document.getElementById('signup-form');
  }

  if (tab === 'login') {
    loginForm.classList.remove('d-none');
    signupForm.classList.add('d-none');
    loginTab.classList.add('active-tab');
    signupTab.classList.remove('active-tab');
  } else {
    signupForm.classList.remove('d-none');
    loginForm.classList.add('d-none');
    signupTab.classList.add('active-tab');
    loginTab.classList.remove('active-tab');
  }
}

window.handleSignupClick = function() {
  const roleSelect = document.getElementById('signup-role');
  const selectedRole = roleSelect ? roleSelect.value : '';

  if (selectedRole === 'Student') {
    window.location.href = '/auth/student-register/';
  } else if (selectedRole === 'Teacher') {
    window.location.href = '/auth/teacher-register/';
  } else {
    alert('Please select a role to continue.');
  }
}

// Wait for DOM to be fully loaded before initializing
document.addEventListener('DOMContentLoaded', function() {
  loginTab = document.getElementById('login-tab');
  signupTab = document.getElementById('signup-tab');
  loginForm = document.getElementById('login-form');
  signupForm = document.getElementById('signup-form');

  // Initialize with login tab
  window.showTab('login');

  // Handle URL parameters for role selection
  const urlParams = new URLSearchParams(window.location.search);
  const role = urlParams.get('role');

  if (role) {
    const loginRoleSelect = document.getElementById('login-role');
    const signupRoleSelect = document.getElementById('signup-role');

    if (role === 'student') {
      if (loginRoleSelect) loginRoleSelect.value = 'Student';
      if (signupRoleSelect) signupRoleSelect.value = 'Student';
    } else if (role === 'teacher') {
      if (loginRoleSelect) loginRoleSelect.value = 'Teacher';
      if (signupRoleSelect) signupRoleSelect.value = 'Teacher';
    }
  }

  // Add form input animations
  const formInputs = document.querySelectorAll('.form-control, .form-select');
  formInputs.forEach(input => {
    input.addEventListener('focus', function() {
      this.style.transform = 'scale(1.02)';
    });
    input.addEventListener('blur', function() {
      this.style.transform = 'scale(1)';
    });
  });
});
