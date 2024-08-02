import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import pickle
from datetime import datetime

def extract_features(window, frame_indices):
    features = {}
    features['num_key_presses'] = len(window[window['device'] == 'keyboard'])
    features['num_mouse_clicks'] = len(window[window['device'] == 'mouse'])
    features['num_mouse_moves'] = len(window[window['event'] == 'move'])
    features['num_mouse_scrolls'] = len(window[window['event'] == 'scroll'])
    features['avg_frame_index'] = np.mean(frame_indices) if frame_indices else 0
    return features

def create_features(df, frame_timestamps):
    window_size = pd.Timedelta(seconds=5)
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
    scaler = StandardScaler()
    X = scaler.fit_transform(features_df.drop(columns=['start_time']))
    
    return X, features_df

def save_features(features_df, X, filename='./Codes/Minecraft/Tree/Datas/variables.pkl'):
    with open(filename, 'rb') as f:
        variables = pickle.load(f)
    
    variables['features_df'] = features_df
    variables['X'] = X
    
    with open(filename, 'wb') as f:
        pickle.dump(variables, f)

def load_variables(filename='./Codes/Minecraft/Tree/Datas/variables.pkl'):
    with open(filename, 'rb') as f:
        return pickle.load(f)
    
if __name__ == "__main__":
    variables = load_variables('./Codes/Minecraft/Tree/Datas/variables.pkl')
    
    df = variables['df']
    frame_timestamps = variables['frame_timestamps']
    
    X, features_df = create_features(df, frame_timestamps)
    save_features(features_df, X)
    print("Features extracted and saved.")
