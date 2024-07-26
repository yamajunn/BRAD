import cv2
import mediapipe as mp

# MediaPipeのポーズ推定の初期化
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils

# 画像の読み込み
image_path = './Codes/Minecraft/Tree/image.jpg'
image = cv2.imread(image_path)

# 画像が正常に読み込まれたか確認する
if image is None:
    print(f"指定されたファイル {image_path} が見つかりません。ファイルパスを確認してください。")
    exit()

# 色空間の変換
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# ポーズ推定の実行
results = pose.process(image_rgb)

# 推定結果の描画
if results.pose_landmarks:
    mp_draw.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

# 画像を表示
cv2.imshow('Pose Detection', image)

# ウィンドウが表示されるまで待機する
key = cv2.waitKey(0)
if key == -1:
    print("キー入力がありません。ウィンドウが表示されていない可能性があります。")

# ウィンドウを閉じる
cv2.destroyAllWindows()
