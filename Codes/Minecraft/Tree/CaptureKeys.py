import time
import csv
import pyautogui
from pynput import keyboard
import os

# スクリーンショットを保存するディレクトリを作成
screenshot_dir = 'Codes/Minecraft/Tree/screenshots'
os.makedirs(screenshot_dir, exist_ok=True)

# CSVファイルのヘッダー
csv_header = ['Timestamp', 'Keys', 'Screenshot_Path']

# キーログと画面キャプチャのデータを保存するリスト
log_data = []

# キーボードの入力を収録するクラス
class Keylogger:
    def __init__(self):
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
    
    def start(self):
        self.listener.start()
    
    def stop(self):
        self.listener.stop()
    
    def on_press(self, key):
        # キーが押された時の処理
        try:
            current_keys = [k.char if hasattr(k, 'char') else k for k in log_data[-1][1]]
        except (IndexError, AttributeError):
            current_keys = []
        current_keys.append(key)
        log_data.append([time.time(), current_keys])

    def on_release(self, key):
        # キーが離された時の処理
        pass

# キーロガーのインスタンスを作成して収録を開始する
keylogger = Keylogger()
keylogger.start()

# 0.1秒ごとに画面のスクリーンショットを撮影し、キーログを保存する
try:
    while True:
        # 画面のスクリーンショットを撮影する
        screenshot = pyautogui.screenshot()
        
        # 現在の時間を取得する
        timestamp = time.time()

        # スクリーンショットを保存する例
        screenshot_file = f'{screenshot_dir}/{timestamp}.png'
        screenshot.save(screenshot_file)

        # CSVファイルにキーログを書き込む
        with open('Codes/Minecraft/Tree/keylog.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            for data in log_data:
                writer.writerow([data[0], data[1], f"{timestamp}.png"])  # 時刻、キー、スクリーンショットのファイル名を保存
        log_data = []  # データを保存した後にリセットする

        # 0.1秒待つ
        time.sleep(0.1)

except KeyboardInterrupt:
    # Ctrl+Cで収録を終了する
    keylogger.stop()
    print("Keylogging stopped.")
