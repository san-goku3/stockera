from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import tensorflow as tf
import pickle

app = Flask(__name__)
CORS(app)

# Load Model and Scaler
model = tf.keras.models.load_model("../models/best_lstm_model.h5")
with open("../models/scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Parse JSON Input
        data = request.json
        features = np.array(data['features'])  # Don't reshape here, it's already a flat list of features

        # Ensure that we have 9 features per time step (10 time steps)
        if features.shape[0] != 90:  # 9 features * 10 time steps
            return jsonify({"error": "Incorrect number of features. Expected 90 features (9 per time step for 10 time steps)."}), 400

        features = features.reshape(10, 9)  # 10 time steps, 9 features

        # Scale Features
        features_scaled = scaler.transform(features)

        # Reshape Input for LSTM
        input_reshaped = features_scaled.reshape(1, 10, 9)

        # Make Prediction
        prediction = model.predict(input_reshaped)
        return jsonify({"listing_gain": float(prediction[0])})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
