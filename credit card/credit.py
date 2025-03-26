import os
import pandas as pd
import numpy as np
import joblib  # For saving the model & scaler
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score

# Load the dataset
file_path = r"C:\\Users\\User\\Desktop\\credit card\\dataset\\record.csv"
df = pd.read_csv(file_path)

# Drop rows with missing 'approved' values
df.dropna(subset=['approved'], inplace=True)

# Handle missing values in categorical columns by filling with 'Unknown'
categorical_cols = df.select_dtypes(include=['object']).columns
df[categorical_cols] = df[categorical_cols].fillna('Unknown')

# Encode categorical features
label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Replace missing numerical values with mean
imputer = SimpleImputer(strategy='mean')
numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns
df[numerical_cols] = imputer.fit_transform(df[numerical_cols])

# Define features and target variable
X = df.drop(columns=['ID', 'approved'])  # Features (excluding ID and target)
y = df['approved']  # Target (1 = Approved, 0 = Not Approved)

# Standardize numerical features
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Split into training & testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train multiple models
models = {
    "Logistic Regression": LogisticRegression(),
    "Decision Tree": DecisionTreeClassifier(),
    "Random Forest": RandomForestClassifier(),
    "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric="logloss")
}

best_model = None
best_accuracy = 0
model_results = {}

# Train and evaluate each model
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    model_results[name] = accuracy

    print(f"{name} Accuracy: {accuracy:.4f}")

    # Save the best model
    if accuracy > best_accuracy:
        best_accuracy = accuracy
        best_model = model

# Create 'model' folder if it doesn't exist
model_folder = r"C:\\Users\\User\\Desktop\\credit card\\model"
os.makedirs(model_folder, exist_ok=True)

# Save the best model in the 'model' folder
best_model_path = os.path.join(model_folder, "best_credit_model.pkl")
joblib.dump(best_model, best_model_path)

# Save the scaler in the 'model' folder
scaler_path = os.path.join(model_folder, "scaler.pkl")
joblib.dump(scaler, scaler_path)

print(f"\nBest Model: {best_model} with Accuracy: {best_accuracy:.4f}")
print(f"Model saved at: {best_model_path}")
print(f"Scaler saved at: {scaler_path}")