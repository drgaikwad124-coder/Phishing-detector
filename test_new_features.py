"""
Quick test script for new features
"""
import requests
import json
import time

BASE_URL = "http://127.0.0.1:5000"

def test_health():
    """Test health endpoint"""
    print("Testing /health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"[OK] Health check: {response.status_code}")
        print(f"  Response: {response.json()}")
        return True
    except Exception as e:
        print(f"[FAIL] Health check failed: {e}")
        return False

def test_api_check():
    """Test API check endpoint"""
    print("\nTesting /api/check endpoint...")
    try:
        data = {"url": "https://www.google.com"}
        response = requests.post(f"{BASE_URL}/api/check", json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            print(f"[OK] API check successful")
            print(f"  URL: {result['url']}")
            print(f"  Prediction: {result['prediction']}")
            print(f"  Safe Probability: {result['safe_probability']}")
            print(f"  Phishing Probability: {result['phishing_probability']}")
            return True
        else:
            print(f"[FAIL] API check failed: {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print(f"[FAIL] API check error: {e}")
        return False

def test_batch_api():
    """Test batch API endpoint"""
    print("\nTesting /api/batch endpoint...")
    try:
        data = {"urls": ["https://www.google.com", "https://www.github.com"]}
        response = requests.post(f"{BASE_URL}/api/batch", json=data, timeout=60)
        if response.status_code == 200:
            result = response.json()
            print(f"[OK] Batch API successful")
            print(f"  Processed {len(result['results'])} URLs")
            for i, res in enumerate(result['results'], 1):
                print(f"  {i}. {res.get('url', 'N/A')}: {res.get('prediction', 'N/A')}")
            return True
        else:
            print(f"[FAIL] Batch API failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"[FAIL] Batch API error: {e}")
        return False

def test_pages():
    """Test new pages"""
    print("\nTesting new pages...")
    pages = ["/", "/about", "/history"]
    for page in pages:
        try:
            response = requests.get(f"{BASE_URL}{page}", timeout=10)
            if response.status_code == 200:
                print(f"[OK] {page} - OK")
            else:
                print(f"[FAIL] {page} - {response.status_code}")
        except Exception as e:
            print(f"[FAIL] {page} - Error: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("TESTING NEW FEATURES")
    print("=" * 60)
    
    # Wait a bit for server to start
    print("\nWaiting for server to start...")
    time.sleep(3)
    
    # Run tests
    test_health()
    test_pages()
    test_api_check()
    test_batch_api()
    
    print("\n" + "=" * 60)
    print("Testing complete!")
    print("=" * 60)
    print("\nOpen your browser and visit:")
    print("  - Home: http://127.0.0.1:5000")
    print("  - About: http://127.0.0.1:5000/about")
    print("  - History: http://127.0.0.1:5000/history")

