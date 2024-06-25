import torch
from torch.utils.data import DataLoader
from torchvision.datasets import CocoDetection
from torchvision.transforms import ToTensor
from torchvision.models.detection import fasterrcnn_resnet50_fpn
import torchvision.transforms.functional as F

def collate_fn(batch):
    images = [item[0] for item in batch]
    targets = [item[1] for item in batch]
    return images, targets

def main():
    # データセットのパス
    train_path = './Datasets/Minecraft/Tree/train'
    test_path = './Datasets/Minecraft/Tree/test'
    valid_path = './Datasets/Minecraft/Tree/valid'

    # データセットの読み込み
    train_dataset = CocoDetection(root=train_path, annFile=train_path+'/_annotations.coco.json', transform=ToTensor())
    test_dataset = CocoDetection(root=test_path, annFile=test_path+'/_annotations.coco.json', transform=ToTensor())
    valid_dataset = CocoDetection(root=valid_path, annFile=valid_path+'/_annotations.coco.json', transform=ToTensor())

    # DataLoaderの作成
    train_loader = DataLoader(train_dataset, batch_size=2, shuffle=True, num_workers=4, collate_fn=collate_fn)
    test_loader = DataLoader(test_dataset, batch_size=2, shuffle=False, num_workers=4, collate_fn=collate_fn)
    valid_loader = DataLoader(valid_dataset, batch_size=2, shuffle=False, num_workers=4, collate_fn=collate_fn)

    # モデルの定義
    model = fasterrcnn_resnet50_fpn(pretrained=True)

    # デバイスの設定
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    model.to(device)

    # 損失関数と最適化手法の定義
    params = [p for p in model.parameters() if p.requires_grad]
    optimizer = torch.optim.SGD(params, lr=0.005, momentum=0.9, weight_decay=0.0005)
    lr_scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=3, gamma=0.1)

    # 学習
    num_epochs = 10
    for epoch in range(num_epochs):
        model.train()
        for images, targets in train_loader:
            images = list(image.to(device) for image in images)
            
            # ターゲットの形式に合わせて変換
            new_targets = []
            for target_list in targets:
                new_target_list = []
                for target in target_list:
                    new_target = {
                        'boxes': torch.tensor(target['bbox']).unsqueeze(0).to(device),  # bboxをtorch.tensorに変換
                        'labels': torch.tensor([target['category_id']]).unsqueeze(0).to(device),  # category_idをtorch.tensorに変換
                        'image_id': torch.tensor([target['image_id']]).unsqueeze(0).to(device),  # image_idをtorch.tensorに変換
                        'area': torch.tensor([target['area']]).unsqueeze(0).to(device),  # areaをtorch.tensorに変換
                        'iscrowd': torch.tensor([target['iscrowd']]).unsqueeze(0).to(device)  # iscrowdをtorch.tensorに変換
                    }
                    new_target_list.append(new_target)
                new_targets.append(new_target_list)
            
            # forwardとloss計算
            loss_dict = model(images, new_targets)
            losses = sum(loss for loss in loss_dict.values())
            
            # 逆伝搬
            optimizer.zero_grad()
            losses.backward()
            optimizer.step()
        
        # 学習率の更新
        lr_scheduler.step()



    # 学習済みモデルの保存
    torch.save(model.state_dict(), 'path_to_save_model/model.pt')

if __name__ == '__main__':
    main()
