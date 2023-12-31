import os
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.utils import to_categorical

# Load and preprocess data
def load_data(csv_file, image_folder, input_shape):
    df = pd.read_csv(csv_file)
    images = []
    labels = []
    bboxes = []

    for idx, row in df.iterrows():
        # Load and preprocess image
        img_path = os.path.join(image_folder, row['filename'])
        img = load_img(img_path, target_size=input_shape)
        img = img_to_array(img)
        img /= 255.0

        # Extract labels and bounding boxes
        label = row['class']
        bbox = [row['xmin'], row['ymin'], row['xmax'], row['ymax']]

        images.append(img)
        labels.append(label)
        bboxes.append(bbox)

    return np.array(images), np.array(labels), np.array(bboxes)

# Custom data generator
def data_generator(images, labels, bboxes, batch_size, num_classes):
    num_samples = len(images)

    while True:
        for offset in range(0, num_samples, batch_size):
            batch_images = images[offset:offset+batch_size]
            batch_labels = labels[offset:offset+batch_size]
            batch_bboxes = bboxes[offset:offset+batch_size]

            yield batch_images, {'class_output': to_categorical(batch_labels, num_classes=num_classes),
                                 'bbox_output': np.array(batch_bboxes)}

# Set file paths and parameters
csv_file = r"C:\Users\bduser\Desktop\KIRAN REDDY\NEA-1\train\_annotations.csv"
image_folder = r'C:\Users\bduser\Desktop\KIRAN REDDY\NEA-1\train'
input_shape = (224, 224, 3)
num_classes = 3  # Adjust as needed

# Load and preprocess data
images, labels, bboxes = load_data(csv_file, image_folder, input_shape[:2])

# Convert labels to numerical values
# Assuming 'class' column contains textual labels
label_to_num = {label: num for num, label in enumerate(np.unique(labels))}
labels = np.array([label_to_num[label] for label in labels])

# Split data
X_train, X_val, y_train, y_val, bbox_train, bbox_val = train_test_split(images, labels, bboxes, test_size=0.2)

# Data generators
batch_size = 32
train_gen = data_generator(X_train, y_train, bbox_train, batch_size, num_classes)
val_gen = data_generator(X_val, y_val, bbox_val, batch_size, num_classes)

# Train the model
history = model.fit(
    train_gen,
    steps_per_epoch=len(X_train) // batch_size,
    validation_data=val_gen,
    validation_steps=len(X_val) // batch_size,
    epochs=100
)

# Save the model
model.save(r'C:\Users\manumaddi\best_model.h5')
