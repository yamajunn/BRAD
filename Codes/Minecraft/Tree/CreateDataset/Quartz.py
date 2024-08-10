import time
import numpy as np
import cv2
import mss
from Quartz import CGWindowListCopyWindowInfo, kCGWindowListOptionOnScreenOnly, kCGNullWindowID, kCGWindowImageDefault

# スクリーンキャプチャを行う関数
def capture_screen():
    with mss.mss() as sct:
        # 画面のサイズを取得
        monitor = sct.monitors[0]
        width = monitor["width"]
        height = monitor["height"]

        while True:
            # スクリーンキャプチャ
            img = sct.grab(monitor)
            
            # numpy配列に変換
            img_np = np.array(img)

            # BGRからRGBに変換
            frame = cv2.cvtColor(img_np, cv2.COLOR_BGRA2BGR)
            
            # OpenCVで表示
            cv2.imshow("Screen Capture", frame)
            
            # 'q'キーが押されたらループを終了
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_screen()
