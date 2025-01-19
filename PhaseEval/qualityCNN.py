# 1] MODEL SELECTION

import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.layers import Dense, Flatten, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator


# Load ResNet50 pre-trained on ImageNet
base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Freeze the base model layers
base_model.trainable = False

# Add custom layers for banana quality classification
x = Flatten()(base_model.output)
x = Dense(128, activation='relu')(x)
x = Dropout(0.5)(x)
output = Dense(4, activation='softmax')(x)  # Assuming 4 quality levels

# Define the model
model = Model(inputs=base_model.input, outputs=output)

# 2] MODEL TRAINING 

# Compile the model
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Set up ImageDataGenerator for data augmentation and rescaling
train_datagen = ImageDataGenerator(rescale=1./255)
validation_datagen = ImageDataGenerator(rescale=1./255)

# Create the flow from directory using train and validation data
train_dataset = train_datagen.flow_from_directory(
    'dataset/processed_dataset/train',
    target_size=(224, 224),  # Resizing images to match ResNet50 input
    batch_size=32,
    class_mode='sparse'  # For sparse categorical labels
)

validation_dataset = validation_datagen.flow_from_directory(
    'dataset/processed_dataset/valid',
    target_size=(224, 224),
    batch_size=32,
    class_mode='sparse'  # For sparse categorical labels
)

# Train the model
history = model.fit(
    train_dataset,
    validation_data=validation_dataset,
    epochs=10,
    batch_size=32
)

#Code for Model Evaluation

# Evaluate on the validation dataset
# val_loss, val_accuracy = model.evaluate(validation_dataset)
# print(f"Validation Loss: {val_loss}")
# print(f"Validation Accuracy: {val_accuracy}")

#Evaluate Using a Separate Test Dataset

# Create a test dataset generator
# test_datagen = ImageDataGenerator(rescale=1./255)

# test_dataset = test_datagen.flow_from_directory(
#     'dataset/processed_dataset/test',  # Path to test dataset
#     target_size=(224, 224),
#     batch_size=32,
#     class_mode='sparse'
# )

# # Evaluate on the test dataset
# test_loss, test_accuracy = model.evaluate(test_dataset)
# print(f"Test Loss: {test_loss}")
# print(f"Test Accuracy: {test_accuracy}")




#Visualizing Model Performance (optional)

import matplotlib.pyplot as plt

# # Plot accuracy
# plt.plot(history.history['accuracy'], label='Training Accuracy')
# plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
# plt.title('Model Accuracy')
# plt.xlabel('Epochs')
# plt.ylabel('Accuracy')
# plt.legend()
# plt.show()

# # Plot loss
# plt.plot(history.history['loss'], label='Training Loss')
# plt.plot(history.history['val_loss'], label='Validation Loss')
# plt.title('Model Loss')
# plt.xlabel('Epochs')
# plt.ylabel('Loss')
# plt.legend()
# plt.show()


