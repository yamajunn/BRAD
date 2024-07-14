import csv
import time
import threading
import cv2
import numpy as np
from pynput import keyboard, mouse
from PIL import ImageGrab

# CSVファイルを開き、ライターを作成
with open('./Codes/Minecraft/Tree/Datas/Input/input_log.csv', mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['timestamp', 'device', 'event', 'detail'])
    print("CSV file opened and header written")

    pressed_keys = set()
    pressed_buttons = set()
    running = True  # 実行中のフラグ

    # キーボードが押されたときのコールバック関数
    def on_key_press(key):
        global running
        if key == keyboard.KeyCode.from_char('q'):  # qキーで終了
            running = False
            return False  # リスナーを停止する
        if key not in pressed_keys:
            pressed_keys.add(key)
            timestamp = time.time()
            try:
                csv_writer.writerow([timestamp, 'keyboard', 'press', key.char])
            except AttributeError:
                csv_writer.writerow([timestamp, 'keyboard', 'press', str(key)])
            csv_file.flush()
            print(f"Key pressed: {key}")

    # キーボードが離されたときのコールバック関数
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

    # マウスがクリックされたときのコールバック関数
    def on_click(x, y, button, pressed):
        if not running:
            return  # 実行中でない場合は何もしない
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

    # マウスが移動したときのコールバック関数
    def on_move(x, y):
        if not running:
            return  # 実行中でない場合は何もしない
        timestamp = time.time()
        csv_writer.writerow([timestamp, 'mouse', 'move', f'({x}, {y})'])
        csv_file.flush()
        print(f"Mouse moved to ({x}, {y})")

    # マウスがスクロールされたときのコールバック関数
    def on_scroll(x, y, dx, dy):
        if not running:
            return  # 実行中でない場合は何もしない
        timestamp = time.time()
        csv_writer.writerow([timestamp, 'mouse', 'scroll', f'({x}, {y}) {dx} {dy}'])
        csv_file.flush()
        print(f"Mouse scrolled at ({x}, {y}) with delta ({dx}, {dy})")

    # スクリーンショットを動画形式で保存する関数
    def capture_video():
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # MP4形式
        out = cv2.VideoWriter('./Codes/Minecraft/Tree/Datas/Video/output.mp4', fourcc, 30.0, (1920, 1080))
        while running:
            img = ImageGrab.grab()
            img_np = np.array(img)
            img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
            out.write(img_bgr)
            time.sleep(1 / 30)  # 30fpsでキャプチャ
        out.release()

    # スクリーンキャプチャを別スレッドで実行
    video_thread = threading.Thread(target=capture_video)
    video_thread.start()

    # キーボードリスナーを作成
    keyboard_listener = keyboard.Listener(on_press=on_key_press, on_release=on_key_release)
    # マウスリスナーを作成
    mouse_listener = mouse.Listener(on_click=on_click, on_move=on_move, on_scroll=on_scroll)

    # リスナーを開始
    keyboard_listener.start()
    mouse_listener.start()

    # リスナーを停止するまで待機
    keyboard_listener.join()
    mouse_listener.stop()  # マウスリスナーを停止
    video_thread.join()
    print("Listeners stopped")
