# Deployment Guide

## Option 1: Hugging Face Spaces (Recommended for ML Apps)

### URL Format:
`https://your-username-spaces-name.hf.space`

### Steps:
1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Name your space (e.g., `Squat-Repetition-Counter`)
4. Select **"Docker"** as the SDK
5. Clone the Space repository:
   ```bash
   git clone https://huggingface.co/spaces/your-username/Squat-Repetition-Counter
   ```
6. Copy your files to the cloned repository
7. Push to Hugging Face:
   ```bash
   cd Squat-Repetition-Counter
   git add .
   git commit -m "Deploy Flask app"
   git push
   ```
8. Hugging Face will automatically build and deploy

**Note:** Camera access may be limited. The app uses server-side camera access which won't work on HF Spaces. You'll need to modify the app to use WebRTC for browser-based camera access.

---

## Option 2: PythonAnywhere (Traditional Web Hosting)

### URL Format:
`https://your-username.pythonanywhere.com`

### Steps:
1. Sign up at https://www.pythonanywhere.com
2. Go to the "Web" tab
3. Click "Add a new web app"
4. Choose Flask and Python 3.10
5. Upload your files via the "Files" tab:
   - `app.py`
   - `requirements.txt`
   - `templates/` folder
   - `static/` folder
6. Edit the WSGI file (located in `/var/www/your-username_pythonanywhere_com_wsgi.py`):
   ```python
   import sys
   path = '/home/your-username/mysite'
   if path not in sys.path:
       sys.path.insert(0, path)
   
   from app import app as application
   ```
7. Install dependencies via Bash console:
   ```bash
   pip3.10 install --user -r requirements.txt
   ```
8. Reload your web app from the "Web" tab

**Note:** Free tier doesn't support webcam access. You'll need a paid plan for camera access, or modify the app to use WebRTC.

---

## Option 3: GitHub Pages (Static Only)

### URL Format:
`https://techieaakanksha.github.io/Squat-Repetition-Counter/`

GitHub Actions will automatically deploy static files on push to `main` or `master` branch.

**Note:** Flask features won't work on GitHub Pages since it only serves static files.

---

## Camera Access Limitations

All these platforms have limitations with camera access:
- **Server-side camera access** (`cv2.VideoCapture(0)`) won't work on cloud platforms
- **Solution:** Modify the app to use **WebRTC** for browser-based camera access
- Or use **MediaPipe JavaScript** instead of Python MediaPipe

