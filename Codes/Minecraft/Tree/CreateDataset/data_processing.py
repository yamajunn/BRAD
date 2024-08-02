import pandas as pd
from datetime import datetime
import pickle

def load_data():
    df = pd.read_csv('./Codes/Minecraft/Tree/Datas/Input/input_log.csv')
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    return df

def read_video_frames(video_path):
    import cv2
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

def save_variables(variables, filename='./Codes/Minecraft/Tree/Datas/variables.pkl'):
    with open(filename, 'wb') as f:
        pickle.dump(variables, f)

def load_variables(filename='./Codes/Minecraft/Tree/Datas/variables.pkl'):
    with open(filename, 'rb') as f:
        return pickle.load(f)

if __name__ == "__main__":
    df = load_data()
    frames, frame_timestamps = read_video_frames('./Codes/Minecraft/Tree/Datas/Video/output.mp4')
    
    variables = {
        'df': df,
        'frames': frames,
        'frame_timestamps': frame_timestamps
    }
    
    save_variables(variables)
    print("Data processed and saved.")
