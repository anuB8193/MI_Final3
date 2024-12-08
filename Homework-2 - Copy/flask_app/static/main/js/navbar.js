// Select the menu toggle button (image) and the navigation bar
const menuToggle = document.querySelector('.menu-toggle');
const navLinks = document.querySelector('.nav-links');

// Ensure that both menuToggle and navLinks are defined
if (menuToggle && navLinks) {
    // Add an event listener to the menu button to toggle the visibility of the nav links
    menuToggle.addEventListener('click', () => {
        navLinks.classList.toggle('nav-open');
    });
} else {
    console.error('Menu toggle button or navigation links not found.');
}
