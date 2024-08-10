import numpy as np
import cv2
from PIL import Image, ImageGrab
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
screen_rect = (0, 0, 1440, 900)  # 画面のサイズに合わせて設定

# 動画のフォーマット、コーデック、フレームレート、サイズを設定
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = cv2.VideoWriter(output_file, fourcc, fps, (screen_rect[2] - screen_rect[0], screen_rect[3] - screen_rect[1]))

def get_mouse_position():
    import Quartz
    mouse_location = Quartz.CGEventGetLocation(Quartz.CGEventCreate(None))
    return int(mouse_location.x), int(mouse_location.y)

def capture_screen():
    while True:
        # 現在のスクリーンの画像を取得
        img = ImageGrab.grab(bbox=screen_rect)
        img_np = np.array(img)
        if img_np.shape[2] == 3:  # RGBの場合、アルファチャネルを追加
            img_np = np.dstack([img_np, np.full((img_np.shape[0], img_np.shape[1]), 255)])

        # PillowのImageに変換
        img_pil = Image.fromarray(img_np, 'RGBA')

        # マウスカーソルの位置を取得
        cursor_x, cursor_y = get_mouse_position()

        # カーソルの位置とサイズを計算
        x1, y1 = cursor_x - cursor_width // 2, cursor_y - cursor_height // 2
        x2, y2 = x1 + cursor_width, y1 + cursor_height

        if x1 < screen_rect[2] and y1 < screen_rect[3]:
            # カーソル画像をスクリーン画像に合成
            cursor_pil = cursor_image
            img_pil.paste(cursor_pil, (x1, y1), cursor_pil)  # 透明度を考慮して合成

        # フレームを動画に書き込み
        video_writer.write(np.array(img_pil))

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
