# import tensorflow as tf
# from tensorflow.keras.applications import ResNet50V2
# from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
# from tensorflow.keras.models import Model
# from tensorflow.keras.preprocessing.image import ImageDataGenerator
# from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
# import matplotlib.pyplot as plt
#
# # Enhanced Data Augmentation
# train_datagen = ImageDataGenerator(
#     rescale=1./255,
#     rotation_range=20,
#     width_shift_range=0.2,
#     height_shift_range=0.2,
#     horizontal_flip=True,
#     zoom_range=0.15,
#     shear_range=0.15,
#     fill_mode='nearest'
# )
#
# validation_datagen = ImageDataGenerator(rescale=1./255)
# test_datagen = ImageDataGenerator(rescale=1./255)
#
# # Data Generators
# train_dataset = train_datagen.flow_from_directory(
#     '/content/banana_classification/train',
#     target_size=(224, 224),
#     batch_size=32,
#     class_mode='sparse',
#     shuffle=True
# )
#
# validation_dataset = validation_datagen.flow_from_directory(
#     '/content/banana_classification/valid',
#     target_size=(224, 224),
#     batch_size=32,
#     class_mode='sparse',
#     shuffle=False
# )
#
# test_dataset = test_datagen.flow_from_directory(
#     '/content/banana_classification/test',
#     target_size=(224, 224),
#     batch_size=32,
#     class_mode='sparse',
#     shuffle=False
# )
#
# # Model Architecture
# base_model = ResNet50V2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
#
# # Fine-tuning strategy
# for layer in base_model.layers[:-30]:  # Freeze all except last 30 layers
#     layer.trainable = False
#
# # Model structure
# x = base_model.output
# x = GlobalAveragePooling2D()(x)
# x = Dense(256, activation='relu')(x)
# x = Dropout(0.5)(x)
# x = Dense(128, activation='relu')(x)
# x = Dropout(0.3)(x)
# output = Dense(4, activation='softmax')(x)
#
# model = Model(inputs=base_model.input, outputs=output)
#
# # Optimizer with initial learning rate
# optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
#
# # Compile model
# model.compile(
#     optimizer=optimizer,
#     loss='sparse_categorical_crossentropy',
#     metrics=['accuracy', tf.keras.metrics.SparseTopKCategoricalAccuracy(k=2, name='top_2_accuracy')]
# )
#
# # Callbacks
# callbacks = [
#     EarlyStopping(
#         monitor='val_loss',
#         patience=5,
#         restore_best_weights=True,
#         verbose=1
#     ),
#     ReduceLROnPlateau(
#         monitor='val_loss',
#         factor=0.2,
#         patience=3,
#         min_lr=1e-6,
#         verbose=1
#     ),
#     ModelCheckpoint(
#         'best_banana_model.keras',
#         monitor='val_accuracy',
#         save_best_only=True,
#         mode='max',
#         verbose=1
#     )
# ]
#
# # Training
# history = model.fit(
#     train_dataset,
#     validation_data=validation_dataset,
#     epochs=30,
#     callbacks=callbacks,
#     verbose=1
# )
#
# # Plotting function
# def plot_training_history(history):
#     fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
#
#     # Plot accuracy
#     ax1.plot(history.history['accuracy'], label='Training Accuracy')
#     ax1.plot(history.history['val_accuracy'], label='Validation Accuracy')
#     ax1.set_title('Model Accuracy')
#     ax1.set_xlabel('Epoch')
#     ax1.set_ylabel('Accuracy')
#     ax1.legend()
#
#     # Plot loss
#     ax2.plot(history.history['loss'], label='Training Loss')
#     ax2.plot(history.history['val_loss'], label='Validation Loss')
#     ax2.set_title('Model Loss')
#     ax2.set_xlabel('Epoch')
#     ax2.set_ylabel('Loss')
#     ax2.legend()
#
#     plt.tight_layout()
#     plt.show()
#
# # Plot training history
# plot_training_history(history)
#
# # Final evaluation
# print("\nEvaluating on test dataset...")
# test_loss, test_accuracy, test_top2_accuracy = model.evaluate(test_dataset, verbose=1)
# print(f"\nFinal Test Results:")
# print(f"Loss: {test_loss:.4f}")
# print(f"Accuracy: {test_accuracy:.4f}")
# print(f"Top-2 Accuracy: {test_top2_accuracy:.4f}")
#
# # Save final model
# model.save('banana_classifier_resnet50.h5')
#
# # Print model summary
# print("\nModel Architecture:")
# # model.summary()
#
