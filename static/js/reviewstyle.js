let currentIndex = 0;

function loadReviews() {
    const reviewsContainer = document.getElementById("reviewsContainer");
    const reviews = document.querySelectorAll(".review");

    if (reviews.length === 0) {
        reviewsContainer.innerHTML = "<p>No reviews submitted yet.</p>";
        return;
    }

    // Initialize the carousel position
    reviewsContainer.style.transform = `translateX(0)`;
}

function slide(direction) {
    const reviews = document.querySelectorAll(".review");
    const carouselContainer = document.querySelector(".carousel-container");

    if (reviews.length === 0) return;

    currentIndex += direction;

    // Loop to the beginning or end
    if (currentIndex < 0) currentIndex = reviews.length - 1;
    if (currentIndex >= reviews.length) currentIndex = 0;

    carouselContainer.style.transform = `translateX(-${currentIndex * 100}%)`;
}

// Load reviews on page load
window.onload = loadReviews;