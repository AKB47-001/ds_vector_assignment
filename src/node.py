# src/node.py
from flask import Flask, request, jsonify
import threading
import requests
import time
import json
import os

app = Flask(__name__)

# Setup
NODE_ID = int(os.environ['NODE_ID'])          # e.g., 0, 1, 2
TOTAL_NODES = int(os.environ['TOTAL_NODES'])  # e.g., 3
PORT = int(os.environ['PORT'])                # e.g., 5000, 5001, 5002

# State
store = {}  # key-value data
vector_clock = [0] * TOTAL_NODES
message_buffer = []
lock = threading.Lock()

# Utility Functions
def increment_clock():
    vector_clock[NODE_ID] += 1

def send_update_to_peers(key, value):
    payload = {
        'key': key,
        'value': value,
        'clock': vector_clock.copy()
    }
    for i in range(TOTAL_NODES):
        if i != NODE_ID:
            try:
                requests.post(f"http://node{i}:{5000+i}/replicate", json=payload)
            except Exception as e:
                print(f"[ERROR] Could not send to node{i}: {e}")

def can_deliver(received_clock):
    for i in range(TOTAL_NODES):
        if i == received_clock['from']:
            if received_clock['clock'][i] != vector_clock[i] + 1:
                return False
        else:
            if received_clock['clock'][i] > vector_clock[i]:
                return False
    return True

def apply_buffered_messages():
    global message_buffer
    to_process = []
    for msg in message_buffer:
        if can_deliver({'clock': msg['clock'], 'from': msg['from']}):
            to_process.append(msg)

    for msg in to_process:
        message_buffer.remove(msg)
        process_replication(msg)

# API Routes
@app.route('/put', methods=['POST'])
def put():
    data = request.json
    key = data['key']
    value = data['value']
    with lock:
        increment_clock()
        store[key] = value
        send_update_to_peers(key, value)
    return jsonify({'status': 'PUT accepted', 'clock': vector_clock})

@app.route('/get/<key>', methods=['GET'])
def get(key):
    with lock:
        value = store.get(key, None)
    return jsonify({'key': key, 'value': value, 'clock': vector_clock})

@app.route('/replicate', methods=['POST'])
def replicate():
    data = request.json
    key = data['key']
    value = data['value']
    clock = data['clock']
    msg = {'key': key, 'value': value, 'clock': clock, 'from': clock.index(max(clock))}
    with lock:
        if can_deliver(msg):
            process_replication(msg)
            apply_buffered_messages()
        else:
            message_buffer.append(msg)
    return jsonify({'status': 'Buffered or applied'})

def process_replication(msg):
    store[msg['key']] = msg['value']
    for i in range(TOTAL_NODES):
        vector_clock[i] = max(vector_clock[i], msg['clock'][i])
    print(f"[Node {NODE_ID}] Applied update {msg}")

# Run
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
