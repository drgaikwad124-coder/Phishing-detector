# Phishing URL Detection System

Hey! This is a web app I built that checks if URLs are phishing sites or not. It uses machine learning to analyze 30 different features from a URL and tells you if it's safe or suspicious.

## What it does

Basically, you paste a URL and it tells you if it's probably a phishing site. It looks at things like:
- Does the URL use an IP address instead of a domain name?
- Is it a URL shortener?
- How long is the URL?
- Does it have weird symbols?
- And like 25 more things...

Then it uses a machine learning model (Gradient Boosting Classifier) to make a prediction. It gives you a percentage of how safe or dangerous it thinks the URL is.

## Features

- Checks URLs in real-time
- Shows you probability scores (like "95% safe" or "80% phishing")
- Has a web interface with 3 pages (home, about, history)
- Saves your check history automatically
- Has an API if you want to use it programmatically
- Validates URLs so you don't waste time on invalid ones
- Error messages disappear after a few minutes (so they don't clutter the screen)

## Installation

### What you need

- Python 3.11 or 3.12 (3.14 doesn't work well with some packages yet)
- pip (comes with Python usually)

### Setup steps

1. **Get the code**
   - Download the ZIP or clone the repo, whatever you prefer
   - Extract it somewhere

2. **Create a virtual environment** (trust me, you want to do this)
   
   Windows:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
   
   Linux/Mac:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install the packages**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or if you want to install them manually:
   ```bash
   pip install beautifulsoup4 Flask googlesearch-python numpy pandas python-dateutil requests scikit-learn python-whois gunicorn lxml
   ```

4. **Make sure the model file exists**
   - Check that `pickle/model.pkl` is there
   - If it's missing, you'll need to train it first (see train_model.py)

## Running it

1. Activate your virtual environment (if you closed the terminal)
   ```bash
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Linux/Mac
   ```

2. Run the app
   ```bash
   python app.py
   ```

3. Open your browser and go to `http://127.0.0.1:5000`

4. Paste a URL and click "Analyze"

That's it! The results show up right on the same page.

## Project structure

Here's what's in this project:

```
├── app.py              # Main Flask app - handles all the routes
├── feature.py          # Extracts the 30 features from URLs
├── train_model.py      # Script to train the ML model (if you want to retrain)
├── test_system.py      # Some test scripts I wrote
├── requirements.txt    # All the Python packages needed
├── pickle/
│   └── model.pkl      # The trained model (this is important!)
├── static/
│   ├── styles.css     # CSS for the website
│   └── img/
│       └── hh.jpg     # Background image
└── templates/
    ├── index.html     # Home page
    ├── about.html     # About page
    └── history.html   # Shows past URL checks
```

## How it works

The system looks at 30 different features:

**URL stuff (1-9):**
1. Using IP address?
2. URL length
3. Is it a URL shortener?
4. Has @ symbol?
5. Multiple redirects?
6. Prefix/suffix in domain?
7. How many subdomains?
8. Uses HTTPS?
9. Domain registration length

**Content stuff (10-23):**
10. Favicon source
11. Non-standard port
12. HTTPS in domain name
13. Request URL stuff
14. Anchor URLs
15. Links in scripts
16. Form handlers
17. Email in page
18. Abnormal URL patterns
19. Website forwarding
20. Status bar customization
21. Right click disabled?
22. Popup windows?
23. Iframe redirection

**External stuff (24-30):**
24. How old is the domain?
25. DNS records
26. Website traffic
27. PageRank
28. Google index
29. Links pointing to page
30. Stats reports

Each feature gets a value of -1 (suspicious), 0 (neutral), or 1 (safe). Then the model takes all 30 values and predicts if it's phishing or not.

## API

If you want to use this programmatically, there are a few endpoints:

**Health check:**
```
GET /health
```
Returns if the server is running and if the model loaded.

**Check a URL:**
```
POST /api/check
Content-Type: application/json

{
  "url": "https://example.com"
}
```

**Check multiple URLs (max 10):**
```
POST /api/batch
Content-Type: application/json

{
  "urls": ["https://google.com", "https://github.com"]
}
```

## Testing

I included some test scripts:

```bash
python test_system.py
```

This tests a few URLs and shows you what features were detected.

## Performance

- First check: Usually takes 5-10 seconds (has to do whois lookups and stuff)
- After that: Usually 2-5 seconds
- The model prediction itself is super fast (<0.1 seconds)

The slow part is getting info from external sources like whois databases and DNS lookups.

## Common problems

**"Model not found" error:**
- Make sure `pickle/model.pkl` exists
- Check you're running from the project root directory

**"No module named X" error:**
- Activate your virtual environment!
- Run `pip install -r requirements.txt` again

**Port 5000 already in use:**
- Change the port in app.py: `app.run(debug=True, port=5001)`
- Or close whatever is using port 5000

**URL validation errors:**
- Make sure the URL has a proper domain (like example.com)
- Don't just type random letters
- Include http:// or https:// if needed

**It's slow:**
- That's normal, especially the first check
- Network speed affects it a lot
- Some websites take forever to respond

## Notes

- This is for educational purposes
- Don't rely on this as your only security measure
- The model isn't perfect - it can miss some phishing sites
- Keep the model updated if you're using this seriously

## License

Free to use, modify, whatever. It's for learning.

## Support

If something's broken:
1. Check the console for error messages
2. Make sure Python version is 3.11 or 3.12
3. Verify all packages are installed
4. Check that model.pkl exists

That's about it. Have fun!
