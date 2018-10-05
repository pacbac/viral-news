import networkx as nx
from random import random

NUM_NODES = 2

G = nx.DiGraph()
# create sample users
for i in range(NUM_NODES):
    G.add_node(i)
# randomly assign followers to users
for i in range(NUM_NODES):
    for j in range(1):
        follower = i + j if i < NUM_NODES else i - NUM_NODES + j
        G.add_edge(i, follower, weight=1)
print(nx.algorithms.cuts.conductance(G, [i for i in range(NUM_NODES)]))
