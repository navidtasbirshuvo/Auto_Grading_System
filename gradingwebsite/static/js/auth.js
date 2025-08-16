
const loginTab = document.getElementById('login-tab');
const signupTab = document.getElementById('signup-tab');
const loginForm = document.getElementById('login-form');
const signupForm = document.getElementById('signup-form');

function showTab(tab) {
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


function handleSignupSubmit(event) {
  event.preventDefault();

  const roleSelect = document.getElementById('signup-role');
  const selectedRole = roleSelect.value;

  if (selectedRole === 'Student') {
    window.location.href = '/auth/student-register/';
  } else if (selectedRole === 'Teacher') {
    window.location.href = '/auth/teacher-register/';
  } else {
    alert('Please select a role to continue.');
  }
}


function handleSignupClick() {
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


showTab('login');


document.addEventListener('DOMContentLoaded', function() {
 
  const urlParams = new URLSearchParams(window.location.search);
  const role = urlParams.get('role');

  if (role) {
    
    const loginRoleSelect = document.getElementById('login-role');
    const signupRoleSelect = document.getElementById('signup-role');

    if (role === 'student') {
      loginRoleSelect.value = 'Student';
      signupRoleSelect.value = 'Student';
    } else if (role === 'teacher') {
      loginRoleSelect.value = 'Teacher';
      signupRoleSelect.value = 'Teacher';
    }
  }

  
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
