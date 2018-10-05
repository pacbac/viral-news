# K MEAN IMPLEMENTATION
import networkx as nx
import numpy as np
from random import random
import math
from user import User
import threading
import matplotlib.pyplot as plt

NUM_USERS = 5000
AVG_FOLLOWERS = 20
MAX_ROUNDS = int(math.log(NUM_USERS))
INIT_SRC_NUM = 5

# units: hours
def calcTime(G, i, userList):
    return 2*MAX_ROUNDS/nx.algorithms.cuts.conductance(G, userList)

def initSim():
    userList = []
    G = nx.DiGraph()
    # create sample users
    for i in range(NUM_USERS):
        u = User(G, i)
        userList.append(u)
        G.add_node(u)
    # randomly assign followers to users
    for user in userList:
        for i in range(AVG_FOLLOWERS):
            follower = userList[int(NUM_USERS * random())]
            # interaction = probability of interaction between the two nodes (the quality of relationship)
            # geoDist = distance between two users, determined by time zone
            interaction, geoDist = random(), random()
            G.add_edge(user, follower, weight=(interaction, geoDist))
    return G, userList

def runSim():
    numHeardNews = 0
    time = 0
    G, userList = initSim()
    srcList = []
    # for i in range(INIT_SRC_NUM):
    #     initSource = userList[int(NUM_USERS * random())]
    #     initSource.hearNews()
    #     numHeardNews = initSource.shareNews()
    #     numHeardNews += 1
    #     srcList.append(initSource) # choose the first user to receive news
    #
    # for round in range(MAX_ROUNDS):
    #     newSrcList = []
    #     for src in srcList:
    #         newSrcList.extend(G.neighbors(src))
    #     for src in newSrcList:
    #         numHeardNews = src.shareNews(numHeardNews)
    #     srcList = newSrcList # spread outward like waves
    #     if numHeardNews >= 0.9*NUM_USERS:
    #         break
    userList.pop()
    print(calcTime(G, NUM_USERS, userList))

if __name__ == "__main__":
    for i in range(2):
        threading.Thread(target=runSim).start()
