document.addEventListener("DOMContentLoaded", () => {
    // Page load animation
    const pageContent = document.querySelector("main");
    pageContent.style.opacity = 0;
    pageContent.style.transform = "translateY(20px)";

    setTimeout(() => {
        pageContent.style.transition = "opacity 0.8s ease, transform 0.8s ease";
        pageContent.style.opacity = 1;
        pageContent.style.transform = "translateY(0)";
    }, 100);

    // Trailer link animation
    const trailerLink = document.querySelector(".movie-info a");
    trailerLink.addEventListener("mouseover", () => {
        trailerLink.style.transform = "scale(1.1)";
    });

    trailerLink.addEventListener("mouseout", () => {
        trailerLink.style.transform = "scale(1)";
    });

    // Dynamic back-to-home functionality
    const homeLink = document.querySelector('a[href="index.html"]');
    homeLink.addEventListener("click", (event) => {
        event.preventDefault();
        window.location.href = "index.html";
    });

    // Add a subtle scrolling effect to the page
    window.addEventListener("scroll", () => {
        const header = document.querySelector("header");
        if (window.scrollY > 50) {
            header.style.backgroundColor = "#5a4c82"; // Darker color on scroll
            header.style.boxShadow = "0 4px 6px rgba(0, 0, 0, 0.1)";
        } else {
            header.style.backgroundColor = "#6b5b95";
            header.style.boxShadow = "none";
        }
    });

    // Dynamic title update for better accessibility
    document.title = "LEO - Action Thriller by Lokesh Kanagaraj";
});
