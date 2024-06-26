import os
import json
import shutil

def convert_coco_to_yolo(coco_json_path, output_dir):
    if not os.path.exists(coco_json_path):
        print(f"Error: {coco_json_path} does not exist.")
        return

    with open(coco_json_path) as f:
        data = json.load(f)

    images = {image['id']: image for image in data['images']}
    annotations = data['annotations']

    for ann in annotations:
        image_id = ann['image_id']
        image_info = images[image_id]

        img_width = image_info['width']
        img_height = image_info['height']

        bbox = ann['bbox']
        x_min, y_min, width, height = bbox
        x_center = x_min + width / 2
        y_center = y_min + height / 2

        x_center /= img_width
        y_center /= img_height
        width /= img_width
        height /= img_height

        category_id = ann['category_id'] - 1  # YOLOは0ベース

        yolo_annotation = f"{category_id} {x_center} {y_center} {width} {height}\n"

        image_filename = images[image_id]['file_name']
        label_filename = os.path.splitext(image_filename)[0] + ".txt"

        with open(os.path.join(output_dir, label_filename), 'a') as label_file:
            label_file.write(yolo_annotation)

def create_yolo_dataset_structure(base_dir, output_dir):
    for subset in ['train', 'val', 'test']:
        os.makedirs(os.path.join(output_dir, subset, 'images'), exist_ok=True)
        os.makedirs(os.path.join(output_dir, subset, 'labels'), exist_ok=True)

        subset_dir = os.path.join(base_dir, subset)
        json_path = os.path.join(subset_dir, '_annotations.coco.json')

        if not os.path.exists(json_path):
            print(f"Error: {json_path} does not exist.")
            continue

        convert_coco_to_yolo(json_path, os.path.join(output_dir, subset, 'labels'))

        for image_file in os.listdir(subset_dir):
            if image_file.endswith('.jpg'):
                shutil.copy(os.path.join(subset_dir, image_file), os.path.join(output_dir, subset, 'images', image_file))

base_dir = '../../../Datasets/Minecraft/TreeCOCO'
output_dir = '../../../Datasets/Minecraft/TreeYOLO'
create_yolo_dataset_structure(base_dir, output_dir)
