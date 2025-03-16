from flask import Flask, request, jsonify, render_template
import tensorflow as tf
import numpy as np
import cv2
import os
from flask_cors import CORS

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)  # Enable CORS for frontend-backend communication

# Load the trained model
model = tf.keras.models.load_model(r"C:\Users\dell\Desktop\API\breast_cancer-api\breast_cancer_xception.h5")

# Define class labels
class_labels = ["Cancer", "Non-Cancer"]

def preprocess_image(image_path, img_size=(224, 224)):
    """
    Preprocess an image for model prediction.
    - Reads the image in grayscale
    - Converts it to 3-channel (RGB format)
    - Resizes to match model input
    - Normalizes pixel values
    """
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Load grayscale image
    if img is None:
        raise ValueError("Error loading image")

    img = cv2.resize(img, img_size)  # Resize
    img = img / 255.0  # Normalize pixel values
    img = np.stack([img] * 3, axis=-1)  # Convert (224, 224, 1) -> (224, 224, 3)
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    return img

@app.route("/")
def index():
    """Serve the HTML page."""
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    """Handle image upload and return prediction."""
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    file_path = "temp_image.jpg"
    file.save(file_path)

    try:
        img = preprocess_image(file_path)
        prediction = model.predict(img)[0][0]  # Get prediction score

        class_idx = 1 if prediction > 0.5 else 0  # Map to class
        confidence = float(prediction if class_idx == 1 else 1 - prediction)
        result = {"class": class_labels[class_idx], "confidence": confidence}
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        os.remove(file_path)  # Clean up temporary file

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
