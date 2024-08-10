from PIL import ImageGrab, Image
import cv2
import numpy as np
import time
import Quartz

# 画面キャプチャの設定
fps = 15
output_file = 'output.mp4'
cursor_image_path = './Codes/Minecraft/Tree/CreateDataset/clipart.png'  # カーソル画像のパス

# 画面のサイズを取得
screen_rect = (0, 0, *ImageGrab.grab().size)
width, height = screen_rect[2], screen_rect[3]

# 動画のフォーマット、コーデック、フレームレート、サイズを設定
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

def get_cursor_image():
    """カーソルの画像を取得する"""
    cursor_image = Image.open(cursor_image_path).convert('RGBA')
    return np.array(cursor_image)

def get_cursor_position():
    """カーソルの位置を取得する"""
    mouse_location = Quartz.CGEventGetLocation(Quartz.CGEventCreate(None))
    return int(mouse_location.x), int(mouse_location.y)

def capture_screen():
    cursor_image_np = get_cursor_image()
    cursor_height, cursor_width = cursor_image_np.shape[:2]
    
    while True:
        # 現在のスクリーンの画像を取得
        img = ImageGrab.grab(bbox=screen_rect)
        img_np = np.array(img)
        
        # Pillowの画像はRGB形式なので、OpenCVのBGR形式に変換
        img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

        # マウスカーソルの位置を取得
        cursor_x, cursor_y = get_cursor_position()

        # カーソルの位置とサイズを計算
        x1, y1 = cursor_x - cursor_width // 2, cursor_y - cursor_height // 2
        x2, y2 = x1 + cursor_width, y1 + cursor_height

        # スクリーン画像にカーソルを追加
        if 0 <= x1 < width and 0 <= y1 < height:
            # カーソル画像をBGR形式に変換
            cursor_bgr = cv2.cvtColor(cursor_image_np, cv2.COLOR_RGBA2BGR)
            # カーソル画像をスクリーン画像に合成
            cursor_x1, cursor_y1 = max(0, x1), max(0, y1)
            cursor_x2, cursor_y2 = min(width, x2), min(height, y2)
            img_bgr[cursor_y1:cursor_y2, cursor_x1:cursor_x2] = cursor_bgr[
                0:(cursor_y2 - cursor_y1),
                0:(cursor_x2 - cursor_x1)
            ]

        # フレームを動画に書き込み
        video_writer.write(img_bgr)

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
