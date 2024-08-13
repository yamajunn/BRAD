import numpy as np
import cv2
import time
import Quartz
import AppKit

# 画面キャプチャの設定
fps = 15
output_file = 'output.mp4'

# 画面のサイズを取得
screen_width = Quartz.CGDisplayPixelsWide(Quartz.kCGDirectMainDisplay)
screen_height = Quartz.CGDisplayPixelsHigh(Quartz.kCGDirectMainDisplay)

# 動画のフォーマット、コーデック、フレームレート、サイズを設定
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = cv2.VideoWriter(output_file, fourcc, fps, (screen_width, screen_height))

def get_cursor_image():
    """カーソルの画像を取得する"""
    cursor = AppKit.NSImage.imageNamed_("cursor.png")
    cursor_size = cursor.size()
    cursor_width = int(cursor_size.width)
    cursor_height = int(cursor_size.height)
    
    cursor_rect = AppKit.NSMakeRect(0, 0, cursor_width, cursor_height)
    cursor_bmp = AppKit.NSBitmapImageRep.alloc().initWithFocusedViewRect_(cursor_rect)
    
    cursor_data = cursor_bmp.representationUsingType_properties_(AppKit.NSBitmapImageFileTypePNG, None)
    cursor_array = np.frombuffer(cursor_data.bytes(), dtype=np.uint8)
    cursor_img = cv2.imdecode(cursor_array, cv2.IMREAD_UNCHANGED)
    
    return cursor_img

def get_cursor_position():
    """カーソルの位置を取得する"""
    mouse_location = Quartz.CGEventGetLocation(Quartz.CGEventCreate(None))
    return int(mouse_location.x), int(mouse_location.y)

def capture_screen():
    cursor_image_np = get_cursor_image()
    cursor_height, cursor_width = cursor_image_np.shape[:2]
    
    while True:
        # 現在のスクリーンの画像を取得
        screenshot = Quartz.CGWindowListCreateImage(Quartz.CGRectInfinite, Quartz.kCGWindowListOptionOnScreenOnly, Quartz.kCGNullWindowID, Quartz.kCGWindowImageDefault)
        img_np = np.frombuffer(Quartz.CGDataProviderCopyData(Quartz.CGImageGetDataProvider(screenshot)), dtype=np.uint8)
        img_np = img_np.reshape((screen_height, screen_width, 4))  # BGRA形式
        
        # BGRAをBGRに変換
        img_bgr = cv2.cvtColor(img_np, cv2.COLOR_BGRA2BGR)

        # マウスカーソルの位置を取得
        cursor_x, cursor_y = get_cursor_position()

        # カーソルの位置とサイズを計算
        x1, y1 = cursor_x - cursor_width // 2, cursor_y - cursor_height // 2
        x2, y2 = x1 + cursor_width, y1 + cursor_height

        # スクリーン画像にカーソルを追加
        if 0 <= x1 < screen_width and 0 <= y1 < screen_height:
            # カーソル画像をスクリーン画像に合成
            alpha_cursor = cursor_image_np[:, :, 3] / 255.0
            for c in range(0, 3):
                img_bgr[y1:y2, x1:x2, c] = alpha_cursor * cursor_image_np[:, :, c] + (1 - alpha_cursor) * img_bgr[y1:y2, x1:x2, c]

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
