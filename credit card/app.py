from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
import datetime

app = Flask(__name__)

# Load the trained model and scaler
model = joblib.load("model\\best_credit_model.pkl")
scaler = joblib.load("model\\scaler.pkl")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        # Convert date of birth to 'days since birth'
        dob_str = data.get("DOB", "")
        if not dob_str:
            return jsonify({"error": "Date of Birth is required!"}), 400

        dob = datetime.datetime.strptime(dob_str, "%Y-%m-%d")
        days_since_birth = (datetime.datetime.today() - dob).days

        # Extract and convert input features
        input_features = np.array([
            days_since_birth,
            int(data["CODE_GENDER"]),
            int(data["FLAG_OWN_CAR"]),
            int(data["FLAG_OWN_REALTY"]),
            int(data["NAME_INCOME_TYPE"]),
            int(data["NAME_EDUCATION_TYPE"]),
            int(data["NAME_FAMILY_STATUS"]),
            int(data["NAME_HOUSING_TYPE"]),
            float(data["AMT_INCOME_TOTAL"]),
            float(data["AMT_CREDIT"]),
            float(data["AMT_ANNUITY"]),
            float(data["AMT_GOODS_PRICE"]),
            int(data["OCCUPATION_TYPE"]),
            float(data["CNT_FAM_MEMBERS"]),
            
            # 🔹 Add missing features (Set default values if not provided)
            float(data.get("EXT_SOURCE_1", 0.5)),  # Default 0.5 if missing
            float(data.get("EXT_SOURCE_2", 0.5)),  # Default 0.5 if missing
            float(data.get("EXT_SOURCE_3", 0.5))   # Default 0.5 if missing
        ]).reshape(1, -1)

        # Scale the features
        input_scaled = scaler.transform(input_features)

        # Make prediction
        prediction = model.predict(input_scaled)[0]

        # Convert prediction to readable format
        approval_status = "Approved" if prediction == 1 else "Rejected"

        return jsonify({"approval_status": approval_status})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
