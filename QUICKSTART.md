# Quick Start Guide

Want to get this running fast? Here's how to do it in about 5 minutes.

## Step 1: Check your Python version

```bash
python --version
```

You need Python 3.11 or 3.12. If you have 3.14, it won't work well with some packages. Download 3.12 from python.org if needed.

## Step 2: Create a virtual environment

This keeps your project's packages separate from your system Python. Trust me, it's worth it.

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

You should see `(.venv)` appear in your terminal prompt. That means it's active.

## Step 3: Install the packages

```bash
# Upgrade pip first (good practice)
python -m pip install --upgrade pip

# Install everything
pip install -r requirements.txt
```

This will take a couple minutes. Go grab a coffee or something.

If you don't have a requirements.txt file, you can install manually:
```bash
pip install beautifulsoup4 Flask googlesearch-python numpy pandas python-dateutil requests scikit-learn python-whois gunicorn lxml
```

## Step 4: Check the model file

Make sure `pickle/model.pkl` exists. If it doesn't, you'll need to train the model first (which requires the phishing.csv dataset).

**Windows:**
```bash
dir pickle\model.pkl
```

**Linux/Mac:**
```bash
ls pickle/model.pkl
```

## Step 5: Run it!

```bash
python app.py
```

You should see something like:
```
INFO:__main__:Model loaded successfully
 * Running on http://127.0.0.1:5000
```

## Step 6: Test it

Open your browser and go to `http://127.0.0.1:5000`

Try these URLs:
- `https://www.google.com` (should be safe)
- `http://192.168.1.1/login` (might be flagged as suspicious)

## Troubleshooting

### "Model not found" error

The model file is missing. Make sure `pickle/model.pkl` is in the right place. If you don't have it, you'll need to train the model using `train_model.py`.

### "No module named 'numpy'" or similar

You probably forgot to activate the virtual environment. Do this:
```bash
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

Then install packages again:
```bash
pip install -r requirements.txt
```

### Port 5000 already in use

Something else is using that port. Either:
1. Close whatever is using port 5000, or
2. Change the port in app.py:
   ```python
   app.run(debug=True, port=5001)
   ```
   Then access it at `http://127.0.0.1:5001`

### Packages won't install

A few things to check:
- Python version (needs to be 3.11 or 3.12)
- pip might be outdated (try `python -m pip install --upgrade pip`)
- Internet connection

If Python version is wrong:
```bash
# Use specific version
py -3.12 -m venv .venv  # Windows
python3.12 -m venv .venv  # Linux/Mac
```

### "This type of URL does not exist" error

The URL validation is being strict. Make sure:
- The URL has a real domain (like example.com)
- Don't just type random letters
- Include http:// or https:// if needed

Valid examples:
- ✅ `https://www.google.com`
- ✅ `google.com`
- ❌ `asdfghjkl` (random letters)
- ❌ `test` (no domain)

## Verify it works

Run the test script:
```bash
python test_system.py
```

It'll test a few URLs and show you the results. If everything passes, you're good to go!

## Quick reference

**Activate virtual environment:**
```bash
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

**Run the app:**
```bash
python app.py
```

**Deactivate when done:**
```bash
deactivate
```

## What's next?

Once it's running:
- Try checking different URLs
- Check out the History page to see past checks
- Look at the About page to learn more about the features
- If you're a developer, check out the API endpoints

## Performance note

The first URL check might take 5-10 seconds because it needs to do external lookups (whois, DNS, etc.). After that, it's usually faster (2-5 seconds). The actual ML prediction is super fast, but getting all the feature data takes time.

That's it! You should be up and running now. If you run into issues, check the main README.md for more details.
