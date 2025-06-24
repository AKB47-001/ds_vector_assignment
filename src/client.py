# src/client.py

import requests
import time

NODES = {
    0: "http://localhost:5000",
    1: "http://localhost:5001",
    2: "http://localhost:5002"
}

def put(node, key, value):
    print(f"[Client] PUT '{key}'='{value}' to Node {node}")
    res = requests.post(f"{NODES[node]}/put", json={"key": key, "value": value})
    print(f"  Response: {res.json()}\n")

def get(node, key):
    print(f"[Client] GET '{key}' from Node {node}")
    res = requests.get(f"{NODES[node]}/get/{key}")
    print(f"  Response: {res.json()}\n")
    return res.json()

def scenario_causal_consistency():
    print("\n--- Scenario: Causal Consistency Test ---\n")

    # Step 1: Write x=apple to node 0
    put(0, "x", "apple")

    time.sleep(1)  # Give time for propagation

    # Step 2: Read x from node 1 (establish causal dependency)
    x_val = get(1, "x")  # Should return 'apple'

    time.sleep(1)

    # Step 3: Write x=banana to node 1 (causally dependent on prior read)
    put(1, "x", "banana")

    time.sleep(1.5)

    # Step 4: Read x from node 2 (should eventually return 'banana' only after 'apple')
    get(2, "x")

if __name__ == "__main__":
    scenario_causal_consistency()
