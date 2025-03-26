import pickle
import tkinter as tk
from tkinter import messagebox, ttk
import numpy as np
import pandas as pd  # Fix feature name warning

# Load saved model and scaler
try:
    with open("housing_model.pkl", "rb") as f:
        model = pickle.load(f)

    with open("housing_scaler.pkl", "rb") as f:
        scaler = pickle.load(f)

except FileNotFoundError:
    messagebox.showerror("Error", "Model files not found! Ensure 'housing_model.pkl' and 'housing_scaler.pkl' exist.")
    exit()

# Predict function
def predict_price():
    try:
        # Get user inputs
        features = [float(entry.get()) for entry in feature_entries]
        
        # Convert to DataFrame with correct feature names
        features_df = pd.DataFrame([features], columns=feature_names)

        # Scale the input
        features_scaled = scaler.transform(features_df)  # No warning now!

        # Predict house price
        prediction = model.predict(features_scaled)[0]

        # Show result
        result_label.config(text=f"🏠 Predicted Price: ${prediction:.2f}", fg="white", bg="#1E88E5")

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numerical values.")

# Build GUI
app = tk.Tk()
app.title("🏡 Housing Price Predictor")
app.geometry("600x700")
app.configure(bg="#E3F2FD")  # Light Blue Background

tk.Label(app, text="Enter Housing Features:", font=("Arial", 18, "bold"), fg="black", bg="#E3F2FD").pack(pady=10)

# Feature labels & input fields
feature_names = ["MedInc", "HouseAge", "AveRooms", "AveBedrms", "Population", "AveOccup", "Latitude", "Longitude"]
feature_entries = []

frame = tk.Frame(app, bg="#E3F2FD")
frame.pack(pady=10)

for feature in feature_names:
    row_frame = tk.Frame(frame, bg="#E3F2FD")
    row_frame.pack(fill="x", padx=10, pady=5)

    label = tk.Label(row_frame, text=f"{feature}:", font=("Arial", 12, "bold"), fg="black", bg="#E3F2FD", width=15, anchor="w")
    label.pack(side="left")

    entry = ttk.Entry(row_frame, font=("Arial", 12), width=25)
    entry.pack(side="right")
    feature_entries.append(entry)

# Predict button with hover effect
def on_enter(e):
    predict_btn.config(bg="#0056b3")

def on_leave(e):
    predict_btn.config(bg="#007BFF")

predict_btn = tk.Button(
    app, text="📊 Predict Price", font=("Arial", 14, "bold"),
    bg="#007BFF", fg="white", padx=10, pady=5, relief="raised",
    command=predict_price
)
predict_btn.bind("<Enter>", on_enter)
predict_btn.bind("<Leave>", on_leave)
predict_btn.pack(pady=20)

# Result label
result_label = tk.Label(app, text="", font=("Arial", 14, "bold"), width=50, height=2, bg="#E3F2FD")
result_label.pack(pady=10)

app.mainloop()
