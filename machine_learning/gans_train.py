# import torch
# import torch.nn as nn
# from torch.utils.data import Dataset, DataLoader
# from torchvision import transforms
# from PIL import Image
# import os
# from pathlib import Path
# import numpy as np
#
# # Configuration with validation
# class Config:
#     latent_dim = 100
#     img_size = 64
#     time_steps = 7  # Days 0-6
#     num_classes = 4
#     batch_size = 32
#     device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#     valid_extensions = {'.jpg', '.jpeg', '.png', '.webp'}
#
# # Generator (original architecture)
# class BananaAgingGenerator(nn.Module):
#     def _init_(self):
#         super()._init_()
#         self.time_embed = nn.Linear(1, 64)
#         self.init_process = nn.Sequential(
#             nn.Linear(Config.latent_dim + 64, 512),
#             nn.BatchNorm1d(512),
#             nn.LeakyReLU(0.2)
#         )
#         self.conv_blocks = nn.Sequential(
#             nn.ConvTranspose2d(512, 256, 4, 1, 0),
#             nn.BatchNorm2d(256),
#             nn.LeakyReLU(0.2),
#             nn.ConvTranspose2d(256, 128, 4, 2, 1),
#             nn.BatchNorm2d(128),
#             nn.LeakyReLU(0.2),
#             nn.ConvTranspose2d(128, 64, 4, 2, 1),
#             nn.BatchNorm2d(64),
#             nn.LeakyReLU(0.2),
#             nn.ConvTranspose2d(64, 32, 4, 2, 1),
#             nn.BatchNorm2d(32),
#             nn.LeakyReLU(0.2),
#             nn.ConvTranspose2d(32, 3, 4, 2, 1),
#             nn.Tanh()
#         )
#
#     def forward(self, z, time_step):
#         time_emb = self.time_embed(time_step.unsqueeze(1))
#         x = torch.cat([z, time_emb], 1)
#         x = self.init_process(x)
#         x = x.view(-1, 512, 1, 1)
#         return self.conv_blocks(x)
#
# # Discriminator (original architecture)
# class BananaAgingDiscriminator(nn.Module):
#     def _init_(self):
#         super()._init_()
#         self.conv_blocks = nn.Sequential(
#             nn.Conv2d(3, 32, 4, 2, 1),
#             nn.LeakyReLU(0.2),
#             nn.Conv2d(32, 64, 4, 2, 1),
#             nn.BatchNorm2d(64),
#             nn.LeakyReLU(0.2),
#             nn.Conv2d(64, 128, 4, 2, 1),
#             nn.BatchNorm2d(128),
#             nn.LeakyReLU(0.2),
#             nn.Conv2d(128, 256, 4, 2, 1),
#             nn.BatchNorm2d(256),
#             nn.LeakyReLU(0.2)
#         )
#         self.time_embed = nn.Linear(1, 256)
#         self.classifier = nn.Sequential(
#             nn.Linear(256*4*4 + 256, 512),
#             nn.LeakyReLU(0.2),
#             nn.Dropout(0.4),
#             nn.Linear(512, 1),
#             nn.Sigmoid()
#         )
#
#     def forward(self, img, time_step):
#         features = self.conv_blocks(img).view(img.size(0), -1)
#         time_emb = self.time_embed(time_step.unsqueeze(1))
#         combined = torch.cat([features, time_emb], 1)
#         return self.classifier(combined)
#
# # Enhanced Dataset with strict validation
# class BananaDataset(Dataset):
#     def _init_(self, root_dir):
#         self.root_dir = Path(root_dir)
#         self.transform = transforms.Compose([
#             transforms.Resize(Config.img_size),
#             transforms.CenterCrop(Config.img_size),
#             transforms.ToTensor(),
#             transforms.Normalize((0.5,)*3, (0.5,)*3)
#         ])
#
#         self.classes = ['unripe', 'ripe', 'overripe', 'rotten']
#         self.samples = []
#
#         # Validate directory structure
#         self._validate_structure()
#
#         # Load samples with progress tracking
#         total_images = 0
#         for class_idx, class_name in enumerate(self.classes):
#             class_dir = self.root_dir / class_name
#             images = []
#             for ext in Config.valid_extensions:
#                 images.extend(class_dir.glob(f"*{ext}"))
#
#             print(f"Found {len(images)} images in {class_name} directory")
#             for img_path in images:
#                 self.samples.append((img_path, class_idx))
#                 total_images += 1
#
#             if not images:
#                 raise RuntimeError(f"No valid images found in {class_dir}. "
#                                    f"Supported extensions: {Config.valid_extensions}")
#
#         if total_images == 0:
#             raise RuntimeError(f"No images found in any class directory. "
#                                f"Check: 1) Directory structure 2) File extensions 3) File permissions")
#
#         print(f"Successfully loaded {total_images} images from dataset")
#
#     def _validate_structure(self):
#         """Ensure correct directory structure"""
#         missing = []
#         for class_name in self.classes:
#             if not (self.root_dir / class_name).exists():
#                 missing.append(class_name)
#
#         if missing:
#             raise RuntimeError(f"Missing required directories: {missing}\n"
#                                f"Directory structure should be:\n"
#                                f"{self.root_dir}/unripe/\n"
#                                f"{self.root_dir}/ripe/\n"
#                                f"...etc.")
#
#     def _len_(self):
#         return len(self.samples)
#
#     def _getitem_(self, idx):
#         img_path, label = self.samples[idx]
#         try:
#             img = Image.open(img_path).convert('RGB')
#             return self.transform(img), label
#         except Exception as e:
#             print(f"Error loading {img_path}: {str(e)}")
#             # Return random tensor to avoid breaking the batch
#             return torch.randn(3, Config.img_size, Config.img_size), label
#
# # Training function with validation
# def train_banana_gan(data_root, num_epochs=100):
#     try:
#         # Initialize dataset with validation
#         dataset = BananaDataset(data_root)
#         loader = DataLoader(
#             dataset,
#             batch_size=Config.batch_size,
#             shuffle=True,
#             num_workers=2,
#             persistent_workers=True
#         )
#
#         # Initialize models
#         gen = BananaAgingGenerator().to(Config.device)
#         disc = BananaAgingDiscriminator().to(Config.device)
#
#         # Optimizers
#         opt_gen = torch.optim.Adam(gen.parameters(), lr=0.0002, betas=(0.5, 0.999))
#         opt_disc = torch.optim.Adam(disc.parameters(), lr=0.0002, betas=(0.5, 0.999))
#
#         # Training loop
#         for epoch in range(num_epochs):
#             for real_imgs, labels in loader:
#                 real_imgs = real_imgs.to(Config.device)
#                 time_steps = torch.randint(0, 7, (real_imgs.size(0),).float().to(Config.device))
#
#                 # Train Discriminator
#                 opt_disc.zero_grad()
#
#                 # Real images
#                 real_validity = disc(real_imgs, time_steps/7)
#                 d_real_loss = -torch.mean(torch.log(real_validity + 1e-8))
#
#                 # Fake images
#                 z = torch.randn(real_imgs.size(0), Config.latent_dim).to(Config.device)
#                 fake_imgs = gen(z, time_steps)
#                 fake_validity = disc(fake_imgs.detach(), time_steps/7)
#                 d_fake_loss = -torch.mean(torch.log(1 - fake_validity + 1e-8))
#
#                 d_loss = (d_real_loss + d_fake_loss) / 2
#                 d_loss.backward()
#                 opt_disc.step()
#
#                 # Train Generator
#                 opt_gen.zero_grad()
#                 fake_validity = disc(fake_imgs, time_steps/7)
#                 g_loss = -torch.mean(torch.log(fake_validity + 1e-8))
#                 g_loss.backward()
#                 opt_gen.step()
#
#             print(f"Epoch {epoch+1}/{num_epochs} | D Loss: {d_loss.item():.4f} | G Loss: {g_loss.item():.4f}")
#
#         # Save models
#         os.makedirs("models", exist_ok=True)
#         torch.save(gen.state_dict(), "models/generator.pth")
#         torch.save(disc.state_dict(), "models/discriminator.pth")
#         print("Training completed successfully!")
#
#     except Exception as e:
#         print(f"Error during training: {str(e)}")
#         print("Common fixes:")
#         print("1. Verify dataset directory structure")
#         print("2. Check image file extensions (.jpg, .png, etc.)")
#         print("3. Ensure images are RGB format")
#         print("4. Check file permissions")
#
# # Prediction class (original logic)
# class BananaShelfLifePredictor:
#     def _init_(self, gen_path, disc_path):
#         self.gen = BananaAgingGenerator().to(Config.device)
#         self.disc = BananaAgingDiscriminator().to(Config.device)
#         self.gen.load_state_dict(torch.load(gen_path, map_location=Config.device))
#         self.disc.load_state_dict(torch.load(disc_path, map_location=Config.device))
#
#         self.transform = transforms.Compose([
#             transforms.Resize(Config.img_size),
#             transforms.CenterCrop(Config.img_size),
#             transforms.ToTensor(),
#             transforms.Normalize((0.5,)*3, (0.5,)*3)
#         ])
#
#     def predict(self, image_path, threshold=0.6):
#         try:
#             img = Image.open(image_path).convert('RGB')
#             img_tensor = self.transform(img).unsqueeze(0).to(Config.device)
#
#             shelf_life = 0
#             z = torch.randn(1, Config.latent_dim).to(Config.device)
#
#             with torch.no_grad():
#                 for day in range(Config.time_steps):
#                     time_step = torch.tensor([day/Config.time_steps]).to(Config.device)
#                     aged_img = self.gen(z, time_step)
#                     validity = self.disc(aged_img, time_step)
#
#                     if validity.item() < threshold:
#                         break
#                     shelf_life += 1
#
#             return shelf_life
#
#         except Exception as e:
#             print(f"Prediction error: {str(e)}")
#             return -1
#
# if _name_ == "_main_":
#     # Example usage
#     train_banana_gan("/content/banana_classification/train")
#
#     # Predict
#     predictor = BananaShelfLifePredictor("/content/models/generator.pth", "/content/models/discriminator.pth")
#     result = predictor.predict("/content/ripe.jpg")
#     if result != -1:
#         print(f"Predicted shelf life: {result} days")