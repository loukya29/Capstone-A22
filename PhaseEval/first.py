import os
import numpy as np
import cv2
from PIL import Image
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import os
import cv2

def is_blurry(image_path, threshold=100):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    variance = cv2.Laplacian(image, cv2.CV_64F).var()
    return variance < threshold

dataset_path = "dataset/banana_classification"  
subsets = ["train", "test", "valid"]  
categories = ["unripe", "ripe", "overripe", "rotten"]  

for subset in subsets:
    print(f"Processing {subset} dataset...")
    subset_path = os.path.join(dataset_path, subset)
    
    for category in categories:
        category_path = os.path.join(subset_path, category)
        
        if not os.path.exists(category_path):
            print(f"Category folder {category_path} does not exist. Skipping...")
            continue
        
        for img_file in os.listdir(category_path):
            img_path = os.path.join(category_path, img_file)
            
            try:
                if is_blurry(img_path):
                    os.remove(img_path)  # Remove blurry images
                    print(f"Removed blurry image: {img_path}")
            except Exception as e:
                print(f"Error processing {img_path}: {e}")
