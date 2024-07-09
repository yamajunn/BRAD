import csv
import time
from pynput import keyboard, mouse

# CSVファイルを開き、ライターを作成
with open('./Codes/Minecraft/Tree/TestData/Input/input_log.csv', mode='w', newline='') as csv_file:
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

    # キーボードリスナーを作成
    keyboard_listener = keyboard.Listener(on_press=on_key_press, on_release=on_key_release)
    # マウスリスナーを作成
    mouse_listener = mouse.Listener(on_click=on_click, on_move=on_move)

    # リスナーを開始
    keyboard_listener.start()
    mouse_listener.start()

    # リスナーを停止するまで待機
    keyboard_listener.join()
    mouse_listener.join()
    print("Listeners stopped")
