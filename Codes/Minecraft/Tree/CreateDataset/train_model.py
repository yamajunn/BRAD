from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
import pickle

def train_and_evaluate(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    return model, accuracy, report

def load_variables(filename='./Codes/Minecraft/Tree/Datas/variables.pkl'):
    with open(filename, 'rb') as f:
        return pickle.load(f)
    
if __name__ == "__main__":
    variables = load_variables('./Codes/Minecraft/Tree/Datas/variables.pkl')

    X = variables['X']
    cluster_labels = variables['cluster_labels']

    model, accuracy, report = train_and_evaluate(X, cluster_labels)
    print(f"Accuracy: {accuracy}")
    print(report)

    with open('./Codes/Minecraft/Tree/Datas/model.pkl', 'wb') as f:
        pickle.dump(model, f)

    print("Model trained and saved.")
