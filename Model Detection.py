# Model Detection Code:

import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from IPython.display import display
from PIL import Image

# Load the model
model = load_model(r'C:\Users\manumaddi\best_model.h5')

# Function to preprocess the image
def preprocess_image(img_path, input_shape):
    img = load_img(img_path, target_size=input_shape[:2])
    img = img_to_array(img)
    img /= 255.0
    return np.expand_dims(img, axis=0)  # Expand dims to add batch size of 1

# Function to get class label from prediction
def get_label(prediction, label_to_num):
    class_index = np.argmax(prediction)
    for label, index in label_to_num.items():
        if index == class_index:
            return label

# Load and preprocess a new image
img_path = r"C:\Users\manumaddi\NEA-1\valid\frame_0003_png.rf.23e8a9d180703373c364db92ac8a6420.jpg"
preprocessed_img = preprocess_image(img_path, input_shape)

# Make predictions
predictions = model.predict(preprocessed_img)
class_pred, bbox_pred = predictions

# Assuming bbox_pred is an array with shape (1, 4) containing [xmin, ymin, xmax, ymax]
xmin, ymin, xmax, ymax = bbox_pred[0]

# Scale the bounding box coordinates if necessary
original_img = cv2.imread(img_path)
height, width, _ = original_img.shape

xmin = int(xmin * width)
ymin = int(ymin * height)
xmax = int(xmax * width)
ymax = int(ymax * height)

# Process class prediction
label = get_label(class_pred, label_to_num)

# Print the class label
print("Predicted class label:", label)

# Draw the bounding box and label
cv2.rectangle(original_img, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
cv2.putText(original_img, label, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

# Convert OpenCV image to PIL image for display in Jupyter notebook
original_img_pil = Image.fromarray(cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB))

# Display the image
display(original_img_pil)

