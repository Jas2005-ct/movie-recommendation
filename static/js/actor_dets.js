document.addEventListener("DOMContentLoaded", () => {
    const button = document.querySelector(".mov");
    const actorId = button.dataset.actorId;
    const moviesDiv = document.querySelector(".movies");

    button.addEventListener("click", async() => {
        // Fetch movies data from the server
        const response = await fetch(`/act_det/${actorId}/?format=json`);
        const data = await response.json();

        // Clear the current movies div
        moviesDiv.innerHTML = '';

        // Add the movies data dynamically
        if (data.movies.length) {
            data.movies.forEach(movie => {
                const movieHTML = `
                        <div class="movie">
                            <a href="/index/${movie.id}">
                                <img src="${movie.img}" alt="${movie.name}">
                            </a>
                            <h2>${movie.name}</h2>
                            <p>${movie.rate}</p>
                            <p class="year">${movie.year}</p>
                        </div>
                    `;
                moviesDiv.insertAdjacentHTML('beforeend', movieHTML);
            });
        } else {
            moviesDiv.innerHTML = '<p>No movies found</p>';
        }
    });
});