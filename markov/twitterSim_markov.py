# MONTE CARLO MARKOV CHAIN IMPLEMENTATION
import networkx as nx
import numpy as np
from random import random
import math
from user import User
import threading
from numpy.random import gamma
import time

# initialization constants
NUM_USERS = 20000
AVG_FOLLOWERS = 15
MAX_ROUNDS = 10
INIT_SRC_NUM = 5
# gamma distribution parameters
K = AVG_FOLLOWERS/2
THETA = 2
# spread probability parameters
informProb = 0.5
forwardProb = 0.5
# spread rate parameters
a1 = 0.5
a2 = 0.5

# units: hours
def calcTime(round):
    global a1
    return 8*math.exp(-a1*round)

def calcProbInform(round):
    global informProb, a2
    informProb = 1 - informProb*math.exp(-a2*round)

def calcProbForward(round):
    global informProb, a2
    informProb = 1 - forwardProb*math.exp(-a2*round)

def initSim():
    userList = []
    G = nx.Graph()
    # create sample users
    for i in range(NUM_USERS):
        u = User(G, i)
        userList.append(u)
        G.add_node(u)
    # randomly assign followers to users
    for user in userList:
        for i in range(int(gamma(K, THETA))):
            follower = userList[int(NUM_USERS * random())]
            # weight of edge = probability that follower node sees what node i shares
            G.add_edge(user, follower)
    return G, userList

def runSim():
    start = time.time()
    numHeardNews = 0
    simTime = 0
    G, userList = initSim()
    srcList = []
    newSrcList = []
    newSrcListHeard = []
    for i in range(INIT_SRC_NUM):
        initSource = userList[int(NUM_USERS * random())]
        numHeardNews = initSource.hearNews(numHeardNews)
        numHeardNews += 1
        srcList.append(initSource) # choose the first user to receive news

    for round in range(MAX_ROUNDS):
        neighborList = []
        for src in srcList:
            if random() < forwardProb: # if chooses to forward, forward to all its neighbors
                neighborList.extend(G.neighbors(src))
        for n in neighborList:
            if random() < informProb and not n.heardNews: # if chooses to be informed after it was forwarded to them
                numHeardNews = n.hearNews(numHeardNews)
            elif not n.heardNews: # chose not to hear the news after being forwarded it
                neighborList.remove(n)
        srcList = neighborList # spread outward like waves
        simTime += calcTime(round)
        if numHeardNews >= 0.9*NUM_USERS:
            break
    end = time.time()
    print("Time to reach <= 90%% users:", simTime, "hours.")
    print(numHeardNews, "many people heard the news by round", round)
    print("Elapsed calculation time:", end - start, "seconds.")

if __name__ == "__main__":
    threads = []
    for i in range(2):
        threads.append(threading.Thread(target=runSim))
        threads[i].start()
