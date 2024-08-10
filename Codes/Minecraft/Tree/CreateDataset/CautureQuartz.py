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

        # Quartzの画像データを取得
        image_provider = Quartz.CGImageGetDataProvider(image_ref)
        image_data = Quartz.CGDataProviderCopyData(image_provider)
        
        # データをnumpy配列に変換
        data = np.frombuffer(image_data, dtype=np.uint8)
        
        # 画像のフォーマット情報を取得
        bytes_per_row = Quartz.CGImageGetBytesPerRow(image_ref)
        bits_per_component = Quartz.CGImageGetBitsPerComponent(image_ref)
        bits_per_pixel = Quartz.CGImageGetBitsPerPixel(image_ref)
        channels = bits_per_pixel // bits_per_component
        
        # 画像データのサイズを確認
        expected_size = height * bytes_per_row
        if len(data) != expected_size:
            print(f"Warning: Data size mismatch. Expected {expected_size}, but got {len(data)}")
            continue
        
        # データをリシェイプ
        try:
            img = data.reshape((height, bytes_per_row // channels, channels))
        except ValueError as e:
            print(f"ValueError: {e}")
            continue
        
        # データがBGRAの場合、BGRに変換
        if channels == 4:  # BGRA
            img = img[..., :3]  # BGRAからBGRに変換（最後のチャンネルを除去）
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
