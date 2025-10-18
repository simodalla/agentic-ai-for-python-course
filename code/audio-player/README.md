# Podcast Audio Player

A simple, lightweight HTML/JavaScript audio player for podcast episodes. This project demonstrates how to build a functional web application without complex frameworks or backend infrastructure.

## Features

- Browse podcast episodes from a JSON data file
- Play episodes directly in the browser with HTML5 audio controls
- Responsive design using Bulma CSS framework
- Clean, modern UI with smooth animations
- Download episodes for offline listening
- No build process or dependencies required

## Technologies Used

- **HTML5** - Structure and audio playback
- **Vanilla JavaScript** - Dynamic content loading and interaction
- **Bulma CSS** - Responsive styling and components
- **Python http.server** - Simple local development server

## Project Structure

```
audio-player/
├── index.html      # Home page with episode listing
├── details.html    # Episode details with audio player
├── tracks.json     # Podcast episode data
└── README.md       # This file
```

## How to Run

1. Make sure you have Python installed (Python 3.x recommended)

2. Navigate to the project directory:
   ```bash
   cd audio-player
   ```

3. Start the local web server:
   ```bash
   uv run python -m http.server -b 127.0.0.1 10000
   ```
   
   Or using standard Python:
   ```bash
   python -m http.server -b 127.0.0.1 10000
   ```

4. Open your browser and navigate to:
   ```
   http://127.0.0.1:10000/
   ```

5. To stop the server, press `Ctrl+C` in the terminal

## Usage

### Home Page (index.html)
- View all available podcast episodes
- See episode titles and preview of show notes
- Click "Listen Now" to go to the episode details

### Details Page (details.html)
- View complete episode information
- Play the episode using the built-in audio player
- Download the episode for offline listening
- Return to the home page with the back button

## Data Format

Episodes are stored in `tracks.json` with the following structure:

```json
{
    "episodes": [
        {
            "title": "Episode Title",
            "mp3_link": "https://example.com/episode.mp3",
            "show_nows": "Episode description and show notes"
        }
    ]
}
```

To add or modify episodes, simply edit the `tracks.json` file.

## Browser Compatibility

This project uses modern web standards and is compatible with:
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Any browser supporting HTML5 audio and ES6 JavaScript

## License

This is a demonstration project for educational purposes.

