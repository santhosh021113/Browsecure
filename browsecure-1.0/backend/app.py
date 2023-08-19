from flask import Flask, request, jsonify
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import requests
import csv

def write_to_csv(report):
    fieldnames = ['Report']
    with open('report.csv', mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow({'Report': report})


app = Flask(__name__)


dataset = pd.read_csv('uci-ml-phishing-dataset.csv')
dataset = dataset.drop('id', axis=1)  

x = dataset.drop('Result', axis=1).values  
y = dataset['Result'].values   

# Train the model
classifier = RandomForestClassifier(n_estimators=100, random_state=0)
classifier.fit(x, y)

def extract_features(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            features = [
                url.count('-'),
                url.count('@'),
                url.count('//'),
                url.count('.'),
                len(url),
                url.startswith('https://'),
                url.startswith('http://'),
                url.count('?'),
                url.count('='),
                url.count('.com'),
                url.count('-'),
                url.count('.'),
                url.count('www.'),
                url.count('https'),
                url.count('http'),
                url.count('//'),
                url.count('.com'),
                url.count('.org'),
                url.count('.net'),
                url.count('.info'),
                url.count('.biz'),
                url.count('.gov'),
                url.count('.edu'),
                url.count('.mil'),
                url.count('.int'),
                url.count('.eu'),
                url.count('.tv'),
                url.count('.us'),
                url.count('.cc'),
                url.count('.name')
            ]
            return features
    except requests.exceptions.RequestException:
        pass
    return None

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        url = data['url']
        features = extract_features(url)
        if features is None:
            prediction = -1  
        else:
            prediction = classifier.predict([features])[0]
        response = {'prediction': int(prediction)}
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)})
    

@app.route('/submit', methods=['POST'])
def submit():
    try:
        report= request.form.get('report')
        write_to_csv(report)
        return 'success'
    except Exception as e:
        return 'error'


if __name__ == '__main__':
    app.run()

