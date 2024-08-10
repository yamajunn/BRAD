import Quartz
import cv2
import numpy as np
import time
from PIL import Image

# 画面キャプチャの設定
screen_rect = Quartz.CGDisplayBounds(Quartz.CGMainDisplayID())
width = int(screen_rect.size.width)
height = int(screen_rect.size.height)
fps = 15
output_file = 'output.mp4'

# 動画のフォーマット、コーデック、フレームレート、サイズを設定
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

# 画面キャプチャを行う関数
def capture_screen():
    while True:
        # 現在のスクリーンの画像を取得
        image_ref = Quartz.CGDisplayCreateImage(Quartz.CGMainDisplayID())
        
        # Quartzの画像をPIL Imageに変換
        pil_image = Image.frombytes(
            'RGBA', 
            (Quartz.CGImageGetWidth(image_ref), Quartz.CGImageGetHeight(image_ref)),
            Quartz.CGDataProviderCopyData(Quartz.CGImageGetDataProvider(image_ref))
        )
        
        # PIL Imageをnumpy配列に変換
        img = np.array(pil_image)
        img = img[:, :, :3]  # RGBAからRGBに変換

        # フレームを動画に書き込み
        video_writer.write(img)

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
