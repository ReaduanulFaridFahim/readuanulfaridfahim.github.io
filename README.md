# Readuanul Farid Fahim Portfolio

A polished single-page portfolio for a Computer Science graduate with focus on AI/ML, aviation operations, and sports leadership.

## Run locally

You can run the portfolio locally using any of the following methods:

### Method 1: Using `uv` (Fastest & Recommended)
```bash
uv run serve.py
```
This automatically finds an available port, disables browser caching so edits show instantly, and opens `http://localhost:8000` in your default browser.

### Method 2: One-Click Launch (Windows)
Double-click `start-localhost.bat` or run:
```powershell
.\start-localhost.ps1
```

### Method 3: Standard Python
```bash
python serve.py
# or
python -m http.server 8000
```

### Method 4: npm / Node
```bash
npm start
# or
npm run dev
```

Then open:
```text
http://localhost:8000
```

## Deploy on GitHub Pages

1. Push this project to a GitHub repository.
2. Open the repository settings.
3. Go to Pages.
4. Set the source to the main branch and root folder.
5. Save.
6. Your site will be available at:

```text
https://<your-username>.github.io/<your-repo-name>/
```

## Deploy on Netlify

1. Drag and drop the project folder into Netlify.
2. Keep the publish directory as the project root.
3. Deploy.

## Notes

- The portfolio is a static HTML file and works without a build step.
- The profile photo uses the GitHub avatar with an offline SVG fallback (`profile.svg`).
- Project thumbnails are located in `assets/`, and travel stamp photography is preserved locally in `assets/travel/` for reliability and offline support.
