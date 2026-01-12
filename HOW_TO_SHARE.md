# How to Share This Project

Here are different ways to share your Phishing Detection project:

## Method 1: Create a ZIP File (Easiest)

### What to Include:
- ✅ All `.py` files (app.py, feature.py, etc.)
- ✅ `requirements.txt`
- ✅ `pickle/model.pkl` (the trained model)
- ✅ `templates/` folder (all HTML files)
- ✅ `static/` folder (CSS and images)
- ✅ `README.md` and `QUICKSTART.md`
- ✅ `phishing.csv` (if you want to share the dataset)

### What to Exclude:
- ❌ `__pycache__/` folder (Python cache - not needed)
- ❌ `.venv/` or `venv/` folder (virtual environment - too large, recipient will create their own)
- ❌ `url_history.json` (user-specific history file)

### Steps:
1. **Windows**: Right-click the folder → "Send to" → "Compressed (zipped) folder"
2. **Mac**: Right-click → "Compress"
3. **Linux**: `zip -r PhishingDetection.zip . -x "*.venv/*" "__pycache__/*" "*.pyc"`

Then share the ZIP file via:
- Email (if under size limit)
- Google Drive / Dropbox / OneDrive
- USB drive
- Network share

## Method 2: Upload to GitHub (Best for Code Sharing)

### Steps:

1. **Create a GitHub account** (if you don't have one): https://github.com

2. **Create a new repository**:
   - Go to GitHub → Click "+" → "New repository"
   - Name it: `phishing-detection` or `phishing-url-detector`
   - Make it Public or Private (your choice)
   - Don't initialize with README (you already have one)

3. **Initialize Git in your project**:
   ```bash
   cd "D:\PhisingDetection-main\PhisingDetection-main"
   git init
   git add .
   git commit -m "Initial commit - Phishing Detection System"
   ```

4. **Connect to GitHub**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/phishing-detection.git
   git branch -M main
   git push -u origin main
   ```

5. **Share the GitHub link**: `https://github.com/YOUR_USERNAME/phishing-detection`

### Benefits:
- Version control
- Easy to update and share
- Others can contribute
- Free hosting

## Method 3: Google Drive / Dropbox / OneDrive

### Steps:
1. Upload the entire folder to your cloud storage
2. Right-click the folder → "Share" or "Get link"
3. Send the link to whoever needs it

**Note**: Make sure to exclude `__pycache__` and `.venv` folders before uploading (they're large and unnecessary)

## Method 4: USB Drive / External Storage

1. Copy the project folder to USB drive
2. Exclude `__pycache__` and `.venv` folders
3. Share the USB drive

## Method 5: Network Share (Local Network)

1. Right-click folder → Properties → Sharing
2. Share with specific users or make it accessible on network
3. Share the network path: `\\COMPUTER_NAME\PhisingDetection-main`

## Quick ZIP Creation Script

If you want to create a clean ZIP file automatically, here's a Python script:

```python
import zipfile
import os

def create_zip():
    exclude = ['__pycache__', '.venv', 'venv', 'env', '.git', 
               'url_history.json', '.DS_Store', 'Thumbs.db']
    
    with zipfile.ZipFile('PhishingDetection.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk('.'):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if d not in exclude]
            
            for file in files:
                file_path = os.path.join(root, file)
                # Skip excluded files
                if not any(exc in file_path for exc in exclude):
                    zipf.write(file_path)
    
    print("Created PhishingDetection.zip")

if __name__ == "__main__":
    create_zip()
```

Save as `create_zip.py` and run: `python create_zip.py`

## What the Recipient Needs to Do

After receiving the project, they should:

1. Extract the ZIP (if shared as ZIP)
2. Create virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Linux/Mac
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the app:
   ```bash
   python app.py
   ```

## Important Files Checklist

Make sure these are included:
- ✅ `app.py` - Main application
- ✅ `feature.py` - Feature extraction
- ✅ `pickle/model.pkl` - Trained model (IMPORTANT!)
- ✅ `requirements.txt` - Dependencies
- ✅ `templates/` - All HTML files
- ✅ `static/` - CSS and images
- ✅ `README.md` - Documentation
- ✅ `QUICKSTART.md` - Setup guide

## File Size Considerations

- **With .venv**: ~500MB - 1GB (too large, don't include)
- **Without .venv**: ~10-50MB (much better)
- **Without model.pkl**: Smaller, but recipient can't run it

## Security Note

If sharing publicly:
- Don't include any API keys or secrets
- Don't include personal data in `url_history.json`
- Review code for any sensitive information

---

**Recommended**: Use GitHub for code sharing, or ZIP file for quick sharing via email/cloud storage.
