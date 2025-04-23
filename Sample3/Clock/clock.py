import time
import random

class Node:
    def __init__(self, node_id, clock_time):
        self.node_id = node_id
        self.clock_time = clock_time  # Local clock time

    def get_time(self):
        return self.clock_time

    def adjust_time(self, offset):
        self.clock_time += offset

class MasterNode:
    def __init__(self, nodes):
        self.nodes = nodes

    def synchronize_clocks(self):
        # Step 1: Collect time from all nodes
        times = [node.get_time() for node in self.nodes]
        avg_time = sum(times) / len(times)

        # Step 2: Compute time offset and update clocks
        for node in self.nodes:
            offset = avg_time - node.get_time()
            node.adjust_time(offset)
            print(f"Node {node.node_id} adjusted by {offset:.2f} seconds.")

        print("\nAfter Synchronization:")
        for node in self.nodes:
            print(f"Node {node.node_id} Clock: {node.get_time():.2f}")

# Simulating 5 nodes with different clock drifts
nodes = [Node(i, random.uniform(10.0, 20.0)) for i in range(5)]
master = MasterNode(nodes)

print("Before Synchronization:")
for node in nodes:
    print(f"Node {node.node_id} Clock: {node.get_time():.2f}")

print("\nSynchronizing Clocks...\n")
master.synchronize_clocks()
