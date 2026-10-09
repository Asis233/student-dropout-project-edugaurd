import os
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import (
    precision_score, recall_score, f1_score, roc_auc_score,
    confusion_matrix, classification_report
)

NUMERICAL_FEATURES = [
    'attendance_rate',
    'gpa',
    'previous_gpa',
    'gpa_change',
    'assignment_completion_rate',
    'late_submissions_count',
    'library_visits_monthly',
    'lms_login_frequency_weekly',
    'failed_courses_count',
    'tuition_fee_delinquent',
    'semester'
]

CATEGORICAL_FEATURES = [
    'department',
    'financial_aid_status'
]

TARGET = 'dropout_target'

def train_and_evaluate():
    data_path = os.path.join("data", "student_data.csv")
    if not os.path.exists(data_path):
        from generate_data import generate_student_dataset
        df = generate_student_dataset(n_samples=650)
        os.makedirs("data", exist_ok=True)
        df.to_csv(data_path, index=False)
    else:
        df = pd.read_csv(data_path)

    X = df[NUMERICAL_FEATURES + CATEGORICAL_FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), NUMERICAL_FEATURES),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), CATEGORICAL_FEATURES)
        ]
    )

    gb_classifier = GradientBoostingClassifier(
        n_estimators=130,
        learning_rate=0.07,
        max_depth=4,
        subsample=0.85,
        random_state=42
    )

    model_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', gb_classifier)
    ])

    model_pipeline.fit(X_train, y_train)

    y_pred = model_pipeline.predict(X_test)
    y_proba = model_pipeline.predict_proba(X_test)[:, 1]

    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    roc_auc = roc_auc_score(y_test, y_proba)
    cm = confusion_matrix(y_test, y_pred).tolist()

    # Get feature names after one-hot encoding
    cat_encoder = model_pipeline.named_steps['preprocessor'].named_transformers_['cat']
    encoded_cat_names = list(cat_encoder.get_feature_names_out(CATEGORICAL_FEATURES))
    all_feature_names = NUMERICAL_FEATURES + encoded_cat_names

    feature_importances = model_pipeline.named_steps['classifier'].feature_importances_
    importance_dict = dict(zip(all_feature_names, [round(float(val), 4) for val in feature_importances]))

    metrics = {
        "precision": round(float(prec), 4),
        "recall": round(float(rec), 4),
        "f1_score": round(float(f1), 4),
        "roc_auc": round(float(roc_auc), 4),
        "confusion_matrix": cm,
        "n_train": len(X_train),
        "n_test": len(X_test),
        "feature_importances": importance_dict,
        "model_type": "Gradient Boosting Classifier",
        "training_date": "2026-10-09"
    }

    os.makedirs("models", exist_ok=True)
    model_path = os.path.join("models", "eduguard_model.joblib")
    metrics_path = os.path.join("models", "model_metrics.json")

    joblib.dump(model_pipeline, model_path)

    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=2)

    print(f"Model successfully trained & saved to {model_path}")
    print(f"Metrics saved to {metrics_path}")
    print(f"Test Set Evaluation -> Accuracy ROC-AUC: {metrics['roc_auc']}, Precision: {metrics['precision']}, Recall: {metrics['recall']}, F1: {metrics['f1_score']}")

    return model_pipeline, metrics

if __name__ == "__main__":
    train_and_evaluate()
