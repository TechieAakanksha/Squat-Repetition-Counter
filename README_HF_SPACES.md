# Hugging Face Spaces Deployment

This app is ready to deploy on Hugging Face Spaces using Docker.

## Quick Deploy Steps:

1. **Create a Space** on https://huggingface.co/spaces
   - Choose "Docker" as the SDK
   - Name it (e.g., `Squat-Repetition-Counter`)

2. **Clone your Space repository:**
   ```bash
   git clone https://huggingface.co/spaces/your-username/Squat-Repetition-Counter
   ```

3. **Copy files to the Space repo:**
   ```bash
   cp app.py templates/ static/ requirements.txt Dockerfile .dockerignore README_HF_SPACES.md <Space-repo-path>/
   ```

4. **Push to Hugging Face:**
   ```bash
   cd <Space-repo-path>
   git add .
   git commit -m "Deploy Flask app"
   git push
   ```

5. **Wait for build** - HF Spaces will automatically build and deploy

## Your URL will be:
`https://your-username-squat-repetition-counter.hf.space`

## Important Notes:

⚠️ **Camera Access:** Server-side camera access won't work on HF Spaces. You'll need to:
- Modify the app to use **WebRTC** for browser-based camera access
- Or use **MediaPipe JavaScript** instead of Python MediaPipe

The current app uses `cv2.VideoCapture(0)` which requires a physical camera on the server, which cloud platforms don't have.

## Environment Variables (Optional):

- `PORT`: Server port (default: 7860 for HF Spaces)
- `HOST`: Server host (default: 0.0.0.0 for HF Spaces)
- `DEBUG`: Enable debug mode (default: False in production)

