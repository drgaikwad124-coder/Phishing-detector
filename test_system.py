"""
Testing script for Phishing Detection System
Tests the FeatureExtraction class and model predictions
"""

import numpy as np
import pickle
from feature import FeatureExtraction
import time

def test_feature_extraction():
    """Test feature extraction with sample URLs"""
    
    print("=" * 60)
    print("PHISHING DETECTION SYSTEM - TEST SUITE")
    print("=" * 60)
    
    # Test URLs
    test_cases = [
        {
            "url": "https://www.google.com",
            "expected": "Safe",
            "description": "Popular legitimate site"
        },
        {
            "url": "http://192.168.1.1/login",
            "expected": "Suspicious",
            "description": "IP address URL"
        },
        {
            "url": "https://bit.ly/test123",
            "expected": "Suspicious",
            "description": "URL shortener"
        },
        {
            "url": "https://secure-bank@phishing.com",
            "expected": "Suspicious",
            "description": "URL with @ symbol"
        },
        {
            "url": "https://www.github.com",
            "expected": "Safe",
            "description": "Popular legitimate site"
        }
    ]
    
    # Load model
    try:
        with open("pickle/model.pkl", "rb") as file:
            model = pickle.load(file)
        print("\n✓ Model loaded successfully\n")
    except Exception as e:
        print(f"\n✗ Error loading model: {e}")
        print("Please ensure model.pkl exists in the pickle/ directory\n")
        return
    
    # Test each URL
    results = []
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['description']}")
        print(f"URL: {test_case['url']}")
        print(f"Expected: {test_case['expected']}")
        
        try:
            # Extract features
            start_time = time.time()
            obj = FeatureExtraction(test_case['url'])
            features = obj.getFeaturesList()
            extraction_time = time.time() - start_time
            
            # Check feature count
            if len(features) != 30:
                print(f"✗ Warning: Expected 30 features, got {len(features)}")
                continue
            
            # Make prediction
            x = np.array(features).reshape(1, 30)
            prediction = model.predict(x)[0]
            probabilities = model.predict_proba(x)[0]
            
            # Interpret results
            is_safe = prediction == 1
            safe_prob = probabilities[1] * 100
            phishing_prob = probabilities[0] * 100
            
            print(f"Result: {'SAFE ✓' if is_safe else 'PHISHING ✗'}")
            print(f"Safe Probability: {safe_prob:.2f}%")
            print(f"Phishing Probability: {phishing_prob:.2f}%")
            print(f"Processing Time: {extraction_time:.2f}s")
            
            # Store results
            results.append({
                'url': test_case['url'],
                'expected': test_case['expected'],
                'prediction': 'Safe' if is_safe else 'Phishing',
                'safe_prob': safe_prob,
                'time': extraction_time
            })
            
        except Exception as e:
            print(f"✗ Error: {str(e)}")
            results.append({
                'url': test_case['url'],
                'expected': test_case['expected'],
                'prediction': 'Error',
                'error': str(e)
            })
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['url']}")
        if 'error' in result:
            print(f"   Status: ERROR - {result['error']}")
        else:
            print(f"   Prediction: {result['prediction']} ({result['safe_prob']:.1f}% safe)")
            print(f"   Processing Time: {result['time']:.2f}s")
    
    # Feature breakdown for first URL
    if results:
        print("\n" + "=" * 60)
        print("DETAILED FEATURE ANALYSIS (First URL)")
        print("=" * 60)
        
        feature_names = [
            "1. Using IP Address", "2. Long URL", "3. Short URL Service",
            "4. Symbol @", "5. Redirecting //", "6. Prefix/Suffix",
            "7. SubDomains", "8. HTTPS", "9. Domain Registration Length",
            "10. Favicon", "11. Non-Standard Port", "12. HTTPS in Domain",
            "13. Request URL", "14. Anchor URL", "15. Links in Script Tags",
            "16. Server Form Handler", "17. Info Email", "18. Abnormal URL",
            "19. Website Forwarding", "20. Status Bar Customization",
            "21. Disable Right Click", "22. Using Popup Window", 
            "23. Iframe Redirection", "24. Age of Domain", "25. DNS Recording",
            "26. Website Traffic", "27. PageRank", "28. Google Index",
            "29. Links Pointing to Page", "30. Stats Report"
        ]
        
        try:
            obj = FeatureExtraction(test_cases[0]['url'])
            features = obj.getFeaturesList()
            
            suspicious_features = []
            safe_features = []
            
            for name, value in zip(feature_names, features):
                if value == -1:
                    suspicious_features.append(name)
                elif value == 1:
                    safe_features.append(name)
            
            print(f"\n✓ Safe Features ({len(safe_features)}):")
            for feature in safe_features[:5]:  # Show first 5
                print(f"   - {feature}")
            if len(safe_features) > 5:
                print(f"   ... and {len(safe_features) - 5} more")
            
            print(f"\n✗ Suspicious Features ({len(suspicious_features)}):")
            for feature in suspicious_features:
                print(f"   - {feature}")
                
        except Exception as e:
            print(f"\nError in detailed analysis: {e}")

def test_individual_features():
    """Test individual feature extraction methods"""
    print("\n" + "=" * 60)
    print("INDIVIDUAL FEATURE TESTS")
    print("=" * 60)
    
    test_url = "https://www.example.com"
    print(f"\nTesting URL: {test_url}\n")
    
    try:
        obj = FeatureExtraction(test_url)
        
        tests = [
            ("IP Address Check", obj.UsingIp()),
            ("URL Length Check", obj.longUrl()),
            ("Short URL Check", obj.shortUrl()),
            ("@ Symbol Check", obj.symbol()),
            ("HTTPS Check", obj.Hppts()),
            ("Subdomain Check", obj.SubDomains()),
        ]
        
        for test_name, result in tests:
            status = "✓ PASS" if result in [-1, 0, 1] else "✗ FAIL"
            interpretation = {
                -1: "Suspicious",
                0: "Neutral",
                1: "Safe"
            }.get(result, "Unknown")
            print(f"{status} {test_name}: {interpretation} ({result})")
            
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == "__main__":
    # Run all tests
    test_feature_extraction()
    test_individual_features()
    
    print("\n" + "=" * 60)
    print("Testing complete!")
    print("=" * 60)