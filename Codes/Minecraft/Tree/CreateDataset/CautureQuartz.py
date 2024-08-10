from PIL import ImageGrab
import cv2
import numpy as np
import time

# 画面キャプチャの設定
fps = 15
output_file = 'output.mp4'

# 画面のサイズを取得
screen_rect = (0, 0, *ImageGrab.grab().size)
width, height = screen_rect[2], screen_rect[3]

# 動画のフォーマット、コーデック、フレームレート、サイズを設定
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

def capture_screen():
    while True:
        # 現在のスクリーンの画像を取得
        img = ImageGrab.grab(bbox=screen_rect)
        
        # Pillowの画像をnumpy配列に変換
        img_np = np.array(img)
        
        # Pillowの画像はRGB形式なので、OpenCVのBGR形式に変換
        img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

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
