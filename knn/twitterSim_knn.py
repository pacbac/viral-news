# K NEAREST NEIGHBORS IMPLEMENTATION
import networkx as nx
import numpy as np
from random import random
import math
from user import User
import threading
from queue import PriorityQueue

NUM_USERS = 5000
AVG_FOLLOWERS = 20
MAX_TIME = 1000
INIT_SRC_NUM = 5
CIRCLE_SIZE = 10
K = 10

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
            # relation = probability of interaction between the two nodes (the quality of relationship)
            # geoDist = distance between two users, determined primarily by time zone
            relation, geoDist = random(), CIRCLE_SIZE*random()
            G.add_edge(user, follower, weight=(relation, geoDist))
            # update radii of their follower circles
            if geoDist > user.radius:
                user.radius = geoDist
            if geoDist > follower.radius:
                follower.radius = geoDist
    return G, userList

def runSim():
    simTime = 0
    G, userList = initSim()
    srcList = []
    toBeHeard = PriorityQueue() # users that will hear about the news in the future
    numHeardNews = 0
    for i in range(INIT_SRC_NUM):
        initSource = userList[int(NUM_USERS * random())] # choose the first user to receive news
        numHeardNews = initSource.hearNews(numHeardNews)
        srcList.append(initSource)

    # unit: a time unit (1 second, 1 minute, etc depending on context)
    for unit in range(MAX_TIME):
        newSrcList = []
        for src in srcList:
            if random() < src.interest: # if the user decides to forward it to his neighbors
                numHeardNews = src.shareNews(numHeardNews, toBeHeard, unit)
        print(len(toBeHeard.queue))
        while not toBeHeard.empty() and toBeHeard.queue[0][0] == unit: # continue popping users from queue while it is their time to be informed
            thisUnit, (parent, follower) = toBeHeard.get()
            if random() < follower.calcProbInform(parent): # if the follower decides to be informed
                numHeardNews = follower.hearNews(numHeardNews)
                newSrcList.append(follower)
        srcList = newSrcList # spread outward like waves
        if numHeardNews >= 0.9*NUM_USERS:
            print("total time taken:", unit, "hours")
            break
        unit += 1

if __name__ == "__main__":
    for i in range(2):
        threading.Thread(target=runSim).start()
