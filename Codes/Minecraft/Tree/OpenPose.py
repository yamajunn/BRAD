import cv2

# 画像の読み込み
image = cv2.imread('./Codes/Minecraft/Tree/image.jpg')
if image is None:
    raise FileNotFoundError("指定した画像ファイルが見つかりません")

# ネットワークの読み込み
net = cv2.dnn.readNetFromTensorflow('pose_model.pb')

# 入力の前処理
blob = cv2.dnn.blobFromImage(image, 1.0, (368, 368), (127.5, 127.5, 127.5), swapRB=True, crop=False)
net.setInput(blob)
output = net.forward()

# 画像サイズの取得
height, width, _ = image.shape

# 各ポイントの描画
for i in range(output.shape[1]):
    # 出力から座標を取得
    x = int(output[0, i, 0, 0] * width)
    y = int(output[0, i, 0, 1] * height)
    
    # 骨格ポイントを描画
    cv2.circle(image, (x, y), 5, (0, 255, 0), -1)

# 結果の表示
cv2.imshow('Skeleton Detection', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
