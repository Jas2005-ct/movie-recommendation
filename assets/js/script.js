// Select modal elements
const modal = document.getElementById('movieModal');
const modalTitle = document.getElementById('modal-title');
const modalPoster = document.getElementById('modal-poster');
const modalRating = document.getElementById('modal-rating');
const modalGenre = document.getElementById('modal-genre');
const modalReleaseDate = document.getElementById('modal-release-date');
const modalDuration = document.getElementById('modal-duration');
const modalDescription = document.getElementById('modal-description');
const modalLanguage = document.getElementById('modal-language');
const closeButton = document.querySelector('.close-button');

// Movie data
const movieData = [
    {
        id: "leo",
        title: "LEO",
        releaseDate: "October 19, 2023",
        genre: "Action, Thriller",
        duration: "2h 45m",
        rating: "8.8/10",
        tagline: "When the predator becomes prey.",
        description: "Leo is an action-packed thriller starring Vijay in the lead role, exploring the battle between good and evil.",
        language: "Tamil",
        trailer: "https://www.youtube.com/watch?v=leo-trailer",
        img: "LEO.jpg"
    },
    {
        id: "jailer",
        title: "JAILER",
        releaseDate: "August 10, 2023",
        genre: "Action, Drama",
        duration: "2h 35m",
        rating: "8/10",
        tagline: "A retired jailer’s unexpected journey.",
        description: "Jailer is a gripping story of a retired cop who faces challenges in his family and profession.",
        language: "Tamil",
        trailer: "https://www.youtube.com/watch?v=jailer-trailer",
        img: "JAILER.jpg"
    },
    {
        id: "amaran",
        title: "AMARAN",
        releaseDate: "1992",
        genre: "Action, Thriller",
        duration: "2h 20m",
        rating: "9.4/10",
        tagline: "An epic tale of revenge.",
        description: "Amaran is a 90s classic, known for its iconic music and thrilling storyline.",
        language: "Tamil",
        trailer: "https://www.youtube.com/watch?v=amaran-trailer",
        img: "AMARAN.jpg"
    }
];

// Add click event to movie posters
const movieElements = document.querySelectorAll('.movie');
movieElements.forEach(movie => {
    movie.addEventListener('click', () => {
        const movieKey = movie.getAttribute('data-movie');
        const movieInfo = movieData.find(item => item.id === movieKey); // Match by id

        if (movieInfo) {
            // Populate modal with movie details
            modalTitle.textContent = movieInfo.title;
            modalPoster.src = movieInfo.img;
            modalRating.textContent = movieInfo.rating;
            modalGenre.textContent = movieInfo.genre;
            modalReleaseDate.textContent = movieInfo.releaseDate;
            modalDuration.textContent = movieInfo.duration;
            modalDescription.textContent = movieInfo.description;
            modalLanguage.textContent = movieInfo.language;

            // Show the modal
            modal.style.display = 'flex';
        }
    });
});

// Close modal
closeButton.addEventListener('click', () => {
    modal.style.display = 'none';
});
