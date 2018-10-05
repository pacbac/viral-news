# MONTE CARLO MARKOV CHAIN IMPLEMENTATION
import networkx as nx
import numpy as np
from random import random
import math
from user import User
import threading

NUM_USERS = 20000
AVG_FOLLOWERS = 15
MAX_ROUNDS = 10
INIT_SRC_NUM = 5

# units: hours
def calcTime(round):
    return 8*math.exp(-0.8*round)

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
        for i in range(AVG_FOLLOWERS):
            follower = userList[int(NUM_USERS * random())]
            # weight of edge = probability that follower node sees what node i shares
            G.add_edge(user, follower, weight=user.probShare*follower.avgActivityLevel)
    return G, userList

def runSim():
    numHeardNews = 0
    time = 0
    G, userList = initSim()
    srcList = []
    for i in range(INIT_SRC_NUM):
        initSource = userList[int(NUM_USERS * random())]
        initSource.hearNews()
        numHeardNews = initSource.shareNews()
        numHeardNews += 1
        srcList.append(initSource) # choose the first user to receive news

    for round in range(MAX_ROUNDS):
        newSrcList = []
        for src in srcList:
            newSrcList.extend(G.neighbors(src))
        for src in newSrcList:
            numHeardNews = src.shareNews(numHeardNews)
        srcList = newSrcList # spread outward like waves
        time += calcTime(round)
        if numHeardNews >= 0.9*NUM_USERS:
            break
    print(time, numHeardNews, round)

if __name__ == "__main__":
    for i in range(2):
        threading.Thread(target=runSim).start()
