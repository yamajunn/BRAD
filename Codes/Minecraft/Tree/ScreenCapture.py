import torch
import cv2
import pyautogui
from PIL import Image
import numpy as np

# モデルをロードする
model = torch.hub.load('ultralytics/yolov5', 'custom', path='./Weights/Minecraft/Tree/best.pt')

# 確認用ウィンドウの名前
window_name = 'YOLOv5 Detection'
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.resizeWindow(window_name, 320, 240)  # 確認用ウィンドウのサイズを設定

while True:
    # 画面全体をキャプチャ
    screenshot = pyautogui.screenshot()
    
    # PIL画像をNumPy配列に変換
    frame = np.array(screenshot)
    
    # NumPy配列をOpenCVのBGR形式に変換
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    
    # NumPy配列をPIL画像に変換
    img_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    
    # 物体検出を行う
    results = model(img_pil)
    
    # 検出結果を取得し、CPUに転送してからNumPy配列に変換
    detections = results.xyxy[0].cpu().numpy()  # x1, y1, x2, y2, conf, cls
    
    # 検出結果をフレームに描画
    for detection in detections:
        x1, y1, x2, y2, conf, cls = map(int, detection[:6])
        label = f"{results.names[cls]} {conf:.2f}"
        
        # バウンディングボックスを描画
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    
    # 確認用ウィンドウに表示するフレームを作成
    display_frame = frame.copy()
    
    # 結果を確認用ウィンドウに表示
    cv2.imshow(window_name, display_frame)

    # 'q'キーで終了
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ウィンドウを解放
cv2.destroyAllWindows()
