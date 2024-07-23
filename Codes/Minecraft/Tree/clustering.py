from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pickle

def perform_clustering(X, n_clusters):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(X)
    cluster_labels = kmeans.labels_
    return cluster_labels

def save_clusters(features_df, cluster_labels, filename='./Codes/Minecraft/Tree/Datas/variables.pkl'):
    features_df['cluster_label'] = cluster_labels
    with open(filename, 'wb') as f:
        variables = {
            'features_df': features_df,
            'cluster_labels': cluster_labels
        }
        pickle.dump(variables, f)

if __name__ == "__main__":
    with open('./Codes/Minecraft/Tree/Datas/variables.pkl', 'rb') as f:
        variables = pickle.load(f)

    X = variables['X']
    features_df = variables['features_df']

    n_clusters = min(len(X), 3)  # クラスタ数をデータポイント数以下に設定
    if n_clusters < 2:
        n_clusters = 2  # 最低2クラスタとする

    cluster_labels = perform_clustering(X, n_clusters)
    save_clusters(features_df, cluster_labels)

    # クラスタラベルの分布をプロット
    plt.figure(figsize=(10, 6))
    plt.hist(cluster_labels, bins=n_clusters, edgecolor='k')
    plt.title('Cluster Label Distribution')
    plt.xlabel('Cluster Label')
    plt.ylabel('Frequency')
    plt.show()

    print("Clustering completed and saved.")
