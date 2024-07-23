from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pickle

def perform_clustering(X, n_clusters=3):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(X)
    cluster_labels = kmeans.labels_
    return cluster_labels

def save_clusters(features_df, cluster_labels, filename='./Codes/Minecraft/Tree/Files/variables.pkl'):
    features_df['cluster_label'] = cluster_labels
    with open(filename, 'wb') as f:
        variables = {
            'features_df': features_df,
            'cluster_labels': cluster_labels
        }
        pickle.dump(variables, f)

if __name__ == "__main__":
    with open('./Codes/Minecraft/Tree/Files/variables.pkl', 'rb') as f:
        variables = pickle.load(f)

    X = variables['X']
    features_df = variables['features_df']

    cluster_labels = perform_clustering(X)
    save_clusters(features_df, cluster_labels)

    # クラスタラベルの分布をプロット
    plt.figure(figsize=(10, 6))
    plt.hist(cluster_labels, bins=3, edgecolor='k')
    plt.title('Cluster Label Distribution')
    plt.xlabel('Cluster Label')
    plt.ylabel('Frequency')
    plt.show()

    print("Clustering completed and saved.")
