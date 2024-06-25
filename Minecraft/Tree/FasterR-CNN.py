import os
from PIL import Image
from xml.etree import ElementTree as ET
import torch
from torch.utils.data import DataLoader
from torch.utils.data import Dataset
from torchvision.transforms import ToTensor

class CustomDataset(Dataset):
    def __init__(self, root, transform=None):
        self.root = root
        self.transform = transform
        self.images = []
        self.targets = []

        # trainフォルダ内の画像と対応するXMLファイルを読み込む
        for filename in os.listdir(root):
            if filename.endswith(".jpg"):
                image_path = os.path.join(root, filename)
                xml_path = os.path.join(root, filename.replace(".jpg", ".xml"))
                if os.path.exists(xml_path):
                    self.images.append(image_path)
                    self.targets.append(xml_path)

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        image_path = self.images[idx]
        xml_path = self.targets[idx]

        image = Image.open(image_path).convert("RGB")
        target = self.parse_xml(xml_path)

        if self.transform:
            image = self.transform(image)

        return image, target

    def parse_xml(self, xml_path):
        tree = ET.parse(xml_path)
        root = tree.getroot()
        boxes = []
        for obj in root.findall('object'):
            bbox = obj.find('bndbox')
            xmin = int(bbox.find('xmin').text)
            ymin = int(bbox.find('ymin').text)
            xmax = int(bbox.find('xmax').text)
            ymax = int(bbox.find('ymax').text)
            boxes.append([xmin, ymin, xmax, ymax])
        return torch.tensor(boxes, dtype=torch.float32)

# データセットの準備
train_dataset = CustomDataset(root='./Datasets/Minecraft/Tree/IdentificationDataset/train', transform=ToTensor())
train_loader = DataLoader(train_dataset, batch_size=2, shuffle=True)
