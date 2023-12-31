import tensorflow as tf
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization, Activation, Input
from tensorflow.keras.models import Model


def my_model(input_shape, num_classes):
    inputs = Input(shape=input_shape)

    # Convolutional Base
    x = Conv2D(32, (3, 3), padding='same', activation='relu')(inputs)
    x = MaxPooling2D(pool_size=(2, 2))(x)

    x = Conv2D(64, (3, 3), padding='same', activation='relu')(x)
    x = MaxPooling2D(pool_size=(2, 2))(x)

    x = Conv2D(128, (3, 3), padding='same', activation='relu')(x)
    x = MaxPooling2D(pool_size=(2, 2))(x)

    x = Conv2D(256, (3, 3), padding='same', activation='relu')(x)
    x = MaxPooling2D(pool_size=(2, 2))(x)

    # Flatten the feature maps
    x = Flatten()(x)

    # Detection Layers
    # Class prediction
    class_output = Dense(num_classes, activation='softmax', name='class_output')(x)

    # Bounding box prediction
    bbox_output = Dense(4, activation='sigmoid', name='bbox_output')(x)  # Predicting 4 coordinates

    model = Model(inputs=inputs, outputs=[class_output, bbox_output])

    return model


# Example usage
num_classes = 3  # Adjust as needed
model = my_model((224, 224, 3), num_classes)
model.compile(optimizer='adam',
              loss={'class_output': 'categorical_crossentropy', 'bbox_output': 'mse'},
              metrics=['accuracy'])

# Model summary
model.summary()


