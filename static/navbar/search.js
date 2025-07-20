document.addEventListener('DOMContentLoaded', () => {

    const searchInput = document.getElementById('movie-search-input');
    const resultsContainer = document.getElementById('search-results-container');
    const spinner = document.getElementById('search-spinner');
    
    if (!searchInput) return;

    const debounce = (func, delay) => {
        let timeout;
        return (...args) => {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), delay);
        };
    };

    const handleSearch = async (query) => {
        if (query.length < 2) {
            resultsContainer.innerHTML = '';
            resultsContainer.style.display = 'none';
            return;
        }

        spinner.style.display = 'block';
        resultsContainer.style.display = 'block';

        try {
            const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
            const movies = await response.json();
            renderResults(movies);
        } catch (error) {
            console.error('Search failed:', error);
            resultsContainer.innerHTML = '<div class="search-result-item">Error fetching results.</div>';
        } finally {
            spinner.style.display = 'none';
        }
    };

    const renderResults = (movies) => {
        if (movies.length === 0) {
            resultsContainer.innerHTML = '<div class="search-result-item">No movies found.</div>';
            return;
        }

        resultsContainer.innerHTML = movies.map(movie => {
            const releaseYear = movie.original_release_date ? new Date(movie.original_release_date).getFullYear() : '';
            const posterUrl = movie.poster_url ? movie.poster_url : '/static/img/placeholder.png'; // Use a placeholder if no poster

            return `
                <a href="/film/${movie._id}" class="search-result-item">
                    <img src="${posterUrl}" alt="${movie.movie_title}">
                    <div class="result-info">
                        <strong>${movie.movie_title}</strong>
                        <span>${releaseYear}</span>
                    </div>
                </a>
            `;
        }).join('');
    };

    searchInput.addEventListener('keyup', debounce((e) => {
        handleSearch(e.target.value);
    }, 350));

    document.addEventListener('click', (e) => {
        if (!searchInput.contains(e.target)) {
            resultsContainer.style.display = 'none';
        }
    });
});