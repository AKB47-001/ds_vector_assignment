Vector Clocks and Causal Ordering

Objective:
To move beyond simple event ordering by implementing Vector Clocks to capture the causal relationships between events in a distributed system. You will apply this to build a causally consistent, multi-node key-value store.

Technology Constraints:
• Programming Language: The entire application logic for the nodes and client must be written exclusively in Python.
• Containerization: The system must be containerized and orchestrated solely using Docker and Docker Compose.

Tasks:
Your implementation should cover the following tasks:
1. Node Implementation with Vector Clocks: Create a Python script for a node. Each node must maintain its own local key-value data and a Vector Clock.
2. Vector Clock Logic: Implement the rules for incrementing the clock on local events, including the clock in sent messages, and updating the local clock upon receiving a message.
3. Causal Write Propagation: Implement the Causal Delivery Rule. When a node
receives a replicated write message, it must delay processing that write until the causal dependencies are met by checking the message’s vector clock against its own. Messages that cannot be delivered must be buffered.
4. Containerization and Networking: Write a ‘Dockerfile‘ for your node and a ‘docker-compose.yml‘ file to run a 3-node system.
5. Verification and Scenario Testing: Create a client script and a specific test scenario to prove that your system maintains causal consistency, even when messages arrive out of order.

How to Run the Project:
1. Clone the repository.
2. Open a Terminal and run python -m pip install -r requirements.txt
3. Now run the command docker-compose up --build
4. Open a New Terminal and run the client script by using the command python3 src/client.py


