import Quartz
import cv2
import numpy as np
import time

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
        data = np.frombuffer(image_data, dtype=np.uint8)
        
        # 画像のフォーマットを取得
        bytes_per_row = Quartz.CGImageGetBytesPerRow(image_ref)
        bits_per_component = Quartz.CGImageGetBitsPerComponent(image_ref)
        color_space = Quartz.CGImageGetColorSpace(image_ref)
        channels = 4 if color_space else 3  # 4チャンネル（BGRA）または3チャンネル（BGR）

        # データのサイズと形状を動的に設定
        expected_size = height * bytes_per_row
        if len(data) != expected_size:
            print(f"Warning: Data size mismatch. Expected {expected_size}, but got {len(data)}")
            continue

        img = data.reshape((height, bytes_per_row // channels, channels))

        # BGRAからBGRに変換
        img = img[..., :3]  # RGBAからRGBに変換
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
