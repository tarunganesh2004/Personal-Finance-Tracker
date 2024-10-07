// @ts-nocheck
// Handle login form submission
document.getElementById('loginForm').addEventListener('submit', function (e) {
    e.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert('Login successful');
                window.location.href = 'index.html';  // Redirect to dashboard
            } else {
                alert('Invalid credentials');
            }
        })
        .catch(error => console.error('Error:', error));
});

// Handle registration form submission
document.getElementById('registerForm').addEventListener('submit', function (e) {
    e.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert('Registration successful');
                window.location.href = 'login.html';  // Redirect to login
            } else {
                alert('Registration failed');
            }
        })
        .catch(error => console.error('Error:', error));
});
