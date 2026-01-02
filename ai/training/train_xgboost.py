"""
Skill Lantern - XGBoost Model Training

Train a career recommendation model using XGBoost classifier.
"""

import os
import sys
import json
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    top_k_accuracy_score,
)
from xgboost import XGBClassifier

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class CareerModelTrainer:
    """
    Train XGBoost model for career recommendation.
    """
    
    def __init__(
        self,
        data_path: str = None,
        output_path: str = None,
        random_state: int = 42
    ):
        """
        Initialize the trainer.
        
        Args:
            data_path: Path to training data CSV
            output_path: Path to save trained model
            random_state: Random seed for reproducibility
        """
        base_path = Path(__file__).parent.parent
        
        self.data_path = Path(data_path) if data_path else base_path / "data" / "processed" / "career_dataset.csv"
        self.output_path = Path(output_path) if output_path else base_path / "models" / "trained"
        self.random_state = random_state
        
        # Components
        self.model = None
        self.label_encoder = LabelEncoder()
        self.scaler = StandardScaler()
        self.feature_names = []
        
        # Data
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        
        # Ensure output directory exists
        self.output_path.mkdir(parents=True, exist_ok=True)
    
    def load_data(self) -> pd.DataFrame:
        """Load and validate training data"""
        print(f"\n📂 Loading data from {self.data_path}")
        
        if not self.data_path.exists():
            print(f"❌ Data file not found: {self.data_path}")
            print("\nPlease create training data with these columns:")
            print("  - math_score, science_score, english_score, gpa")
            print("  - skill_* columns (1-5 scale)")
            print("  - interest_* columns (1-5 scale)")
            print("  - career_label (target)")
            raise FileNotFoundError(f"Training data not found: {self.data_path}")
        
        df = pd.read_csv(self.data_path)
        
        print(f"✅ Loaded {len(df)} samples")
        print(f"   Columns: {list(df.columns)}")
        print(f"   Career labels: {df['career_label'].nunique()} unique")
        
        return df
    
    def preprocess_data(self, df: pd.DataFrame):
        """
        Preprocess data for training.
        
        Args:
            df: Raw dataframe
        """
        print("\n🔧 Preprocessing data...")
        
        # Separate features and target
        target_col = 'career_label'
        
        if target_col not in df.columns:
            raise ValueError(f"Target column '{target_col}' not found in data")
        
        # Get feature columns (everything except target)
        feature_cols = [col for col in df.columns if col != target_col]
        self.feature_names = feature_cols
        
        X = df[feature_cols].copy()
        y = df[target_col].copy()
        
        # Handle missing values
        X = X.fillna(0)
        
        # Normalize features
        # Academic scores (0-100) -> (0-1)
        for col in ['math_score', 'science_score', 'english_score']:
            if col in X.columns:
                X[col] = X[col] / 100.0
        
        # GPA (0-4) -> (0-1)
        if 'gpa' in X.columns:
            X[col] = X['gpa'] / 4.0
        
        # Skills and interests are already (1-5), normalize to (0-1)
        for col in X.columns:
            if col.startswith('skill_') or col.startswith('interest_'):
                X[col] = X[col] / 5.0
        
        # Encode target labels
        y_encoded = self.label_encoder.fit_transform(y)
        
        print(f"   Features: {len(self.feature_names)}")
        print(f"   Classes: {len(self.label_encoder.classes_)}")
        
        # Split data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y_encoded,
            test_size=0.2,
            random_state=self.random_state,
            stratify=y_encoded
        )
        
        # Scale features
        self.X_train = self.scaler.fit_transform(self.X_train)
        self.X_test = self.scaler.transform(self.X_test)
        
        print(f"   Training samples: {len(self.X_train)}")
        print(f"   Test samples: {len(self.X_test)}")
    
    def train(
        self,
        n_estimators: int = 200,
        max_depth: int = 6,
        learning_rate: float = 0.1,
        **kwargs
    ):
        """
        Train the XGBoost model.
        
        Args:
            n_estimators: Number of boosting rounds
            max_depth: Maximum tree depth
            learning_rate: Boosting learning rate
        """
        print("\n🚀 Training XGBoost model...")
        
        n_classes = len(self.label_encoder.classes_)
        
        self.model = XGBClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            learning_rate=learning_rate,
            objective='multi:softprob',
            num_class=n_classes,
            random_state=self.random_state,
            use_label_encoder=False,
            eval_metric='mlogloss',
            **kwargs
        )
        
        # Train with validation
        self.model.fit(
            self.X_train, self.y_train,
            eval_set=[(self.X_test, self.y_test)],
            verbose=True
        )
        
        print("✅ Training complete!")
    
    def evaluate(self) -> dict:
        """
        Evaluate the trained model.
        
        Returns:
            Dictionary with evaluation metrics
        """
        print("\n📊 Evaluating model...")
        
        # Predictions
        y_pred = self.model.predict(self.X_test)
        y_pred_proba = self.model.predict_proba(self.X_test)
        
        # Metrics
        accuracy = accuracy_score(self.y_test, y_pred)
        
        # Top-K accuracy (important for recommendation systems)
        top_3_acc = top_k_accuracy_score(self.y_test, y_pred_proba, k=3)
        top_5_acc = top_k_accuracy_score(self.y_test, y_pred_proba, k=5)
        
        # Cross-validation
        cv_scores = cross_val_score(
            self.model, self.X_train, self.y_train, cv=5, scoring='accuracy'
        )
        
        # Classification report
        class_report = classification_report(
            self.y_test, y_pred,
            target_names=self.label_encoder.classes_,
            output_dict=True
        )
        
        # Confusion matrix
        conf_matrix = confusion_matrix(self.y_test, y_pred)
        
        metrics = {
            'accuracy': accuracy,
            'top_3_accuracy': top_3_acc,
            'top_5_accuracy': top_5_acc,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'classification_report': class_report,
        }
        
        print(f"\n📈 Results:")
        print(f"   Accuracy: {accuracy:.2%}")
        print(f"   Top-3 Accuracy: {top_3_acc:.2%}")
        print(f"   Top-5 Accuracy: {top_5_acc:.2%}")
        print(f"   CV Score: {cv_scores.mean():.2%} (+/- {cv_scores.std():.2%})")
        
        return metrics
    
    def save_model(self):
        """Save trained model and components"""
        print("\n💾 Saving model...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save complete model package
        model_package = {
            'model': self.model,
            'label_encoder': self.label_encoder,
            'scaler': self.scaler,
            'feature_names': self.feature_names,
            'classes': list(self.label_encoder.classes_),
            'trained_at': timestamp,
        }
        
        # Save main model
        model_file = self.output_path / "career_model.joblib"
        joblib.dump(model_package, model_file)
        print(f"   Saved: {model_file}")
        
        # Save versioned backup
        backup_file = self.output_path / f"career_model_{timestamp}.joblib"
        joblib.dump(model_package, backup_file)
        print(f"   Backup: {backup_file}")
        
        # Save model info as JSON (for reference)
        info = {
            'feature_names': self.feature_names,
            'classes': list(self.label_encoder.classes_),
            'n_features': len(self.feature_names),
            'n_classes': len(self.label_encoder.classes_),
            'trained_at': timestamp,
        }
        
        info_file = self.output_path / "model_info.json"
        with open(info_file, 'w') as f:
            json.dump(info, f, indent=2)
        print(f"   Info: {info_file}")
        
        print("✅ Model saved successfully!")
    
    def get_feature_importance(self) -> dict:
        """Get feature importance ranking"""
        if self.model is None:
            return {}
        
        importances = self.model.feature_importances_
        
        importance_dict = {}
        for name, importance in zip(self.feature_names, importances):
            importance_dict[name] = float(importance)
        
        # Sort by importance
        sorted_importance = dict(
            sorted(importance_dict.items(), key=lambda x: x[1], reverse=True)
        )
        
        return sorted_importance
    
    def run_full_pipeline(self, **training_kwargs):
        """Run complete training pipeline"""
        print("=" * 60)
        print("🎓 Skill Lantern - Career Model Training")
        print("=" * 60)
        
        # Load data
        df = self.load_data()
        
        # Preprocess
        self.preprocess_data(df)
        
        # Train
        self.train(**training_kwargs)
        
        # Evaluate
        metrics = self.evaluate()
        
        # Save
        self.save_model()
        
        # Feature importance
        print("\n🔑 Top 10 Important Features:")
        importance = self.get_feature_importance()
        for i, (feature, score) in enumerate(list(importance.items())[:10]):
            print(f"   {i+1}. {feature}: {score:.4f}")
        
        print("\n" + "=" * 60)
        print("✅ Training pipeline complete!")
        print("=" * 60)
        
        return metrics


def main():
    """Main training entry point"""
    trainer = CareerModelTrainer()
    
    try:
        metrics = trainer.run_full_pipeline(
            n_estimators=200,
            max_depth=6,
            learning_rate=0.1,
        )
    except FileNotFoundError as e:
        print(f"\n❌ {e}")
        print("\n📝 To generate sample training data, run:")
        print("   python -m training.generate_sample_data")


if __name__ == "__main__":
    main()
