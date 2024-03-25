from flask import Flask, request, jsonify
import pandas as pd
import json
from flask_cors import CORS  # Import CORS from flask_cors

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def load_age_distribution(year=None):
    if year:
        filename = f"./age_distribution_{year}.csv"
    else:
        filename = "./age_distribution.csv"
    
    df = pd.read_csv(filename)
    
    age_bins = list(range(20, 70, 5)) + [70]
    labels = [f"{i}-{i+4}" if i < 70 else "65+" for i in range(20, 70, 5)]
    
    df['Age_Group'] = pd.cut(df['age'], bins=age_bins, labels=labels, right=False)
    df.drop(columns=['age'], inplace=True)
    
    age_group_counts = df.groupby('Age_Group').sum().reset_index()
    
    data = []
    for _, row in age_group_counts.iterrows():
        age_group_data = {"Age_Group": row['Age_Group']}
        for mattress_type in age_group_counts.columns[1:]:
            age_group_data[mattress_type] = int(row[mattress_type])
        data.append(age_group_data)
    
    return data

@app.route('/age_distribution', methods=['POST'])
def age_distribution_post():
    year = request.json.get('year')
    age_groups = request.json.get('age_groups')
    
    data = load_age_distribution(year)
    
    if age_groups:
        data = [entry for entry in data if entry['Age_Group'] in age_groups]
    
    return jsonify(data)

@app.route('/age_distribution', methods=['GET'])
def age_distribution_get():
    year = request.args.get('year')
    
    data = load_age_distribution(year)
    
    return jsonify(data)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5001)
