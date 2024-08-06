import json

def check_class_count(coco_json_path):
    with open(coco_json_path) as f:
        data = json.load(f)
    
    categories = data['categories']
    class_count = len(categories)
    
    print(f"Total classes in dataset: {class_count}")
    for category in categories:
        print(f"Class ID: {category['id']}, Class Name: {category['name']}")

coco_json_path = './Datasets/Minecraft/TreeCOCO/train/_annotations.coco.json'
check_class_count(coco_json_path)