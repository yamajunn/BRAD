import csv
import time
import threading
import cv2
import numpy as np
from pynput import keyboard, mouse
from PIL import Image, ImageGrab
import pyautogui

# カーソル画像を指定
cursor_image_path = './Codes/Minecraft/Tree/clipart.png'
cursor_img = Image.open(cursor_image_path).convert("RGBA")

# CSVファイルを開き、ライターを作成
csv_file = open('./Codes/Minecraft/Tree/Datas/Input/input_log.csv', mode='w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['timestamp', 'device', 'event', 'detail'])
print("CSV file opened and header written")

pressed_keys = set()
pressed_buttons = set()
running = True  # 実行中のフラグ

# コールバック関数
def on_key_press(key):
    global running
    if key == keyboard.KeyCode.from_char('q'):
        running = False
        return False
    if key not in pressed_keys:
        pressed_keys.add(key)
        timestamp = time.time()
        try:
            csv_writer.writerow([timestamp, 'keyboard', 'press', key.char])
        except AttributeError:
            csv_writer.writerow([timestamp, 'keyboard', 'press', str(key)])
        csv_file.flush()
        print(f"\rKey pressed: {key}",end="")

def on_key_release(key):
    if key in pressed_keys:
        pressed_keys.remove(key)
        timestamp = time.time()
        try:
            csv_writer.writerow([timestamp, 'keyboard', 'release', key.char])
        except AttributeError:
            csv_writer.writerow([timestamp, 'keyboard', 'release', str(key)])
        csv_file.flush()
        print(f"\rKey released: {key}",end="")

def on_click(x, y, button, pressed):
    if not running:
        return
    timestamp = time.time()
    if pressed:
        pressed_buttons.add(button)
        csv_writer.writerow([timestamp, 'mouse', 'press', f'{button} at ({x}, {y})'])
        print(f"\rMouse button pressed: {button} at ({x}, {y})",end="")
    else:
        if button in pressed_buttons:
            pressed_buttons.remove(button)
        csv_writer.writerow([timestamp, 'mouse', 'release', f'{button} at ({x}, {y})'])
        print(f"\rMouse button released: {button} at ({x}, {y})",end="")
    csv_file.flush()

def on_move(x, y):
    if not running:
        return
    timestamp = time.time()
    csv_writer.writerow([timestamp, 'mouse', 'move', f'({x}, {y})'])
    csv_file.flush()
    print(f"\rMouse moved to ({x}, {y})",end="")

def on_scroll(x, y, dx, dy):
    if not running:
        return
    timestamp = time.time()
    csv_writer.writerow([timestamp, 'mouse', 'scroll', f'({x}, {y}) {dx} {dy}'])
    csv_file.flush()
    print(f"\rMouse scrolled at ({x}, {y}) with delta ({dx}, {dy})",end="")

# スクリーンショットを動画形式で保存する関数
def capture_video():
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    final_video_path = './Codes/Minecraft/Tree/Datas/Video/output.mp4'

    frames = []
    start_time = time.time()

    while running:
        current_time = time.time()
        elapsed_time = current_time - start_time

        # 30FPSのフレームごとの目標時間
        target_time = 1 / 30

        if elapsed_time > len(frames) * target_time:
            img = ImageGrab.grab()
            img_np = np.array(img)
            img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

            cursor_x, cursor_y = pyautogui.position()
            cursor_resized = cursor_img.resize((10, 15), Image.LANCZOS)
            cursor_img_np = np.array(cursor_resized)

            cursor_x = min(cursor_x, img_bgr.shape[1] - cursor_img_np.shape[1])
            cursor_y = min(cursor_y, img_bgr.shape[0] - cursor_img_np.shape[0])

            for c in range(3):
                img_bgr[cursor_y:cursor_y + cursor_img_np.shape[0], cursor_x:cursor_x + cursor_img_np.shape[1], c] = \
                    cursor_img_np[:, :, c] * (cursor_img_np[:, :, 3] / 255.0) + \
                    img_bgr[cursor_y:cursor_y + cursor_img_np.shape[0], cursor_x:cursor_x + cursor_img_np.shape[1], c] * (1 - cursor_img_np[:, :, 3] / 255.0)

            frames.append(img_bgr)

    actual_duration = time.time() - start_time
    fps = len(frames) / actual_duration
    out_final = cv2.VideoWriter(final_video_path, fourcc, fps, (1920, 1080))

    for frame in frames:
        out_final.write(frame)

    out_final.release()
    print(f"Final video saved with duration: {actual_duration} seconds and FPS: {fps}")

# スクリーンキャプチャを別スレッドで実行
video_thread = threading.Thread(target=capture_video)
video_thread.start()

# リスナーを作成
keyboard_listener = keyboard.Listener(on_press=on_key_press, on_release=on_key_release)
mouse_listener = mouse.Listener(on_click=on_click, on_move=on_move, on_scroll=on_scroll)

# リスナーを開始
keyboard_listener.start()
mouse_listener.start()

keyboard_listener.join()
mouse_listener.stop()
video_thread.join()
csv_file.close()
print("Listeners stopped and CSV file closed")