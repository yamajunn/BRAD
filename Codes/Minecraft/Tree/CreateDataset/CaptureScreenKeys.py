import time
import json
import math
import os
import csv
from PIL import Image, ImageGrab
from PIL.Image import Resampling
from pynput import mouse, keyboard
from threading import Thread, Lock

# パスの設定
frame_dir = './Codes/Minecraft/Tree/Datas/Frames/'
input_csv = './Codes/Minecraft/Tree/Datas/Input/input_log.csv'
cursor_img_path = './Codes/Minecraft/Tree/CreateDataset/clipart.png'
time_json = './Codes/Minecraft/Tree/Datas/Input/capture_time.json'

# フレーム保存ディレクトリが存在しない場合は作成
os.makedirs(frame_dir, exist_ok=True)

# マウスカーソル画像の読み込みとサイズ変更
cursor_img = Image.open(cursor_img_path)
cursor_img = cursor_img.resize((30 // 8, 40 // 8), Resampling.LANCZOS)

# グローバル変数の設定
key_logs = []
mouse_logs = []
image_list = []
last_mouse_position = (0, 0)
last_time = time.time()
stop_program = False
key_states = {}
last_activity_time = time.time()
image_lock = Lock()

# 角度を10度刻みで記録するための関数
def get_nearest_angle(dx, dy):
    angle = math.degrees(math.atan2(dy, dx)) % 360
    return round(angle / 10) * 10

# マウスカーソルの合成位置を調整する関数
def get_scaled_cursor_position(cursor_pos, orig_size, new_size):
    scale_x = new_size[0] / orig_size[0]
    scale_y = new_size[1] / orig_size[1]
    return (int(cursor_pos[0] * scale_x), int(cursor_pos[1] * scale_y))

# スクリーンキャプチャと画像の保存
def capture_screen():
    global last_time
    while not stop_program:
        current_time = time.time()
        try:
            # スクリーンキャプチャ
            img = ImageGrab.grab()
            orig_size = img.size
            # 画像の解像度を1/8に下げる
            new_size = (int(orig_size[0] // 8), int(orig_size[1] // 8))
            img = img.resize(new_size, Resampling.LANCZOS)
            
            # マウスカーソルの合成位置をスケーリング
            scaled_cursor_position = get_scaled_cursor_position(last_mouse_position, orig_size, new_size)
            
            # カーソル画像を中央に配置
            cursor_position = (scaled_cursor_position[0] - cursor_img.width // 2, scaled_cursor_position[1] - cursor_img.height // 2)
            
            img.paste(cursor_img, cursor_position, cursor_img)
            
            # 画像をリストに追加
            timestamp = int(current_time * 1000)
            with image_lock:
                image_list.append((img, timestamp))
                
            # バッチ保存処理
            if len(image_list) >= 10:  # 10枚キャプチャごとに保存
                with image_lock:
                    for image, ts in image_list:
                        save_image(image, ts)
                    image_list.clear()

        except Exception as e:
            print(f"Error saving screenshot: {e}")

        # キャプチャの間隔を短縮
        time.sleep(0.01)

# スクリーン画像の保存
def save_image(img, timestamp):
    img.save(os.path.join(frame_dir, f'screenshot_{timestamp}.png'))

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

def on_release(key):
    global last_activity_time
    key_str = str(key)
    last_activity_time = time.time()
    if key_str in key_states:
        key_logs.append({'time': time.time(), 'key': key_str, 'action': 'release'})
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
        last_mouse_position = (x, y)
        last_activity_time = time.time()

def on_click(x, y, button, pressed):
    global last_activity_time
    action = 'click_press' if pressed else 'click_release'
    log_entry = {'time': time.time(), 'x': x, 'y': y, 'button': str(button), 'action': action}
    mouse_logs.append(log_entry)
    last_activity_time = time.time()

def on_scroll(x, y, dx, dy):
    global last_activity_time
    log_entry = {'time': time.time(), 'x': x, 'y': y, 'dx': dx, 'dy': dy, 'action': 'scroll'}
    mouse_logs.append(log_entry)
    last_activity_time = time.time()

# 「何もしていない」を記録する関数
def log_no_activity():
    global last_activity_time
    while not stop_program:
        current_time = time.time()
        if current_time - last_activity_time >= 0.1:  # 適用時間を0.1秒に増やす
            log_entry = {'time': current_time, 'action': 'no_activity'}
            mouse_logs.append(log_entry)
            last_activity_time = current_time
        time.sleep(0.1)  # スリープ時間を0.1秒に増やす

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
