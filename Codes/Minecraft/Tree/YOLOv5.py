import torch
from pathlib import Path
from PIL import Image
import cv2

# モデルをロードする
model = torch.hub.load('ultralytics/yolov5', 'custom', path='./Weights/Minecraft/Tree/best.pt')

# 画像をロードする
img_path = 'Codes/Minecraft/Tree/Test/TestData/test10.png'
img = Image.open(img_path)

# 物体検出を行う
results = model(img)

# 結果を表示する
results.show()

# 検出結果の詳細を表示する（オプション）
print(results.pandas().xyxy[0])  # x軸、y軸の座標、信頼度、クラスラベルなどの情報
