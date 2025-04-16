import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
import os

# Load the saved model
model_path = "blood_group_classifier_MobileNetV2.h5"
model = tf.keras.models.load_model(model_path)

# Define image size
IMG_SIZE = (224, 224)

# Blood group labels (ensure these match your dataset's class indices)
class_indices = {'A+ve': 0, 'A-ve': 1, 'B+ve': 2, 'B-ve': 3,
                  'AB+ve': 4, 'AB-ve': 5, 'O+ve': 6, 'O-ve': 7}
index_to_label = {v: k for k, v in class_indices.items()}

# Function to preprocess and predict the image
def predict_blood_group(img_path):
    # Load and preprocess the image
    img = image.load_img(img_path, target_size=IMG_SIZE)
    img_array = image.img_to_array(img) / 255.0  # Normalize
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension

    # Prediction
    prediction = model.predict(img_array)
    predicted_class = np.argmax(prediction[0])
    confidence = np.max(prediction[0])

    # Display results
    print(f"🩸 Predicted Blood Group: {index_to_label[predicted_class]} (Confidence: {confidence * 100:.2f}%)")

# Example usage
image_path = "path_to_your_image.jpg"  # Replace with your image path
predict_blood_group(image_path)