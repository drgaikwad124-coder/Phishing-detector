"""
Train phishing detection model with your phishing.csv data
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score
import pickle
import os

def load_data(filepath='phishing.csv'):
    """Load and inspect the CSV data"""
    print("="*60)
    print("LOADING DATA")
    print("="*60)
    
    # Load CSV
    print(f"\nLoading {filepath}...")
    df = pd.read_csv(filepath)
    
    # Show basic info
    print(f"\n✓ Data loaded successfully!")
    print(f"  Shape: {df.shape}")
    print(f"  Columns: {len(df.columns)}")
    print(f"  Rows: {len(df)}")
    
    # Show first few rows
    print("\nFirst 5 rows:")
    print(df.head())
    
    # Show column names
    print("\nColumn names:")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i}. {col}")
    
    # Check for missing values
    missing = df.isnull().sum().sum()
    print(f"\nMissing values: {missing}")
    
    return df

def prepare_data(df):
    """Prepare features and labels"""
    print("\n" + "="*60)
    print("PREPARING DATA")
    print("="*60)
    
    # Common label column names
    label_candidates = ['label', 'class', 'target', 'Result', 'CLASS_LABEL', 'phishing']
    
    # Find label column
    label_col = None
    for col in df.columns:
        if col.lower() in [c.lower() for c in label_candidates]:
            label_col = col
            break
    
    if label_col is None:
        # If not found, assume last column is the label
        label_col = df.columns[-1]
        print(f"\n⚠️  Label column not found. Assuming last column '{label_col}' is the label.")
    else:
        print(f"\n✓ Found label column: '{label_col}'")
    

    df = df.drop(columns=['Index'])


    # Separate features and labels
    X = df.drop(label_col, axis=1)
    y = df[label_col]
    
    print(f"\nFeatures shape: {X.shape}")
    print(f"Labels shape: {y.shape}")
    
    # Check label distribution
    print(f"\nLabel distribution:")
    print(y.value_counts())
    
    # Convert labels to -1 and 1 if needed
    unique_labels = y.unique()
    print(f"\nUnique labels: {unique_labels}")
    
    if set(unique_labels) != {-1, 1}:
        print("\n⚠️  Converting labels to -1 (phishing) and 1 (safe)...")
        # Common conversions
        if set(unique_labels) == {0, 1}:
            # 0 -> -1 (phishing), 1 -> 1 (safe)
            y = y.replace({0: -1, 1: 1})
        elif set(unique_labels) == {1, 2}:
            # 1 -> 1 (safe), 2 -> -1 (phishing) OR opposite
            # Check which is more common (assume legit is more common)
            if y.value_counts()[1] > y.value_counts()[2]:
                y = y.replace({1: 1, 2: -1})
            else:
                y = y.replace({1: -1, 2: 1})
        elif 'phishing' in str(unique_labels[0]).lower() or 'bad' in str(unique_labels[0]).lower():
            # String labels
            phishing_label = [l for l in unique_labels if 'phishing' in str(l).lower() or 'bad' in str(l).lower()][0]
            safe_label = [l for l in unique_labels if l != phishing_label][0]
            y = y.replace({phishing_label: -1, safe_label: 1})
        
        print(f"✓ Converted labels: {y.unique()}")
    
    print(f"\nFinal distribution:")
    print(f"  Safe (1): {sum(y == 1)}")
    print(f"  Phishing (-1): {sum(y == -1)}")
    
    return X.values, y.values

def train_models(X_train, X_test, y_train, y_test):
    """Train and compare different models"""
    print("\n" + "="*60)
    print("TRAINING MODELS")
    print("="*60)
    
    models = {
        'Gradient Boosting': GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=4,
            random_state=42,
            verbose=0
        ),
        'Random Forest': RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
    }
    
    results = {}
    
    for name, model in models.items():
        print(f"\n{'='*40}")
        print(f"Training {name}...")
        print('='*40)
        
        # Train
        model.fit(X_train, y_train)
        
        # Predict
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)
        
        # Evaluate
        accuracy = accuracy_score(y_test, y_pred)
        
        # Cross-validation
        cv_scores = cross_val_score(model, X_train, y_train, cv=5)
        
        print(f"\nResults for {name}:")
        print(f"  Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
        print(f"  Cross-val score: {cv_scores.mean():.4f} (±{cv_scores.std():.4f})")
        
        try:
            roc_auc = roc_auc_score(y_test, y_pred_proba[:, 1])
            print(f"  ROC-AUC: {roc_auc:.4f}")
        except:
            pass
        
        print(f"\nClassification Report:")
        print(classification_report(y_test, y_pred, 
                                   target_names=['Phishing (-1)', 'Safe (1)']))
        
        print(f"\nConfusion Matrix:")
        cm = confusion_matrix(y_test, y_pred)
        print(cm)
        print(f"  True Negatives: {cm[0][0]}")
        print(f"  False Positives: {cm[0][1]}")
        print(f"  False Negatives: {cm[1][0]}")
        print(f"  True Positives: {cm[1][1]}")
        
        results[name] = {
            'model': model,
            'accuracy': accuracy,
            'cv_score': cv_scores.mean()
        }
    
    # Select best model
    best_name = max(results, key=lambda x: results[x]['accuracy'])
    best_model = results[best_name]['model']
    
    print("\n" + "="*60)
    print(f"BEST MODEL: {best_name}")
    print(f"Accuracy: {results[best_name]['accuracy']:.4f}")
    print("="*60)
    
    return best_model, results

def save_model(model, filepath='pickle/model.pkl'):
    """Save the trained model"""
    # Create pickle directory if it doesn't exist
    os.makedirs('pickle', exist_ok=True)
    
    print(f"\nSaving model to {filepath}...")
    with open(filepath, 'wb') as f:
        pickle.dump(model, f)
    
    print("✓ Model saved successfully!")
    
    # Also save model info
    info_path = 'pickle/model_info.txt'
    with open(info_path, 'w') as f:
        import sklearn
        f.write(f"Model trained on: {pd.Timestamp.now()}\n")
        f.write(f"Scikit-learn version: {sklearn.__version__}\n")
        f.write(f"Model type: {type(model).__name__}\n")
    
    print(f"✓ Model info saved to {info_path}")

def test_model(model, X_test, y_test):
    """Test the model with sample cases"""
    print("\n" + "="*60)
    print("TESTING MODEL")
    print("="*60)
    
    # Random samples
    indices = np.random.choice(len(X_test), min(5, len(X_test)), replace=False)
    
    for i, idx in enumerate(indices, 1):
        features = X_test[idx].reshape(1, -1)
        actual = y_test[idx]
        
        pred = model.predict(features)[0]
        proba = model.predict_proba(features)[0]
        
        print(f"\nSample {i}:")
        print(f"  Actual: {'SAFE' if actual == 1 else 'PHISHING'}")
        print(f"  Predicted: {'SAFE' if pred == 1 else 'PHISHING'}")
        print(f"  Confidence: {max(proba)*100:.2f}%")
        print(f"  Match: {'✓' if pred == actual else '✗'}")

def plot_feature_importance(model, feature_names=None):
    """Plot feature importance if available"""
    try:
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
            
            if feature_names is None:
                feature_names = [f"Feature {i+1}" for i in range(len(importances))]
            
            # Get top 15 features
            indices = np.argsort(importances)[-15:]
            
            print("\nTop 15 Feature Importances:")
            for i, idx in enumerate(indices[::-1], 1):
                print(f"  {i}. {feature_names[idx]}: {importances[idx]:.4f}")
    except Exception as e:
        print(f"\n⚠️  Could not analyze feature importance: {e}")

def main():
    print("="*60)
    print("PHISHING DETECTION MODEL TRAINING")
    print("="*60)
    
    # Check scikit-learn version
    import sklearn
    print(f"\nPython packages:")
    print(f"  scikit-learn: {sklearn.__version__}")
    print(f"  pandas: {pd.__version__}")
    print(f"  numpy: {np.__version__}")
    
    try:
        # Load data
        df = load_data('phishing.csv')
        
        # Prepare data
        X, y = prepare_data(df)
        
        # Split data
        print("\n" + "="*60)
        print("SPLITTING DATA")
        print("="*60)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        print(f"\nTraining set: {len(X_train)} samples")
        print(f"Testing set: {len(X_test)} samples")
        
        # Train models
        best_model, results = train_models(X_train, X_test, y_train, y_test)
        
        # Save model
        save_model(best_model)
        
        # Test model
        test_model(best_model, X_test, y_test)
        
        # Plot feature importance
        plot_feature_importance(best_model)
        
        print("\n" + "="*60)
        print("✓ TRAINING COMPLETE!")
        print("="*60)
        print("\nNext steps:")
        print("  1. Run: python app.py")
        print("  2. Open: http://127.0.0.1:5000")
        print("  3. Test your phishing detector!")
        print("\nModel file: pickle/model.pkl")
        
    except FileNotFoundError:
        print("\n✗ ERROR: phishing.csv not found!")
        print("\nPlease ensure 'phishing.csv' is in the same directory.")
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()