import torch
from pathlib import Path
from PIL import Image
from matplotlib import pyplot as plt
import numpy as np

# モデルの読み込み
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# 推論対象の画像
image_path = 'path_to_your_image.jpg'
image = Image.open(image_path)

# 画像をモデルに入力するために変換
img_inference = model.preprocess(image)

# 推論
predictions = model.model(img_inference)[0]

# 予測結果を描画
prediction_img = model.show(image, predictions, save=False, render=True)

# 描画した画像を表示
plt.figure(figsize=(12, 8))
plt.imshow(prediction_img)
plt.axis('off')
plt.show()

# 予測結果を出力
print(predictions)
