import csv
import time
import threading
import cv2
import numpy as np
from pynput import keyboard, mouse
from PIL import Image, ImageGrab
import pyautogui
import os

cursor_image_path = './Codes/Minecraft/Tree/clipart.png'
cursor_img = Image.open(cursor_image_path).convert("RGBA")

csv_file = open('./Codes/Minecraft/Tree/Datas/Input/input_log.csv', mode='w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['timestamp', 'device', 'event', 'detail'])
print("CSV file opened and header written")

pressed_keys = set()
pressed_buttons = set()
running = True
frame_index = 0

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
    if not running:
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
    if not running:
        return
    timestamp = time.time()
    csv_writer.writerow([timestamp, 'mouse', 'move', f'({x}, {y})'])
    csv_file.flush()
    print(f"Mouse moved to ({x}, {y})")

def on_scroll(x, y, dx, dy):
    if not running:
        return
    timestamp = time.time()
    csv_writer.writerow([timestamp, 'mouse', 'scroll', f'({x}, {y}) {dx} {dy}'])
    csv_file.flush()
    print(f"Mouse scrolled at ({x}, {y}) with delta ({dx}, {dy})")

def capture_frame(queue):
    global frame_index
    while running:
        start_time = time.time()
        img = ImageGrab.grab()
        img_np = np.array(img)
        img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        queue.append((time.time(), img_bgr, frame_index))
        frame_index += 1
        elapsed_time = time.time() - start_time
        time.sleep(max(1/60 - elapsed_time, 0))

def process_frame(queue):
    while running or queue:
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

def create_video_from_frames():
    frame_folder = './Codes/Minecraft/Tree/Datas/Frames/'
    final_video_path = './Codes/Minecraft/Tree/Datas/Video/output.mp4'
    frame_paths = sorted([os.path.join(frame_folder, f) for f in os.listdir(frame_folder) if f.endswith('.png')])

    if not frame_paths:
        print("No frames found to create video")
        return

    first_frame = cv2.imread(frame_paths[0])
    height, width, layers = first_frame.shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out_final = cv2.VideoWriter(final_video_path, fourcc, 30, (width, height))

    for frame_path in frame_paths:
        frame = cv2.imread(frame_path)
        out_final.write(frame)

    out_final.release()
    print(f"Final video saved as {final_video_path}")

frame_queue = []
capture_thread = threading.Thread(target=capture_frame, args=(frame_queue,))
process_thread = threading.Thread(target=process_frame, args=(frame_queue,))
capture_thread.start()
process_thread.start()

keyboard_listener = keyboard.Listener(on_press=on_key_press, on_release=on_key_release)
mouse_listener = mouse.Listener(on_click=on_click, on_move=on_move, on_scroll=on_scroll)

keyboard_listener.start()
mouse_listener.start()

keyboard_listener.join()
mouse_listener.stop()
capture_thread.join()
process_thread.join()
csv_file.close()
print("Listeners stopped and CSV file closed")

create_video_from_frames()
