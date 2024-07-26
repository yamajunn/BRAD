import csv
import time
import threading
import cv2
import numpy as np
from pynput import keyboard, mouse
from PIL import Image, ImageGrab
import pyautogui
import os
import json

cursor_image_path = './Codes/Minecraft/Tree/clipart.png'
cursor_img = Image.open(cursor_image_path).convert("RGBA")

csv_file = open('./Codes/Minecraft/Tree/Datas/Input/input_log.csv', mode='w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['timestamp', 'device', 'event', 'detail'])
print("CSV file opened and header written")

pressed_keys = set()
pressed_buttons = set()
running = threading.Event()
running.set()  # スレッドの実行フラグを立てる
frame_index = 0

start_time = time.time()  # 開始時間の記録

def on_key_press(key):
    if key == keyboard.KeyCode.from_char('q'):
        running.clear()  # スレッドの実行フラグを下げる
        return False
    if key not in pressed_keys:
        pressed_keys.add(key)
        timestamp = time.time()
        try:
            csv_writer.writerow([timestamp, 'keyboard', 'press', key.char])
        except AttributeError:
            csv_writer.writerow([timestamp, 'keyboard', 'press', str(key)])
        csv_file.flush()
        print(f"Key pressed: {key}")

def on_key_release(key):
    if key in pressed_keys:
        pressed_keys.remove(key)
        timestamp = time.time()
        try:
            csv_writer.writerow([timestamp, 'keyboard', 'release', key.char])
        except AttributeError:
            csv_writer.writerow([timestamp, 'keyboard', 'release', str(key)])
        csv_file.flush()
        print(f"Key released: {key}")

def on_click(x, y, button, pressed):
    if not running.is_set():
        return
    timestamp = time.time()
    if pressed:
        pressed_buttons.add(button)
        csv_writer.writerow([timestamp, 'mouse', 'press', f'{button} at ({x}, {y})'])
        print(f"Mouse button pressed: {button} at ({x}, {y})")
    else:
        if button in pressed_buttons:
            pressed_buttons.remove(button)
        csv_writer.writerow([timestamp, 'mouse', 'release', f'{button} at ({x}, {y})'])
        print(f"Mouse button released: {button} at ({x}, {y})")
    csv_file.flush()

def on_move(x, y):
    if not running.is_set():
        return
    timestamp = time.time()
    csv_writer.writerow([timestamp, 'mouse', 'move', f'({x}, {y})'])
    csv_file.flush()
    print(f"Mouse moved to ({x}, {y})")

def on_scroll(x, y, dx, dy):
    if not running.is_set():
        return
    timestamp = time.time()
    csv_writer.writerow([timestamp, 'mouse', 'scroll', f'({x}, {y}) {dx} {dy}'])
    csv_file.flush()
    print(f"Mouse scrolled at ({x}, {y}) with delta ({dx}, {dy})")

def capture_frame(queue):
    global frame_index
    while running.is_set():
        start_time = time.time()
        img = ImageGrab.grab()
        img_np = np.array(img)
        img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        queue.append((time.time(), img_bgr, frame_index))
        frame_index += 1
        elapsed_time = time.time() - start_time
        time.sleep(max(1/60 - elapsed_time, 0))

def process_frame(queue):
    while running.is_set() or queue:
        if queue:
            timestamp, img_bgr, index = queue.pop(0)

            screen_width, screen_height = pyautogui.size()
            cursor_x, cursor_y = pyautogui.position()

            cursor_x = int(cursor_x * img_bgr.shape[1] / screen_width)
            cursor_y = int(cursor_y * img_bgr.shape[0] / screen_height)

            cursor_resized = cursor_img.resize((10, 17), Image.LANCZOS)
            cursor_img_np = np.array(cursor_resized)

            cursor_x = min(cursor_x, img_bgr.shape[1] - cursor_img_np.shape[1])
            cursor_y = min(cursor_y, img_bgr.shape[0] - cursor_img_np.shape[0])

            for c in range(3):
                img_bgr[cursor_y:cursor_y + cursor_img_np.shape[0], cursor_x:cursor_x + cursor_img_np.shape[1], c] = \
                    cursor_img_np[:, :, c] * (cursor_img_np[:, :, 3] / 255.0) + \
                    img_bgr[cursor_y:cursor_y + cursor_img_np.shape[0], cursor_x:cursor_x + cursor_img_np.shape[1], c] * (1 - cursor_img_np[:, :, 3] / 255.0)

            frame_path = f'./Codes/Minecraft/Tree/Datas/Frames/frame_{index:05d}.png'
            cv2.imwrite(frame_path, img_bgr)
            # print(f"Frame {index} saved as {frame_path}")

def save_total_capture_time(start, end):
    total_time = end - start
    time_data = {"total_capture_time": total_time}
    with open('./Codes/Minecraft/Tree/Datas/Input/capture_time.json', 'w') as f:
        json.dump(time_data, f, indent=4)
    print("Total capture time saved to capture_time.json")

def main():
    frame_queue = []
    capture_thread = threading.Thread(target=capture_frame, args=(frame_queue,))
    process_thread = threading.Thread(target=process_frame, args=(frame_queue,))
    capture_thread.start()
    process_thread.start()

    keyboard_listener = keyboard.Listener(on_press=on_key_press, on_release=on_key_release)
    mouse_listener = mouse.Listener(on_click=on_click, on_move=on_move, on_scroll=on_scroll)

    keyboard_listener.start()
    mouse_listener.start()

    try:
        keyboard_listener.join()
    except KeyboardInterrupt:
        running.clear()

    capture_thread.join()
    process_thread.join()
    csv_file.close()
    print("Listeners stopped and CSV file closed")

    end_time = time.time()  # 終了時間の記録
    save_total_capture_time(start_time, end_time)

if __name__ == "__main__":
    main()
