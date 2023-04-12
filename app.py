from flask import Flask, render_template, request
from hashlib import sha256
from datetime import datetime
import random

app = Flask(__name__)

# list to store blockchain
blockchain = []

# Patient record class
class PatientRecord:
    def __init__(self, name, uid, age, medical_history):
        self.timestamp = datetime.now()
        self.name = name
        self.age = age
        self.uid = uid
        self.medical_history = medical_history
        self.previous_hash = None
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        hash_data = str(self.timestamp) + self.name + str(self.uid) + str(self.age) + self.medical_history
        return sha256(hash_data.encode()).hexdigest()

    def calculate_previous_hash(self):
        if len(blockchain) > 0:
            previous_record = blockchain[-1]
            return previous_record.hash
        else:
            return None

# to add new record to blockchain
@app.route('/add_record', methods=['POST'])
def add_record():
    name = request.form['name']
    age = request.form['age']
    medical_history = request.form['medical_history']
    uid = request.form['uid']

    # Create a new patient record
    record = PatientRecord(name, uid, age, medical_history)

    # Adding the patient record to the blockchain
    record.previous_hash = record.calculate_previous_hash()
    blockchain.append(record)

    return f'Record added to blockchain successfully. Your User ID - {uid}'

# getting patient record from blockchain
@app.route('/get_record', methods=['GET'])
def get_record():
    uid = request.args.get('uid')
    for block in blockchain:
        if block.uid == uid:
            return render_template('record.html', record=block)
    return 'Record not found.'

# displaying whole blockchain
@app.route('/view_blockchain', methods=['GET'])
def view_blockchain():
    return render_template('blockchain.html', blockchain=blockchain)

@app.route('/get_patient_history', methods=['GET'])
def get_patient_history():
    pass

@app.route('/get_history', methods=['GET'])
def get_history():
    uid = request.args.get('uid')
    history = list()
    for block in blockchain:
        if block.uid == uid:
            history.append(block)
        else:
            return 'Record not found.'
    
    return render_template('patient_records.html', all_records=history)

# returning landing page
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
