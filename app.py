import os
from flask import Flask, request

app = Flask(__name__)

import pandas as pd

@app.route('/')
def hello_world():
    return {
        'status': True,
        'data': pd.read_csv(r'.\inventory.csv').to_dict('records')
        }, 200

# -------------------------------- USER API ------------------------------------- #

@app.route('/inventory', methods=['POST'])
def get_project_details():
    user_payload = request.get_json(force=True)
    old_data = pd.read_csv(r'.\inventory.csv').to_dict('records')
    old_data.append(user_payload)
    df = pd.DataFrame(old_data)
    df.to_csv('inventory.csv')
    return {
            'status': 'success',
            'data': df.to_dict('records')
        }, 201

@app.route('/inventory/delete', methods=['POST'])
def delete_row():
    user_payload = request.get_json(force=True)
    row_id = user_payload.get('id')
    
    old_data = pd.read_csv(r'.\inventory.csv')
    old_data = old_data[old_data['id'] != row_id]
    old_data.to_csv('inventory.csv')
    return {
            'status': 'success',
            'data': old_data.to_dict('records')
        }, 201

@app.route('/inventory/update', methods=['PUT'])
def update_row():
    user_payload = request.get_json(force=True)
    row_id = user_payload.get('id')
    old_data = pd.read_csv(r'.\inventory.csv').to_dict('records')
    for index in range(0, len(old_data)):
        if old_data[index]['id'] == row_id:
            old_data[index] = user_payload
    old_data= pd.DataFrame(old_data)
    old_data.to_csv('inventory.csv')
    return {
        'status': 'success',
        'data': old_data.to_dict('records')
        }, 201

if __name__ == '__main__':
    app.run(debug=True)