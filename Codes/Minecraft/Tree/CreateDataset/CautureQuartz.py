import Quartz.CoreGraphics as CG
import cv2
import numpy as np
import time

# 画面の幅と高さを取得
screen_width = CG.CGDisplayPixelsWide(CG.CGMainDisplayID())
screen_height = CG.CGDisplayPixelsHigh(CG.CGMainDisplayID())

# ビデオライターの初期化
fourcc = cv2.VideoWriter_fourcc(*'XVID')
fps = 30  # フレームレートを設定
output_file = 'screen_capture.avi'
video_writer = cv2.VideoWriter(output_file, fourcc, fps, (screen_width, screen_height))

# キャプチャの開始時間を取得
start_time = time.time()

try:
    while True:
        print("a")
        # スクリーンの全体をキャプチャ
        image = CG.CGWindowListCreateImage(CG.CGRectInfinite, CG.kCGWindowListOptionOnScreenOnly, CG.kCGNullWindowID, CG.kCGWindowImageDefault)
        
        # キャプチャした画像をnumpy配列に変換
        width = CG.CGImageGetWidth(image)
        height = CG.CGImageGetHeight(image)
        data = CG.CGDataProviderCopyData(CG.CGImageGetDataProvider(image))
        image_data = np.frombuffer(data, dtype=np.uint8)
        image_data = image_data.reshape((height, width, 4))

        # BGRAからBGRに変換
        image_data = image_data[:, :, :3]
        
        # OpenCV形式に変換してビデオライターに書き込み
        frame = cv2.cvtColor(image_data, cv2.COLOR_RGBA2BGR)
        video_writer.write(frame)
        
        # キャプチャの間隔を調整
        time.sleep(1 / fps)
        
        # 終了条件（ここでは5秒間キャプチャを行う）
        if time.time() - start_time > 5:
            break

except KeyboardInterrupt:
    pass

finally:
    video_writer.release()
    cv2.destroyAllWindows()

print(f"ビデオファイルが保存されました: {output_file}")
