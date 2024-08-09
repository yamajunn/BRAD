import time
import json
import math
import os
from PIL import Image, ImageGrab
from pynput import mouse, keyboard
from threading import Thread

# パスの設定
frame_dir = './Codes/Minecraft/Tree/Datas/Frames/'
input_csv = './Codes/Minecraft/Tree/Datas/Input/input_log.csv'
cursor_img_path = './Codes/Minecraft/Tree/CreateDataset/clipart.png'
time_json = './Codes/Minecraft/Tree/Datas/Input/capture_time.json'

# マウスカーソル画像の読み込み
cursor_img = Image.open(cursor_img_path)

# グローバル変数の設定
key_logs = []
mouse_logs = []
last_mouse_position = (0, 0)
last_time = time.time()

# 角度を10度刻みで記録するための関数
def get_nearest_angle(x, y):
    angle = math.degrees(math.atan2(y, x)) % 360
    return round(angle / 10) * 10

# スクリーンキャプチャと画像の保存
def capture_screen():
    global last_time
    while True:
        current_time = time.time()
        if current_time - last_time >= 0.05:
            last_time = current_time
            # スクリーンキャプチャ
            img = ImageGrab.grab()
            # マウスカーソルの合成
            img.paste(cursor_img, (int(last_mouse_position[0]), int(last_mouse_position[1])), cursor_img)
            # 保存
            img.save(os.path.join(frame_dir, f'screenshot_{int(current_time)}.png'))
        time.sleep(0.01)

# キー入力の記録
def on_press(key):
    key_logs.append({'time': time.time(), 'key': str(key), 'action': 'press'})

def on_release(key):
    key_logs.append({'time': time.time(), 'key': str(key), 'action': 'release'})

# マウス操作の記録
def on_move(x, y):
    global last_mouse_position
    dx = x - last_mouse_position[0]
    dy = y - last_mouse_position[1]
    if abs(dx) > 1 or abs(dy) > 1:
        angle = get_nearest_angle(dx, dy)
        mouse_logs.append({'time': time.time(), 'x': x, 'y': y, 'angle': angle})
        last_mouse_position = (x, y)

def on_scroll(x, y, dx, dy):
    pass  # スクロールイベントは無視

# スレッドの作成
screen_thread = Thread(target=capture_screen)
screen_thread.daemon = True
screen_thread.start()

mouse_listener = mouse.Listener(on_move=on_move, on_scroll=on_scroll)
keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)

mouse_listener.start()
keyboard_listener.start()

# プログラムが終了するまで待機
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    mouse_listener.stop()
    keyboard_listener.stop()

# CSVファイルにキー入力のログを書き込む
import csv
with open(input_csv, 'w', newline='') as csvfile:
    fieldnames = ['time', 'key', 'action']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for log in key_logs:
        writer.writerow(log)

# JSONファイルに記録した時間を書き込む
with open(time_json, 'w') as jsonfile:
    json.dump({'start_time': last_time, 'end_time': time.time()}, jsonfile)
