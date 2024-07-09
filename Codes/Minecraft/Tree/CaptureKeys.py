import csv
import time
from pynput import keyboard

# CSVファイルを開き、ライターを作成
with open('key_log.csv', mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['timestamp', 'event', 'key'])
    print("CSV file opened and header written")

    # 押されているキーのセット
    pressed_keys = set()

    # キーが押されたときのコールバック関数
    def on_press(key):
        if key not in pressed_keys:
            pressed_keys.add(key)
            timestamp = time.time()
            try:
                csv_writer.writerow([timestamp, 'press', key.char])
            except AttributeError:
                csv_writer.writerow([timestamp, 'press', str(key)])
            csv_file.flush()  # データを即座にファイルに書き込む
            print(f"Key pressed: {key}")

    # キーが離されたときのコールバック関数
    def on_release(key):
        if key in pressed_keys:
            pressed_keys.remove(key)
            timestamp = time.time()
            try:
                csv_writer.writerow([timestamp, 'release', key.char])
            except AttributeError:
                csv_writer.writerow([timestamp, 'release', str(key)])
            csv_file.flush()  # データを即座にファイルに書き込む
            print(f"Key released: {key}")

    # リスナーを作成してキー入力をキャプチャ
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        print("Listener started")
        listener.join()
    print("Listener stopped")
