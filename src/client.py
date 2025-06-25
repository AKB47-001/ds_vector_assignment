import requests
import time

nodes = {
    "node1": "http://localhost:7001",
    "node2": "http://localhost:7002",
    "node3": "http://localhost:7003",
}

def put(node, key, value, clock, sender):
    url = f"{nodes[node]}/replicate"
    data = {"key": key, "value": value, "clock": clock, "sender": sender}
    res = requests.post(url, json=data)
    print(f"PUT to {node}: {res.json()}")

def get(node, key):
    url = f"{nodes[node]}/get?key={key}"  
    res = requests.get(url)
    print(f"GET from {node}: {res.json()}")

# SIMULATING THE CASUAL SCENARIO
print("---- Step_1: Node One writes x=A ----")
put("node1", "x", "Alpha", {"node1": 1, "node2": 0, "node3": 0}, "node1")
time.sleep(1)

print("---- Step_2: Node Two reads x ----")
get("node2", "x")
time.sleep(1)

print("---- Step_3: Node Two writes x=B ----")
put("node2", "x", "Beta", {"node1": 1, "node2": 1, "node3": 0}, "node2")
time.sleep(1)

print("---- Step_4: Node Three reads x ----")
get("node3", "x")