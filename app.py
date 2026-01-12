# importing required libraries
from flask import Flask, request, render_template, jsonify
import numpy as np
import pandas as pd
from sklearn import metrics 
import warnings
import pickle
import logging
from urllib.parse import urlparse
from datetime import datetime
import json
import os
import re
import webbrowser
import threading
import time

warnings.filterwarnings('ignore')

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import the fixed FeatureExtraction class
from feature import FeatureExtraction

# Load the trained model
try:
    file = open("pickle/model.pkl", "rb")
    gbc = pickle.load(file)
    file.close()
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Error loading model: {e}")
    gbc = None

app = Flask(__name__)

# In-memory storage for history (in production, use a database)
HISTORY_FILE = "url_history.json"

def load_history():
    """Load URL checking history from file"""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_history(entry):
    """Save a new entry to history"""
    history = load_history()
    history.append(entry)
    # Keep only last 100 entries
    if len(history) > 100:
        history = history[-100:]
    try:
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        logger.error(f"Error saving history: {e}")

def contains_random_alphabets(url):
    """Check if URL contains random/invalid characters that don't form a valid URL"""
    # Remove scheme for domain checking
    domain_part = url
    if '://' in url:
        domain_part = url.split('://', 1)[1]
    
    # Remove path, query, fragment
    if '/' in domain_part:
        domain_part = domain_part.split('/', 1)[0]
    if '?' in domain_part:
        domain_part = domain_part.split('?', 1)[0]
    if '#' in domain_part:
        domain_part = domain_part.split('#', 1)[0]
    
    # Check if domain is empty or just random characters
    if not domain_part or len(domain_part) < 3:
        return True
    
    # Check for valid domain pattern: should contain at least one dot and valid characters
    # Valid domain: letters, numbers, dots, hyphens
    domain_pattern = re.compile(r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*\.[a-zA-Z]{2,}$')
    
    # If it doesn't match domain pattern and is just random characters
    if not domain_pattern.match(domain_part):
        # Check if it's just random alphabets without proper structure
        if not '.' in domain_part:
            return True
        # Check if it has too many random characters without proper TLD
        parts = domain_part.split('.')
        if len(parts) < 2:
            return True
        # Check if TLD is valid (at least 2 characters, letters only)
        tld = parts[-1]
        if len(tld) < 2 or not tld.isalpha():
            return True
    
    return False

def is_valid_url(url):
    """Validate URL format and check for invalid/random characters"""
    try:
        result = urlparse(url)
        
        # Basic validation
        if not all([result.scheme, result.netloc]):
            return False, "Invalid URL format. Missing scheme or domain."
        
        # Check for random alphabets/invalid domain
        if contains_random_alphabets(url):
            return False, "This type of URL does not exist. Please enter a valid URL with proper domain name (e.g., example.com)."
        
        # Validate domain format
        domain = result.netloc.lower()
        
        # Remove port if present
        if ':' in domain:
            domain = domain.split(':')[0]
        
        # Check domain length
        if len(domain) > 253:
            return False, "Domain name is too long. Please enter a valid URL."
        
        # Check for valid characters in domain
        if not re.match(r'^[a-zA-Z0-9]([a-zA-Z0-9\-\.]{0,251}[a-zA-Z0-9])?$', domain):
            return False, "Invalid characters in domain name. Please enter a valid URL."
        
        # Check if domain has at least one dot (for TLD)
        if '.' not in domain:
            return False, "Invalid domain format. Domain must include a top-level domain (e.g., .com, .org)."
        
        # Check TLD format
        parts = domain.split('.')
        if len(parts) < 2:
            return False, "Invalid domain format. Please enter a valid URL."
        
        tld = parts[-1]
        if len(tld) < 2 or not tld.isalpha():
            return False, "Invalid top-level domain. Please enter a valid URL."
        
        return True, None
        
    except Exception as e:
        return False, f"Invalid URL format: {str(e)}"

def normalize_url(url):
    """Add http:// if no scheme is provided"""
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    return url

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            # Get URL from form
            url = request.form["url"].strip()
            
            # Validate URL
            if not url:
                return render_template('index.html', 
                                     error="Please enter a URL", 
                                     xx=-1)
            
            # Normalize URL (add http:// if missing)
            url = normalize_url(url)
            
            # Validate URL format
            is_valid, error_msg = is_valid_url(url)
            if not is_valid:
                return render_template('index.html', 
                                     error=error_msg or "Invalid URL format. Please enter a valid URL.", 
                                     xx=-1)
            
            # Check if model is loaded
            if gbc is None:
                return render_template('index.html', 
                                     error="Model not loaded. Please check model file.", 
                                     xx=-1)
            
            # Extract features
            logger.info(f"Analyzing URL: {url}")
            obj = FeatureExtraction(url)
            features = obj.getFeaturesList()
            
            # Check if feature extraction was successful
            if len(features) != 30:
                logger.warning(f"Expected 30 features, got {len(features)}")
                return render_template('index.html', 
                                     error="Error extracting features from URL", 
                                     xx=-1)
            
            # Reshape features for prediction
            x = np.array(features).reshape(1, 30)
            
            # Make prediction
            y_pred = gbc.predict(x)[0]
            # 1 is safe, -1 is unsafe
            
            # Get probability scores
            y_pro_phishing = gbc.predict_proba(x)[0, 0]      # Probability of being phishing
            y_pro_non_phishing = gbc.predict_proba(x)[0, 1]  # Probability of being safe
            
            logger.info(f"Prediction: {'Safe' if y_pred == 1 else 'Phishing'} "
                       f"(Safe: {y_pro_non_phishing:.2%}, Phishing: {y_pro_phishing:.2%})")
            
            # Save to history
            history_entry = {
                'url': url,
                'prediction': 'Safe' if y_pred == 1 else 'Phishing',
                'safe_probability': round(y_pro_non_phishing, 2),
                'phishing_probability': round(y_pro_phishing, 2),
                'timestamp': datetime.now().isoformat(),
                'features': features
            }
            save_history(history_entry)
            
            # Return results
            return render_template('index.html',
                                 xx=round(y_pro_non_phishing, 2),
                                 phishing_prob=round(y_pro_phishing, 2),
                                 url=url,
                                 prediction=y_pred,
                                 features=features)
                                 
        except Exception as e:
            logger.error(f"Error processing URL: {str(e)}")
            return render_template('index.html', 
                                 error=f"Error analyzing URL: {str(e)}", 
                                 xx=-1)
    
    # GET request - show initial form
    return render_template("index.html", xx=-1)

@app.route("/about")
def about():
    """About/Features page"""
    return render_template('about.html')

@app.route("/history")
def history():
    """History/Statistics page"""
    history_data = load_history()
    
    # Calculate statistics
    total_checks = len(history_data)
    safe_count = sum(1 for entry in history_data if entry.get('prediction') == 'Safe')
    phishing_count = total_checks - safe_count
    
    # Get recent entries (last 20) - reverse to show newest first
    recent_entries = history_data[-20:][::-1] if history_data else []
    
    # Ensure all entries have required fields
    for entry in recent_entries:
        if 'url' not in entry:
            entry['url'] = 'Unknown URL'
        if 'prediction' not in entry:
            entry['prediction'] = 'Unknown'
        if 'safe_probability' not in entry:
            entry['safe_probability'] = 0.0
        if 'phishing_probability' not in entry:
            entry['phishing_probability'] = 0.0
        if 'timestamp' not in entry:
            entry['timestamp'] = datetime.now().isoformat()
    
    stats = {
        'total_checks': total_checks,
        'safe_count': safe_count,
        'phishing_count': phishing_count,
        'safe_percentage': round((safe_count / total_checks * 100) if total_checks > 0 else 0, 2),
        'phishing_percentage': round((phishing_count / total_checks * 100) if total_checks > 0 else 0, 2)
    }
    
    logger.info(f"History page: {total_checks} total checks, showing {len(recent_entries)} recent entries")
    
    return render_template('history.html', history=recent_entries, stats=stats)

@app.route("/api/check", methods=["POST"])
def api_check():
    """API endpoint for programmatic URL checking"""
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({'error': 'URL is required'}), 400
        
        url = data['url'].strip()
        
        # Normalize URL
        url = normalize_url(url)
        
        # Validate URL
        is_valid, error_msg = is_valid_url(url)
        if not is_valid:
            return jsonify({'error': error_msg or 'Invalid URL format'}), 400
        
        if gbc is None:
            return jsonify({'error': 'Model not loaded'}), 500
        
        # Extract features
        obj = FeatureExtraction(url)
        features = obj.getFeaturesList()
        
        if len(features) != 30:
            return jsonify({'error': 'Feature extraction failed'}), 500
        
        # Make prediction
        x = np.array(features).reshape(1, 30)
        y_pred = gbc.predict(x)[0]
        y_pro_phishing = gbc.predict_proba(x)[0, 0]
        y_pro_non_phishing = gbc.predict_proba(x)[0, 1]
        
        result = {
            'url': url,
            'prediction': 'Safe' if y_pred == 1 else 'Phishing',
            'safe_probability': round(y_pro_non_phishing, 2),
            'phishing_probability': round(y_pro_phishing, 2),
            'features': features,
            'timestamp': datetime.now().isoformat()
        }
        
        # Save to history
        save_history(result)
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"API error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route("/api/batch", methods=["POST"])
def api_batch():
    """API endpoint for batch URL checking"""
    try:
        data = request.get_json()
        if not data or 'urls' not in data:
            return jsonify({'error': 'URLs array is required'}), 400
        
        urls = data['urls']
        if not isinstance(urls, list) or len(urls) == 0:
            return jsonify({'error': 'URLs must be a non-empty array'}), 400
        
        if len(urls) > 10:
            return jsonify({'error': 'Maximum 10 URLs allowed per batch'}), 400
        
        if gbc is None:
            return jsonify({'error': 'Model not loaded'}), 500
        
        results = []
        for url in urls:
            try:
                url = url.strip()
                url = normalize_url(url)
                
                is_valid, error_msg = is_valid_url(url)
                if not is_valid:
                    results.append({
                        'url': url,
                        'error': error_msg or 'Invalid URL format'
                    })
                    continue
                
                obj = FeatureExtraction(url)
                features = obj.getFeaturesList()
                
                if len(features) != 30:
                    results.append({
                        'url': url,
                        'error': 'Feature extraction failed'
                    })
                    continue
                
                x = np.array(features).reshape(1, 30)
                y_pred = gbc.predict(x)[0]
                y_pro_phishing = gbc.predict_proba(x)[0, 0]
                y_pro_non_phishing = gbc.predict_proba(x)[0, 1]
                
                result = {
                    'url': url,
                    'prediction': 'Safe' if y_pred == 1 else 'Phishing',
                    'safe_probability': round(y_pro_non_phishing, 2),
                    'phishing_probability': round(y_pro_phishing, 2)
                }
                results.append(result)
                
                # Save to history
                save_history({
                    **result,
                    'features': features,
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                results.append({
                    'url': url,
                    'error': str(e)
                })
        
        return jsonify({'results': results}), 200
        
    except Exception as e:
        logger.error(f"Batch API error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route("/health")
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "model_loaded": gbc is not None
    })

@app.errorhandler(404)
def not_found(e):
    return render_template('index.html', error="Page not found", xx=-1), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('index.html', error="Server error occurred", xx=-1), 500

def open_browser():
    """Open the browser after a short delay to ensure server is ready"""
    time.sleep(1.5)  # Wait 1.5 seconds for server to start
    webbrowser.open('http://127.0.0.1:5000')

if __name__ == "__main__":
    # Start browser in a separate thread
    threading.Thread(target=open_browser).start()
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)