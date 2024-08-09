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

# マウスカーソル画像の読み込みとサイズ変更
cursor_img = Image.open(cursor_img_path)
cursor_img = cursor_img.resize((32, 32), Image.ANTIALIAS)  # 32x32にリサイズ

# グローバル変数の設定
key_logs = []
mouse_logs = []
last_mouse_position = (0, 0)
last_time = time.time()
stop_program = False
key_states = {}
last_activity_time = time.time()

# 角度を10度刻みで記録するための関数
def get_nearest_angle(dx, dy):
    angle = math.degrees(math.atan2(dy, dx)) % 360
    return round(angle / 10) * 10

# スクリーンキャプチャと画像の保存
def capture_screen():
    global last_time
    while not stop_program:
        current_time = time.time()
        if current_time - last_time >= 0.1:  # キャプチャの間隔を0.1秒に変更
            last_time = current_time
            # スクリーンキャプチャ
            img = ImageGrab.grab()
            # 画像の解像度を下げる
            img = img.resize((img.width // 2, img.height // 2), Image.ANTIALIAS)
            # マウスカーソルの合成
            img.paste(cursor_img, (last_mouse_position[0] // 2, last_mouse_position[1] // 2), cursor_img)
            # 保存
            img.save(os.path.join(frame_dir, f'screenshot_{int(current_time * 1000)}.png'))
        time.sleep(0.01)

# キー入力の記録
def on_press(key):
    global stop_program, last_activity_time
    key_str = str(key)
    last_activity_time = time.time()
    if key == keyboard.KeyCode.from_char('q'):
        stop_program = True
        return False  # リスナーを停止する
    if key_str not in key_states:
        key_states[key_str] = 'press'
        key_logs.append({'time': time.time(), 'key': key_str, 'action': 'press'})
        print(f"press: {key_str}")

def on_release(key):
    global last_activity_time
    key_str = str(key)
    last_activity_time = time.time()
    if key_str in key_states:
        key_logs.append({'time': time.time(), 'key': key_str, 'action': 'release'})
        print(f"release: {key_str}")
        del key_states[key_str]

# マウス操作の記録
def on_move(x, y):
    global last_mouse_position, last_activity_time
    dx = x - last_mouse_position[0]
    dy = y - last_mouse_position[1]
    distance = math.sqrt(dx**2 + dy**2)
    if distance >= 1:
        angle = get_nearest_angle(dx, dy)
        log_entry = {'time': time.time(), 'x': x, 'y': y, 'angle': angle, 'action': 'move'}
        mouse_logs.append(log_entry)
        print(log_entry)
        last_mouse_position = (x, y)
        last_activity_time = time.time()

def on_click(x, y, button, pressed):
    global last_activity_time
    action = 'click_press' if pressed else 'click_release'
    log_entry = {'time': time.time(), 'x': x, 'y': y, 'button': str(button), 'action': action}
    mouse_logs.append(log_entry)
    print(log_entry)
    last_activity_time = time.time()

def on_scroll(x, y, dx, dy):
    global last_activity_time
    log_entry = {'time': time.time(), 'x': x, 'y': y, 'dx': dx, 'dy': dy, 'action': 'scroll'}
    mouse_logs.append(log_entry)
    print(log_entry)
    last_activity_time = time.time()

# 「何もしていない」を記録する関数
def log_no_activity():
    global last_activity_time
    while not stop_program:
        current_time = time.time()
        if current_time - last_activity_time >= 0.01:
            log_entry = {'time': current_time, 'action': 'no_activity'}
            mouse_logs.append(log_entry)
            print(log_entry)
            last_activity_time = current_time
        time.sleep(0.01)

# スレッドの作成
screen_thread = Thread(target=capture_screen)
screen_thread.daemon = True
screen_thread.start()

no_activity_thread = Thread(target=log_no_activity)
no_activity_thread.daemon = True
no_activity_thread.start()

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

# CSVファイルにキー入力とマウス操作のログを書き込む
import csv
with open(input_csv, 'w', newline='') as csvfile:
    fieldnames = ['time', 'key', 'action', 'x', 'y', 'angle', 'dx', 'dy', 'button']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for log in key_logs:
        writer.writerow({'time': log['time'], 'key': log['key'], 'action': log['action'], 'x': '', 'y': '', 'angle': '', 'dx': '', 'dy': '', 'button': ''})
    for log in mouse_logs:
        writer.writerow({'time': log['time'], 'key': '', 'action': log['action'], 'x': log.get('x', ''), 'y': log.get('y', ''), 'angle': log.get('angle', ''), 'dx': log.get('dx', ''), 'dy': log.get('dy', ''), 'button': log.get('button', '')})

# JSONファイルに記録した時間を書き込む
with open(time_json, 'w') as jsonfile:
    json.dump({'start_time': last_time, 'end_time': time.time()}, jsonfile)
