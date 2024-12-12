// // login.js
//
// // Sample Login Validation Function
// function validateLogin(event) {
//     event.preventDefault(); // Prevent form from submitting
//
//     const username = document.getElementById('username').value;
//     const password = document.getElementById('password').value;
//     const errorMessage = document.getElementById('error-message');
//
//     // Retrieve users from localStorage
//     const users = JSON.parse(localStorage.getItem('users')) || [];
//
//     // Check if the user exists in our stored users data
//     const user = users.find(user => user.username === username && user.password === password);
//
//     if (user) {
//         // Store the logged-in user's role in localStorage (for session tracking)
//         localStorage.setItem('loggedInUser', JSON.stringify(user));
//
//         // Redirect based on user role
//         if (user.role === 'doctor') {
//             window.location.href = 'doctors_dashboard.html';  // Redirect to Doctor Dashboard
//         } else if (user.role === 'patient') {
//             window.location.href = 'diagnosis_form.html';  // Redirect to Patient Dashboard
//         }
//     } else {
//         errorMessage.textContent = "Invalid username or password!";
//     }
// }
//
// // Add event listener to form submission
// document.getElementById('login-form').addEventListener('submit', validateLogin);
