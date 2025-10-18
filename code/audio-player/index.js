async function loadEpisodes() {
    const container = document.getElementById('episodes-container');
    const loading = document.getElementById('loading');
    const errorDiv = document.getElementById('error');

    try {
        const response = await fetch('tracks.json');
        if (!response.ok) {
            throw new Error(`Failed to load episodes: ${response.status}`);
        }

        const data = await response.json();
        const episodes = data.episodes;

        if (!episodes || episodes.length === 0) {
            throw new Error('No episodes found');
        }

        loading.classList.add('is-hidden');

        episodes.forEach((episode, index) => {
            const card = document.createElement('div');
            card.className = 'card episode-card';

            card.innerHTML = `
                <div class="card-content">
                    <div class="media">
                        <div class="media-content">
                            <p class="title is-4">${escapeHtml(episode.title)}</p>
                        </div>
                    </div>
                    <div class="content">
                        <p class="show-notes">${escapeHtml(episode.show_nows)}</p>
                    </div>
                </div>
                <footer class="card-footer">
                    <a href="details.html?episode=${index}" class="card-footer-item">
                        <strong>Listen Now</strong>
                    </a>
                </footer>
            `;

            container.appendChild(card);
        });

    } catch (error) {
        loading.classList.add('is-hidden');
        errorDiv.textContent = `Error: ${error.message}`;
        errorDiv.classList.remove('is-hidden');
        console.error('Error loading episodes:', error);
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Load episodes when page loads
document.addEventListener('DOMContentLoaded', loadEpisodes);

