import mss
import numpy as np
import cv2
from PIL import Image
import time

# マウスカーソル画像のパス
cursor_image_path = './Codes/Minecraft/Tree/CreateDataset/clipart.png'

# カーソル画像を読み込む
cursor_image = Image.open(cursor_image_path).convert('RGBA')
cursor_np = np.array(cursor_image)
cursor_height, cursor_width = cursor_np.shape[:2]

# 画面キャプチャの設定
fps = 15
output_file = 'output.mp4'
screen_rect = {'top': 0, 'left': 0, 'width': 1440, 'height': 900}  # 画面のサイズに合わせて設定

# 動画のフォーマット、コーデック、フレームレート、サイズを設定
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = cv2.VideoWriter(output_file, fourcc, fps, (screen_rect['width'], screen_rect['height']))

def get_mouse_position():
    # マウスカーソルの位置を取得
    import Quartz
    mouse_location = Quartz.CGEventGetLocation(Quartz.CGEventCreate(None))
    return int(mouse_location.x), int(mouse_location.y)

def capture_screen():
    with mss.mss() as sct:
        while True:
            # 現在のスクリーンの画像を取得（RGBAでキャプチャ）
            img = sct.grab(screen_rect)
            img_np = np.array(img)
            img_np = np.dstack([img_np, np.full((img_np.shape[0], img_np.shape[1]), 255)])  # Add alpha channel

            # マウスカーソルの位置を取得
            cursor_x, cursor_y = get_mouse_position()

            # カーソルの位置とサイズを計算
            x1, y1 = cursor_x - cursor_width // 2, cursor_y - cursor_height // 2
            x2, y2 = x1 + cursor_width, y1 + cursor_height
            
            if x1 < screen_rect['width'] and y1 < screen_rect['height']:
                # スクリーン画像にカーソル画像を重ね合わせる
                for i in range(cursor_height):
                    for j in range(cursor_width):
                        if (0 <= x1 + j < screen_rect['width']) and (0 <= y1 + i < screen_rect['height']):
                            # カーソルのピクセルをスクリーン画像に適用（透明度も考慮）
                            cursor_pixel = cursor_np[i, j]
                            if cursor_pixel[3] > 0:  # alpha value
                                img_np[y1 + i, x1 + j] = cursor_pixel

            # フレームを動画に書き込み
            video_writer.write(img_np)

            # 15 FPSでキャプチャ
            time.sleep(1 / fps)

# キャプチャを開始
try:
    capture_screen()
except KeyboardInterrupt:
    pass
finally:
    video_writer.release()
    print(f"Recording saved to {output_file}")
