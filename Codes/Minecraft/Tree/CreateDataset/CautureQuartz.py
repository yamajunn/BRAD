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

def capture_screen():
    while True:
        # 現在のスクリーンの画像を取得
        image_ref = Quartz.CGDisplayCreateImage(Quartz.CGMainDisplayID())
        
        # Quartzの画像をnumpy配列に変換
        image_data = Quartz.CGDataProviderCopyData(Quartz.CGImageGetDataProvider(image_ref))
        img = np.frombuffer(image_data, dtype=np.uint8).reshape((height, width, 4))
        
        # BGRAからBGRに変換
        img = img[:, :, :3]  # RGBAからRGBに変換
        img = img[..., ::-1]  # RGBからBGRに変換（OpenCVの期待する順序）
        
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
