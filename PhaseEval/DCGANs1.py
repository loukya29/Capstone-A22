import os
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
import matplotlib.pyplot as plt

# Define constants
IMG_SIZE = 64  # Image size for the DCGAN (64x64 images)
BATCH_SIZE = 32
EPOCHS = 100
LATENT_DIM = 100

# Load your real banana dataset (Assuming images are 64x64 and stored in banana_dataset/)
def load_data(image_dir):
    data = []
    for img in os.listdir(image_dir):
        img_path = os.path.join(image_dir, img)
        img = tf.keras.preprocessing.image.load_img(img_path, target_size=(IMG_SIZE, IMG_SIZE))
        img_array = tf.keras.preprocessing.image.img_to_array(img) / 255.0  # Normalize to [0, 1]
        data.append(img_array)
    return np.array(data)

# Load your dataset
real_images = load_data('banana_dataset/')
print(real_images.shape)  # Should output something like (num_images, 64, 64, 3)

# DCGAN Generator Model
def build_generator():
    model = tf.keras.Sequential([
        layers.Dense(8 * 8 * 256, use_bias=False, input_dim=LATENT_DIM),
        layers.BatchNormalization(),
        layers.LeakyReLU(),
        layers.Reshape((8, 8, 256)),
        layers.Conv2DTranspose(128, (4, 4), strides=(2, 2), padding='same', use_bias=False),
        layers.BatchNormalization(),
        layers.LeakyReLU(),
        layers.Conv2DTranspose(64, (4, 4), strides=(2, 2), padding='same', use_bias=False),
        layers.BatchNormalization(),
        layers.LeakyReLU(),
        layers.Conv2DTranspose(3, (4, 4), strides=(2, 2), padding='same', activation='tanh')
    ])
    return model

# DCGAN Discriminator Model
def build_discriminator():
    model = tf.keras.Sequential([
        layers.Conv2D(64, (4, 4), strides=(2, 2), padding='same', input_shape=(IMG_SIZE, IMG_SIZE, 3)),
        layers.LeakyReLU(),
        layers.Dropout(0.3),
        layers.Conv2D(128, (4, 4), strides=(2, 2), padding='same'),
        layers.LeakyReLU(),
        layers.Dropout(0.3),
        layers.Flatten(),
        layers.Dense(1, activation='sigmoid')
    ])
    return model

# Compile the models
discriminator = build_discriminator()
discriminator.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0002, beta_1=0.5), loss='binary_crossentropy')

generator = build_generator()

# GAN Model (Stack Generator and Discriminator)
def build_gan(generator, discriminator):
    discriminator.trainable = False
    model = tf.keras.Sequential([generator, discriminator])
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0002, beta_1=0.5), loss='binary_crossentropy')
    return model

gan = build_gan(generator, discriminator)

# Training Loop
def train_gan(generator, discriminator, gan, epochs, batch_size, data):
    half_batch = batch_size // 2

    for epoch in range(epochs):
        # Train Discriminator
        idx = np.random.randint(0, data.shape[0], half_batch)
        real_images_batch = data[idx]
        noise = np.random.normal(0, 1, (half_batch, LATENT_DIM))
        generated_images = generator.predict(noise)

        # Labels for real and fake images
        real_labels = np.ones((half_batch, 1))
        fake_labels = np.zeros((half_batch, 1))

        d_loss_real = discriminator.train_on_batch(real_images_batch, real_labels)
        d_loss_fake = discriminator.train_on_batch(generated_images, fake_labels)
        d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)

        # Train Generator
        noise = np.random.normal(0, 1, (batch_size, LATENT_DIM))
        valid_labels = np.ones((batch_size, 1))
        g_loss = gan.train_on_batch(noise, valid_labels)

        # Print progress
        print(f"{epoch + 1}/{epochs} [D loss: {d_loss[0]}] [G loss: {g_loss}]")

        # Save generated images every 10 epochs
        if (epoch + 1) % 10 == 0:
            plot_generated_images(epoch + 1)

# Function to plot generated images
def plot_generated_images(epoch):
    noise = np.random.normal(0, 1, (16, LATENT_DIM))
    generated_images = generator.predict(noise)
    generated_images = (generated_images + 1) / 2.0  # Rescale images to [0, 1]
    fig, axs = plt.subplots(4, 4, figsize=(4, 4), sharex=True, sharey=True)
    count = 0
    for i in range(4):
        for j in range(4):
            axs[i, j].imshow(generated_images[count])
            axs[i, j].axis('off')
            count += 1
    plt.savefig(f"generated_images/epoch_{epoch}.png")
    plt.close()

# Train the GAN
train_gan(generator, discriminator, gan, EPOCHS, BATCH_SIZE, real_images)


#######GANs optimisation#######

# Hyperparameter tuning: Adjust the learning rate, batch size, latent vector dimension, and model architecture for better results.
# Use Fréchet Inception Distance (FID): FID is commonly used for comparing real and generated images. You can implement it with the tensorflow_fid library.


#pip install tensorflow-fid
from tensorflow_fid import fid_score

def calculate_fid(real_images, generated_images):
    fid = fid_score.calculate_fid_given_paths(
        [real_images, generated_images],
        batch_size=50,
        device='cuda',
        dims=2048
    )
    print(f"FID score: {fid}")

####Integration######
#     Once you have your synthetic banana images, you can use them to augment your dataset for further training. Here's how you might integrate the generated images:

# Augment Dataset with Synthetic Images
    
# Save the synthetic images into your dataset
def save_synthetic_images(epoch, generator):
    noise = np.random.normal(0, 1, (1000, LATENT_DIM))  # Generate 1000 synthetic images
    generated_images = generator.predict(noise)
    for i, img in enumerate(generated_images):
        img = (img * 255).astype(np.uint8)
        img_path = f"augmented_images/synthetic_banana_{epoch}_{i}.png"
        tf.keras.preprocessing.image.save_img(img_path, img)

# Use the synthetic images for CNN retraining
