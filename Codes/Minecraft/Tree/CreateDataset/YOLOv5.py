import torch
from pathlib import Path
from PIL import Image
import cv2

model = torch.hub.load('ultralytics/yolov5', 'custom', path='./Weights/Minecraft/Tree/best.pt')

img_path = 'Codes/Minecraft/Tree/Test/TestData/test10.png'
img = Image.open(img_path)

results = model(img)

results.show()