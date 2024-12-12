// Function to display the welcome message for the doctor
function displayWelcomeMessage() {
    // Retrieve logged-in user data from localStorage
    const loggedInUser = JSON.parse(localStorage.getItem('loggedInUser'));

    if (loggedInUser && loggedInUser.role === 'doctor') {
        // Display the welcome message with the user's username
        const welcomeMessage = `Welcome, Dr. ${loggedInUser.username}!`;
        const welcomeElement = document.createElement('div');
        welcomeElement.textContent = welcomeMessage;
        document.querySelector('header').appendChild(welcomeElement);
    } else {
        // If no user is logged in or the role is incorrect, redirect to login page
        window.location.href = 'login';
    }
}

// Function to open the modal and populate it with patient details
function openModal(name, age, gender, symptoms, notes) {
    document.getElementById('modalPatientName').textContent = name;
    document.getElementById('modalPatientAge').textContent = age;
    document.getElementById('modalPatientGender').textContent = gender;
    document.getElementById('modalPatientSymptoms').textContent = symptoms;
    document.getElementById('modalPatientNotes').textContent = notes;
    document.getElementById('detailsModal').style.display = 'flex'; // Show modal
}

// Function to close the modal
function closeModal() {
    document.getElementById('detailsModal').style.display = 'none'; // Hide modal
}

// Close the modal when clicking outside the modal content
window.addEventListener('click', (event) => {
    if (event.target === document.getElementById('detailsModal')) {
        closeModal();
    }
});

// Call the function to display the welcome message when the page loads
window.onload = function() {
    displayWelcomeMessage();
};
