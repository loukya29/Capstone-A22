import os
import cv2
import numpy as np

def resize_and_normalize(image_path, target_size=(224, 224)):
    """
    Resize the image to the target size and normalize pixel values to [0, 1].
    
    Parameters:
        image_path (str): Path to the input image.
        target_size (tuple): Desired size of the output image (width, height).
        
    Returns:
        numpy.ndarray: The resized and normalized image.
    """
    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Image not found: {image_path}")
    
    # Resize the image
    resized_image = cv2.resize(image, target_size, interpolation=cv2.INTER_AREA)
    
    # Normalize pixel values to [0, 1]
    normalized_image = resized_image / 255.0
    
    return normalized_image

def process_images(input_dir, output_dir, target_size=(224, 224)):
    """
    Process all images in the input directory: resize and normalize, then save.
    
    Parameters:
        input_dir (str): Directory containing input images.
        output_dir (str): Directory to save processed images.
        target_size (tuple): Desired size of the output images (width, height).
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for root, _, files in os.walk(input_dir):
        for file in files:
            img_path = os.path.join(root, file)
            
            # Process each image
            try:
                normalized_image = resize_and_normalize(img_path, target_size)
                
                # Save the processed image
                output_path = os.path.join(output_dir, os.path.relpath(img_path, input_dir))
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                # Convert normalized image back to 8-bit (0-255) for saving
                cv2.imwrite(output_path, (normalized_image * 255).astype(np.uint8))
                print(f"Processed and saved: {output_path}")
            except Exception as e:
                print(f"Error processing {img_path}: {e}")

# Directories and configuration
input_directory = "dataset/banana_classification"
output_directory = "dataset/processed_dataset"
target_image_size = (224, 224)  # Resize images to 224x224 pixels

# Process the images
process_images(input_directory, output_directory, target_image_size)
