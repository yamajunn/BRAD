import csv
import time
import threading
import queue
from pynput import keyboard, mouse
from PIL import Image, ImageDraw, ImageGrab
import pyautogui

# CSVファイルを開き、ライターを作成
with open('./Codes/Minecraft/Tree/Datas/Input/input_log.csv', mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['timestamp', 'device', 'event', 'detail'])
    print("CSV file opened and header written")

    # 押されているキーとボタンのセット
    pressed_keys = set()
    pressed_buttons = set()

    # キーボードが押されたときのコールバック関数
    def on_key_press(key):
        if key not in pressed_keys:
            pressed_keys.add(key)
            timestamp = time.time()
            try:
                csv_writer.writerow([timestamp, 'keyboard', 'press', key.char])
            except AttributeError:
                csv_writer.writerow([timestamp, 'keyboard', 'press', str(key)])
            csv_file.flush()  # データを即座にファイルに書き込む
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
            csv_file.flush()  # データを即座にファイルに書き込む
            print(f"Key released: {key}")

    # マウスがクリックされたときのコールバック関数
    def on_click(x, y, button, pressed):
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
        csv_file.flush()  # データを即座にファイルに書き込む

    # マウスが移動したときのコールバック関数
    def on_move(x, y):
        timestamp = time.time()
        csv_writer.writerow([timestamp, 'mouse', 'move', f'({x}, {y})'])
        csv_file.flush()  # データを即座にファイルに書き込む
        print(f"Mouse moved to ({x}, {y})")

    # マウスがスクロールされたときのコールバック関数
    def on_scroll(x, y, dx, dy):
        timestamp = time.time()
        csv_writer.writerow([timestamp, 'mouse', 'scroll', f'({x}, {y}) {dx} {dy}'])
        csv_file.flush()  # データを即座にファイルに書き込む
        print(f"Mouse scrolled at ({x}, {y}) with delta ({dx}, {dy})")

    def capture_screenshots(queue):
        cursor_size = (16, 16)  # カーソルのサイズ
        cursor_color = (255, 0, 0)  # カーソルの色（赤色）

        # スクリーンの解像度を取得
        screen_width, screen_height = pyautogui.size()

        while True:
            start_time = time.time()
            
            # 画像をキャプチャ
            img = ImageGrab.grab()
            img_width, img_height = img.size

            # マウスカーソルの位置を取得
            cursor_x, cursor_y = pyautogui.position()
            
            # 座標を変換
            cursor_x = int(cursor_x * (img_width / screen_width))
            cursor_y = int(cursor_y * (img_height / screen_height))

            # カーソルを描画
            draw = ImageDraw.Draw(img)
            cursor_rect = [cursor_x, cursor_y, cursor_x + cursor_size[0], cursor_y + cursor_size[1]]
            draw.rectangle(cursor_rect, outline=cursor_color, width=2)
            
            # 画像をキューに追加
            queue.put((img, start_time))
            
            # 0.1秒から処理時間を引いた残りの時間だけスリープ
            elapsed_time = time.time() - start_time
            time.sleep(max(0, 0.1 - elapsed_time))

    def save_screenshots(queue):
        frame_count = 0
        while True:
            img, timestamp = queue.get()
            img.save(f'./Codes/Minecraft/Tree/Datas/Frames/frame_{frame_count}.jpg', 'JPEG', quality=85)
            frame_count += 1

    screenshot_queue = queue.Queue()

    # スクリーンショットキャプチャを別スレッドで実行
    capture_thread = threading.Thread(target=capture_screenshots, args=(screenshot_queue,))
    save_thread = threading.Thread(target=save_screenshots, args=(screenshot_queue,))
    capture_thread.start()
    save_thread.start()

    # キーボードリスナーを作成
    keyboard_listener = keyboard.Listener(on_press=on_key_press, on_release=on_key_release)
    # マウスリスナーを作成
    mouse_listener = mouse.Listener(on_click=on_click, on_move=on_move, on_scroll=on_scroll)

    # リスナーを開始
    keyboard_listener.start()
    mouse_listener.start()

    # リスナーを停止するまで待機
    keyboard_listener.join()
    mouse_listener.join()
    capture_thread.join()
    save_thread.join()
    print("Listeners stopped")
