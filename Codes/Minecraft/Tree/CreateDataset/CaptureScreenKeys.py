import time
import os
import csv
import numpy as np
import cv2
from PIL import ImageGrab
from pynput import mouse, keyboard
from threading import Thread
import math

# パスの設定
input_csv_template = './Codes/Minecraft/Tree/Datas/Input/{}.csv'
output_video_template = './Codes/Minecraft/Tree/Datas/Video/{}.mp4'
cursor_img_path = './Codes/Minecraft/Tree/CreateDataset/clipart.png'

# 必要なディレクトリを作成
os.makedirs(os.path.dirname(input_csv_template.format('dummy')), exist_ok=True)
os.makedirs(os.path.dirname(output_video_template.format('dummy')), exist_ok=True)

# マウスカーソル画像の読み込みとサイズ変更
cursor_img = cv2.imread(cursor_img_path, cv2.IMREAD_UNCHANGED)
cursor_img = cv2.resize(cursor_img, (25, 40), interpolation=cv2.INTER_LANCZOS4)

# グローバル変数の設定
key_logs = []
mouse_logs = []
frames = []
last_mouse_position = (0, 0)
stop_program = False
capturing = False
key_states = {}

# 角度を10度刻みで記録するための関数
def get_nearest_angle(dx, dy):
    angle = math.degrees(math.atan2(dy, dx)) % 360
    return round(angle / 10) * 10

# スクリーンキャプチャとフレームの保存
def capture_screen():
    global last_mouse_position
    while not stop_program:
        if capturing:
            try:
                # スクリーンキャプチャ
                img = ImageGrab.grab()
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

                # カーソル画像を合成
                cursor_x, cursor_y = last_mouse_position
                cursor_h, cursor_w = cursor_img.shape[:2]

                x1, y1 = max(cursor_x - cursor_w // 2, 0), max(cursor_y - cursor_h // 2, 0)
                x2, y2 = min(cursor_x + cursor_w // 2, frame.shape[1]), min(cursor_y + cursor_h // 2, frame.shape[0])

                cursor_x1, cursor_y1 = max(0, cursor_w // 2 - cursor_x), max(0, cursor_h // 2 - cursor_y)
                cursor_x2, cursor_y2 = cursor_x1 + (x2 - x1), cursor_y1 + (y2 - y1)

                alpha_s = cursor_img[cursor_y1:cursor_y2, cursor_x1:cursor_x2, 3] / 255.0
                alpha_l = 1.0 - alpha_s

                for c in range(3):
                    frame[y1:y2, x1:x2, c] = (alpha_s * cursor_img[cursor_y1:cursor_y2, cursor_x1:cursor_x2, c] +
                                              alpha_l * frame[y1:y2, x1:x2, c])

                frames.append(frame)
            except Exception as e:
                print(f"Error capturing screenshot: {e}")

        time.sleep(0.01)

# キー入力の記録
def on_press(key):
    global stop_program, capturing
    key_str = str(key)
    if key == keyboard.KeyCode.from_char('q'):
        stop_program = True
        return False
    if key == keyboard.Key.space:
        capturing = not capturing
        if not capturing:
            save_logs()
            save_video()
    elif key_str not in key_states:
        key_states[key_str] = 'press'
        key_logs.append({'time': time.time(), 'key': key_str, 'action': 'press'})

def on_release(key):
    key_str = str(key)
    if key_str in key_states:
        key_logs.append({'time': time.time(), 'key': key_str, 'action': 'release'})
        del key_states[key_str]

# マウス操作の記録
def on_move(x, y):
    global last_mouse_position
    dx = x - last_mouse_position[0]
    dy = y - last_mouse_position[1]
    distance = math.sqrt(dx**2 + dy**2)

    if distance >= 1:  # 1mm移動
        angle = get_nearest_angle(dx, dy)
        mouse_logs.append({'time': time.time(), 'x': x, 'y': y, 'angle': angle, 'action': 'move'})
    
    last_mouse_position = (x, y)

def on_click(x, y, button, pressed):
    action = 'click_press' if pressed else 'click_release'
    mouse_logs.append({'time': time.time(), 'x': x, 'y': y, 'button': str(button), 'action': action})

def on_scroll(x, y, dx, dy):
    mouse_logs.append({'time': time.time(), 'x': x, 'y': y, 'dx': dx, 'dy': dy, 'action': 'scroll'})

# CSVファイルにキー入力とマウス操作のログを書き込む
def save_logs():
    timestamp = int(time.time())
    input_csv = input_csv_template.format(timestamp)
    with open(input_csv, 'w', newline='') as csvfile:
        fieldnames = ['time', 'key', 'action', 'x', 'y', 'angle', 'dx', 'dy', 'button']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for log in key_logs:
            writer.writerow({'time': log['time'], 'key': log['key'], 'action': log['action'],
                             'x': '', 'y': '', 'angle': '', 'dx': '', 'dy': '', 'button': ''})
        for log in mouse_logs:
            writer.writerow({'time': log['time'], 'key': '', 'action': log['action'],
                             'x': log.get('x', ''), 'y': log.get('y', ''), 'angle': log.get('angle', ''),
                             'dx': log.get('dx', ''), 'dy': log.get('dy', ''), 'button': log.get('button', '')})

    # ログをリセット
    key_logs.clear()
    mouse_logs.clear()

# 画像を動画化する関数
def save_video():
    timestamp = int(time.time())
    output_video = output_video_template.format(timestamp)
    if not frames:
        print("No frames to create video.")
        return

    height, width, _ = frames[0].shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # MP4コーデック
    video_writer = cv2.VideoWriter(output_video, fourcc, 30, (width, height))

    for frame in frames:
        video_writer.write(frame)

    video_writer.release()
    print(f"Video saved to {output_video}")

    # フレームをリセット
    frames.clear()

# スレッドの作成
screen_thread = Thread(target=capture_screen)
screen_thread.daemon = True
screen_thread.start()

mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)

mouse_listener.start()
keyboard_listener.start()

# プログラムが終了するまで待機
try:
    while not stop_program:
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    mouse_listener.stop()
    keyboard_listener.stop()
    screen_thread.join()
