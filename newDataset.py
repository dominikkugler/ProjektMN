import os
import json
import torch
from PIL import Image
from torchvision import transforms
from torch.utils.data import Dataset

class CustomDataset(Dataset):
    def init(self, images_dir, labels_dir, transform=None):
        self.images_dir = images_dir
        self.labels_dir = labels_dir
        self.transform = transform
        self.images = [file for file in os.listdir(images_dir) if file.endswith('.jpg')]

    def len(self):
        return len(self.images)

    def getitem(self, i):
        img_name = self.images[i]
        img_path = os.path.join(self.images_dir, img_name)
        image = Image.open(img_path).convert('RGB')

        label_name = img_name.replace('.jpg', '.json')
        label_path = os.path.join(self.labels_dir, label_name)

        if os.path.exists(label_path):
            with open(label_path, 'r') as f:
                label_data = json.load(f)
            label = self.process_label(label_data)
        else:
            label = 0

        if self.transform:
            image = self.transform(image)

        return image, label

    def process_label(self, label_data):
        max_objects = 16
        padded_label = torch.zeros((max_objects, 4))

        if label_data:
            for i, label in enumerate(label_data):
                if i >= max_objects:
                    break
                padded_label[i] = torch.tensor(label['wspolrzedne'][:4])

        return padded_label
    
    transform = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])