from PIL import ImageGrab, Image
import cv2
import numpy as np
import Quartz
import time
import io

# マウスカーソル画像を取得する関数
def get_cursor_image():
    cursor_image = Quartz.CGImageCreateWithImageInRect(
        Quartz.CGDisplayCreateImageForRect(Quartz.kCGDirectDisplayID, Quartz.CGRectMake(0, 0, 32, 32))
    )
    if cursor_image is not None:
        cursor_data = Quartz.CGDataProviderCopyData(Quartz.CGImageGetDataProvider(cursor_image))
        cursor_pil_image = Image.open(io.BytesIO(cursor_data))
        return cursor_pil_image
    return None

# マウスカーソルの位置を取得する関数
def get_mouse_position():
    mouse_location = Quartz.CGEventGetLocation(Quartz.CGEventCreate(None))
    return int(mouse_location.x), int(mouse_location.y)

# 画面キャプチャの設定
fps = 15
output_file = 'output.mp4'

# 画面のサイズを取得
screen_rect = (0, 0, *ImageGrab.grab().size)
width, height = screen_rect[2], screen_rect[3]

# 動画のフォーマット、コーデック、フレームレート、サイズを設定
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

# カーソル画像を取得
cursor_image = get_cursor_image()

def capture_screen():
    while True:
        # 現在のスクリーンの画像を取得
        img = ImageGrab.grab(bbox=screen_rect)
        
        # Pillowの画像をnumpy配列に変換
        img_np = np.array(img)
        
        # Pillowの画像はRGB形式なので、OpenCVのBGR形式に変換
        img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

        # マウスカーソルの位置を取得
        cursor_x, cursor_y = get_mouse_position()
        
        # カーソル画像が取得できている場合
        if cursor_image:
            # カーソル画像をnumpy配列に変換
            cursor_np = np.array(cursor_image)
            
            # カーソルの位置とサイズを計算
            cursor_width, cursor_height = cursor_image.size
            
            # カーソル画像をBGR形式に変換
            cursor_bgr = cv2.cvtColor(cursor_np, cv2.COLOR_RGB2BGR)
            
            # キャプチャ画像にカーソル画像を重ね合わせる
            x1, y1 = cursor_x, cursor_y
            x2, y2 = x1 + cursor_width, y1 + cursor_height
            
            if x1 < width and y1 < height:
                img_bgr[y1:y2, x1:x2] = cv2.addWeighted(img_bgr[y1:y2, x1:x2], 0.5, cursor_bgr, 0.5, 0)
        
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
