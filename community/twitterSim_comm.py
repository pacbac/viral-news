# COMMUNITY IMPLEMENTATION. VARIATION OF THE ANT CLUSTERING ALGORITHM
import networkx as nx
import numpy as np
import random as rd
import math
from community import Community
from functools import reduce
import threading

NUM_USERS = 336000000
MAX_TIME = 1000
COMM_MAX = 0.1*NUM_USERS
INFORMED_COMM_RATIO = 0.1 # the ratio of communities that should have at least one informed user

def isFinished(G):
    return reduce(lambda x, y: x+y.informedRatio*y.pop, G.nodes(), 0) >= 0.9*NUM_USERS

"""
Initializes the simulation (a graph of communities)
Return value: The graph of communities after initialization
"""
def initSim():
    global MAX_TIME
    G = nx.DiGraph()
    available_active = NUM_USERS # number of active users not in a community yet
    GRAPH_INFORM = False # False if there exists at least one community with an informed person
    # create sample communities
    for i in range(NUM_USERS):
        # if all users have been put in a community, break from graphinitialization
        if available_active <= 0:
            break
        pop = rd.randint(2, COMM_MAX) if i != NUM_USERS else available_active
        if int(math.log(pop)) > MAX_TIME:
            MAX_TIME = int(math.log(pop))
        available_active -= pop
        # if available_active <= 0 after updating, this community is the last and must have informed people
        # determines whether community has an informed person
        if available_active <= 0 and not GRAPH_INFORM:
            hasInformed = True
        else:
            hasInformed = rd.random() < INFORMED_COMM_RATIO
        if hasInformed:
            GRAPH_INFORM = True
        c = Community(G, i, pop, hasInformed)
        G.add_node(c)

    commList = list(G.nodes())
    for comm in commList:
        for otherComm in commList:
            if comm != otherComm:
                G.add_edge(comm, otherComm, weight=rd.random()) # weight = probability of impulse sent
    return G

"""
Runs the simulation until 90% of users know the information.
Return value: The graph of communities after the simulations have been run.
"""
def runSim():
    time = 0
    G = initSim()
    commList = list(G.nodes())
    for time in range(1, MAX_TIME+1):
        for comm in commList:
            comm.informedRatio = comm.calcPopInform(time)/comm.pop
            if comm.informedRatio > 0:
                for otherComm in commList:
                    # if the community 'comm' randomly chooses to send an impulse to community 'otherComm'
                    if otherComm != comm and rd.random() < Community.getProbImpulse(G, comm, otherComm):
                        comm.updateImpulse(otherComm)
                        Community.updateProbImpulse(G, comm, otherComm)
                    Community.decayProbImpulse(G, comm, otherComm)
        if isFinished(G):
            break
    print("time:", time)
    return G

if __name__ == "__main__":
    for i in range(10):
        threading.Thread(target=runSim).start()
