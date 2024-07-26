import cv2
import mediapipe as mp

# MediaPipeのポーズ推定の初期化
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils

# ビデオキャプチャの初期化
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 色空間の変換
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # ポーズ推定の実行
    results = pose.process(image_rgb)
    
    # 推定結果の描画
    if results.pose_landmarks:
        mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    
    # 結果の表示
    cv2.imshow('Pose Detection', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
