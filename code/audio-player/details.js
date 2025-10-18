async function loadEpisodeDetails() {
    const urlParams = new URLSearchParams(window.location.search);
    const episodeIndex = urlParams.get('episode');

    const titleElement = document.getElementById('episode-title');
    const detailsContainer = document.getElementById('episode-details');
    const loading = document.getElementById('loading');
    const errorDiv = document.getElementById('error');

    if (episodeIndex === null) {
        showError('No episode specified');
        return;
    }

    try {
        const response = await fetch('tracks.json');
        if (!response.ok) {
            throw new Error(`Failed to load episode data: ${response.status}`);
        }

        const data = await response.json();
        const episodes = data.episodes;

        if (!episodes || episodes.length === 0) {
            throw new Error('No episodes found');
        }

        const index = parseInt(episodeIndex, 10);
        if (isNaN(index) || index < 0 || index >= episodes.length) {
            throw new Error('Invalid episode index');
        }

        const episode = episodes[index];
        loading.classList.add('is-hidden');

        // Update page title
        titleElement.textContent = episode.title;
        document.title = `${episode.title} - Episode Details`;

        // Create episode details
        detailsContainer.innerHTML = `
            <div class="episode-content">
                <div class="custom-audio-player">
                    <img src="https://cdn-podcast.talkpython.fm/static/img/podcast-theme-img_1400_v3.jpg" alt="Podcast Cover" class="album-art" id="album-art">
                    
                    <div class="player-title">${escapeHtml(episode.title)}</div>
                    <div class="player-subtitle">TALK PYTHON TO ME</div>
                    
                    <div class="progress-container">
                        <div class="progress-bar" id="progress-bar">
                            <div class="progress-fill" id="progress-fill"></div>
                        </div>
                        <div class="time-display">
                            <span id="current-time">0:00</span>
                            <span id="total-time">-0:00</span>
                        </div>
                    </div>
                    
                    <div class="playback-controls">
                        <button class="control-button" id="skip-back" title="Skip back 15 seconds">
                            <div class="skip-button">
                                <svg viewBox="0 0 24 24">
                                    <path d="M11.99 5V1l-5 5 5 5V7c3.31 0 6 2.69 6 6s-2.69 6-6 6-6-2.69-6-6h-2c0 4.42 3.58 8 8 8s8-3.58 8-8-3.58-8-8-8z"/>
                                </svg>
                                <span class="skip-number">15</span>
                            </div>
                        </button>
                        
                        <button class="control-button" id="play-pause" title="Play/Pause">
                            <div class="play-pause-button">
                                <svg id="play-icon" viewBox="0 0 24 24">
                                    <path d="M8 5v14l11-7z"/>
                                </svg>
                                <svg id="pause-icon" viewBox="0 0 24 24" style="display: none;">
                                    <path d="M6 4h4v16H6V4zm8 0h4v16h-4V4z"/>
                                </svg>
                            </div>
                        </button>
                        
                        <button class="control-button" id="skip-forward" title="Skip forward 30 seconds">
                            <div class="skip-button">
                                <svg viewBox="0 0 24 24">
                                    <path d="M12.01 5V1l5 5-5 5V7c-3.31 0-6 2.69-6 6s2.69 6 6 6 6-2.69 6-6h2c0 4.42-3.58 8-8 8s-8-3.58-8-8 3.58-8 8-8z"/>
                                </svg>
                                <span class="skip-number">30</span>
                            </div>
                        </button>
                    </div>
                    
                    <audio id="audio-element">
                        <source src="${escapeHtml(episode.mp3_link)}" type="audio/mpeg">
                    </audio>
                </div>

                <div class="content">
                    <h3 class="subtitle is-5">Show Notes</h3>
                    <p class="show-notes-full">${escapeHtml(episode.show_nows)}</p>
                </div>

                <div class="buttons">
                    <a href="${escapeHtml(episode.mp3_link)}" 
                       class="button is-bold" 
                       download
                       target="_blank">
                        Download Episode
                    </a>
                </div>
            </div>
        `;
        
        // Initialize custom audio player
        initializeAudioPlayer();

    } catch (error) {
        showError(error.message);
        console.error('Error loading episode:', error);
    }

    function showError(message) {
        loading.classList.add('is-hidden');
        errorDiv.textContent = `Error: ${message}`;
        errorDiv.classList.remove('is-hidden');
        titleElement.textContent = 'Error Loading Episode';
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function initializeAudioPlayer() {
    const audio = document.getElementById('audio-element');
    const playPauseBtn = document.getElementById('play-pause');
    const playIcon = document.getElementById('play-icon');
    const pauseIcon = document.getElementById('pause-icon');
    const skipBackBtn = document.getElementById('skip-back');
    const skipForwardBtn = document.getElementById('skip-forward');
    const progressBar = document.getElementById('progress-bar');
    const progressFill = document.getElementById('progress-fill');
    const currentTimeEl = document.getElementById('current-time');
    const totalTimeEl = document.getElementById('total-time');
    
    // Format time helper
    function formatTime(seconds) {
        if (!isFinite(seconds)) return '0:00';
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    }
    
    // Update progress bar and time display
    function updateProgress() {
        if (!audio.duration) return;
        
        const progress = (audio.currentTime / audio.duration) * 100;
        progressFill.style.width = progress + '%';
        
        currentTimeEl.textContent = formatTime(audio.currentTime);
        const remaining = audio.duration - audio.currentTime;
        totalTimeEl.textContent = '-' + formatTime(remaining);
    }
    
    // Play/Pause toggle
    playPauseBtn.addEventListener('click', () => {
        if (audio.paused) {
            audio.play();
            playIcon.style.display = 'none';
            pauseIcon.style.display = 'block';
        } else {
            audio.pause();
            playIcon.style.display = 'block';
            pauseIcon.style.display = 'none';
        }
    });
    
    // Skip back 15 seconds
    skipBackBtn.addEventListener('click', () => {
        audio.currentTime = Math.max(0, audio.currentTime - 15);
    });
    
    // Skip forward 30 seconds
    skipForwardBtn.addEventListener('click', () => {
        audio.currentTime = Math.min(audio.duration, audio.currentTime + 30);
    });
    
    // Seek by clicking on progress bar
    progressBar.addEventListener('click', (e) => {
        if (!audio.duration) return;
        
        const rect = progressBar.getBoundingClientRect();
        const percent = (e.clientX - rect.left) / rect.width;
        audio.currentTime = percent * audio.duration;
    });
    
    // Update UI when audio metadata loads
    audio.addEventListener('loadedmetadata', () => {
        totalTimeEl.textContent = '-' + formatTime(audio.duration);
    });
    
    // Update progress as audio plays
    audio.addEventListener('timeupdate', updateProgress);
    
    // Reset play button when audio ends
    audio.addEventListener('ended', () => {
        playIcon.style.display = 'block';
        pauseIcon.style.display = 'none';
    });
}

// Load episode details when page loads
document.addEventListener('DOMContentLoaded', loadEpisodeDetails);

