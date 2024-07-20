import torch
import cv2
import pyautogui
from PIL import Image
import numpy as np

model = torch.hub.load('ultralytics/yolov5', 'custom', path='./Weights/Minecraft/Tree/yolov5.pt')

window_name = 'YOLOv5 Detection'
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.resizeWindow(window_name, 320, 240)

while True:
    screenshot = pyautogui.screenshot()
    
    frame = np.array(screenshot)
    
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    
    img_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    
    results = model(img_pil)
    
    detections = results.xyxy[0].cpu().numpy()
    
    for detection in detections:
        x1, y1, x2, y2, conf, cls = map(int, detection[:6])
        label = f"{results.names[cls]} {conf:.2f}"
        
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    
    display_frame = frame.copy()
    
    cv2.imshow(window_name, display_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
