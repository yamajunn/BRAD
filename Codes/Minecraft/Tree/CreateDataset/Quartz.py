import time
import numpy as np
import cv2
import mss

def capture_screen(output_file="output.mp4", fps=30, duration=10):
    with mss.mss() as sct:
        monitor = sct.monitors[0]
        width = monitor["width"]
        height = monitor["height"]

        # ビデオライターを初期化
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

        start_time = time.time()
        while time.time() - start_time < duration:
            img = sct.grab(monitor)
            img_np = np.array(img)
            frame = cv2.cvtColor(img_np, cv2.COLOR_BGRA2BGR)
            
            # フレームを書き込み
            out.write(frame)
            
            # 'q'キーが押されたらループを終了
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        out.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_screen(output_file="high_fps_capture.mp4", fps=30, duration=10)
