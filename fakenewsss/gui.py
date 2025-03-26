# =============================
# GUI FOR FAKE NEWS DETECTION
# =============================
import pickle
import re
import tkinter as tk
from tkinter import messagebox

# Load saved model and vectorizer
with open("fake_news_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

# Simple clean text function for user input
def clean_input(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text) #remove special characters
    return text

# Predict function
def predict_news():
    news = text_entry.get("1.0", tk.END).strip()
    if not news:
        messagebox.showwarning("Input Error", "Please enter news text.")
        return

    cleaned = clean_input(news)
    vec = vectorizer.transform([cleaned])
    prediction = model.predict(vec)[0]

    result = "REAL News ✅" if prediction == 1 else "FAKE News ❌"
    result_label.config(text=f"Prediction: {result}", fg="green" if prediction == 1 else "red")

# Build GUI
app = tk.Tk()
app.title("Fake News Detector")
app.geometry("500x400")

# Input
tk.Label(app, text="Enter News Text:", font=("Arial", 14)).pack(pady=10)
text_entry = tk.Text(app, height=10, width=60)
text_entry.pack(pady=10)

# Predict button
predict_btn = tk.Button(app, text="Predict", font=("Arial", 12), command=predict_news)
predict_btn.pack(pady=10)

# Result label
result_label = tk.Label(app, text="", font=("Arial", 14, "bold"))
result_label.pack(pady=10)

app.mainloop()