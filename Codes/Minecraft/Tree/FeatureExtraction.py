import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import cv2
import numpy as np
from datetime import datetime

# CSVデータの読み込み
df = pd.read_csv('./Codes/Minecraft/Tree/Datas/Input/input_log.csv')

# タイムスタンプを秒に変換
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

# ビデオフレームの読み込みとタイムスタンプの取得
def read_video_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    frames = []
    timestamps = []
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_time = 1 / fps
    
    success, frame = cap.read()
    time_count = 0
    while success:
        frames.append(frame)
        timestamps.append(time_count)
        time_count += frame_time
        success, frame = cap.read()
    
    cap.release()
    return frames, timestamps

video_path = './Codes/Minecraft/Tree/Datas/Video/output.mp4'
frames, frame_timestamps = read_video_frames(video_path)

# ウィンドウサイズ（例: 5秒）
window_size = pd.Timedelta(seconds=5)

# 特徴量の抽出
def extract_features(window, frame_indices):
    features = {}
    features['num_key_presses'] = len(window[window['device'] == 'keyboard'])
    features['num_mouse_clicks'] = len(window[window['device'] == 'mouse'])
    features['num_mouse_moves'] = len(window[window['event'] == 'move'])
    features['num_mouse_scrolls'] = len(window[window['event'] == 'scroll'])
    features['avg_frame_index'] = np.mean(frame_indices) if frame_indices else 0
    return features

# 特徴量データフレームの作成
features_list = []
start_time = df['timestamp'].min()
end_time = df['timestamp'].max()
current_time = start_time

while current_time + window_size <= end_time:
    window = df[(df['timestamp'] >= current_time) & (df['timestamp'] < current_time + window_size)]
    frame_indices = [i for i, ts in enumerate(frame_timestamps) if current_time <= datetime.fromtimestamp(ts) < current_time + window_size]
    if not window.empty:
        features = extract_features(window, frame_indices)
        features['start_time'] = current_time
        features_list.append(features)
    current_time += window_size

features_df = pd.DataFrame(features_list)

# 特徴量の標準化
scaler = StandardScaler()
X = scaler.fit_transform(features_df.drop(columns=['start_time']))
