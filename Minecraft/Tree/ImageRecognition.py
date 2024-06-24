import os
import cv2
import numpy as np
import xml.etree.ElementTree as ET
import tensorflow as tf
import tensorflow_hub as hub

model = hub.load("https://tfhub.dev/tensorflow/faster_rcnn/inception_resnet_v2_640x640/1")

# XMLファイルからアノテーションを解析する関数
def parse_annotation(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    boxes = []
    for obj in root.findall('object'):
        name = obj.find('name').text
        xmin = int(obj.find('bndbox/xmin').text)
        ymin = int(obj.find('bndbox/ymin').text)
        xmax = int(obj.find('bndbox/xmax').text)
        ymax = int(obj.find('bndbox/ymax').text)
        boxes.append((xmin, ymin, xmax, ymax))

    return boxes

# 画像とアノテーションからデータセットを作成する関数
def create_dataset(image_dir, annotation_dir):
    dataset = []
    for filename in os.listdir(image_dir):
        if filename.endswith('.png') or filename.endswith('.jpg'):
            image_path = os.path.join(image_dir, filename)
            annotation_path = os.path.join(annotation_dir, filename.replace('.png', '.xml').replace('.jpg', '.xml'))
            if os.path.exists(annotation_path):
                image = cv2.imread(image_path)
                boxes = parse_annotation(annotation_path)
                dataset.append({'image': image, 'boxes': boxes})
    return dataset

# データセットのディレクトリ
train_image_dir = './Datasets/Minecraft/Tree/IdentificationDataset/train/'
valid_image_dir = './Datasets/Minecraft/Tree/IdentificationDataset/valid/'
test_image_dir = './Datasets/Minecraft/Tree/IdentificationDataset/test/'
annotation_dir = './Annotations/'

# データセットの作成
train_dataset = create_dataset(train_image_dir, annotation_dir)
valid_dataset = create_dataset(valid_image_dir, annotation_dir)
test_dataset = create_dataset(test_image_dir, annotation_dir)

# 物体検出用の事前訓練済みモデルなどの準備

# 検出された物体の情報（例：bounding boxの座標など）を取得
# ここでは仮に検出された物体の座標を示すリストboxesを想定
boxes = [(100, 100, 200, 200)]  # (xmin, ymin, xmax, ymax)

# 検出された物体の位置に矩形を描画
for data in train_dataset + valid_dataset + test_dataset:
    image = data['image']
    for (xmin, ymin, xmax, ymax) in boxes:
        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

    # 結果を表示
    cv2.imshow('Object Detection', image)
    cv2.waitKey(0)

cv2.destroyAllWindows()

# detect_objects 関数内で画像の形状を修正
def detect_objects(image):
    # 画像をリサイズしてモデルに合わせる
    image_resized = tf.image.resize(image, (640, 640))
    image_resized = tf.cast(image_resized, tf.float32)  # 修正: 画像のデータ型をtf.float32に変換
    # モデルに渡す前に画像の型を変換
    result = model(image_resized)

    # 検出された物体の情報を取得
    boxes = result["detection_boxes"][0].numpy()
    scores = result["detection_scores"][0].numpy()
    classes = result["detection_classes"][0].numpy().astype(int)

    # 画像に物体を描画
    image_np = np.array(image[0])
    for i in range(len(boxes)):
        if scores[i] > 0.5:  # スコアが0.5以上の物体のみを表示
            ymin, xmin, ymax, xmax = boxes[i]
            xmin, xmax, ymin, ymax = int(xmin * 640), int(xmax * 640), int(ymin * 640), int(ymax * 640)
            cv2.rectangle(image_np, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

    return image_np


# 画像を読み込み
image = cv2.imread("./Datasets/Minecraft/Tree/IdentificationDataset/test/2022-06-22_11-25-20_png.rf.d333444b8f317695e98c1eba526316ef.jpg")

# 物体検出を実行
result_image = detect_objects(image)

# 結果を表示
cv2.imshow("Object Detection", result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()