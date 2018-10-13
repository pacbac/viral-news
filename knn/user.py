from numpy.random import gamma
import math
from random import random

TPRIME = 5 # one hour

class User:

    """
    params:
    - universe: the entire social network
    - index: unique id for the user
    - heardNews: if the user has heard the news yet
    - interestLevel: probability the user cares about the news
    - radius: farthest Euclidean distance from its follower
    """
    def __init__(self, universe, index):
        self.universe = universe
        self.index = index
        self.heardNews = False
        self.interest = random() # probability user cares about the news
        self.radius = 0 # will be changed later once the user's followers circle is picked

    def hearNews(self, numHeardNews):
        self.heardNews = True
        return numHeardNews + 1

    # calculate the time it takes for the other person to hear the news
    def calcTimeHearNews(self, follower):
        dist = self.universe[self][follower]['weight'][1]
        distScale = dist/(2*max(self.radius, follower.radius))
        return int(TPRIME*dist/follower.interest*distScale + random())

    # calculate the probability that the user is informed
    def calcProbInform(self, parent):
        relation = self.universe[parent][self]['weight'][0] # strength of the "following" relationship, from 0 to 1
        return math.sqrt(self.interest*relation)

    """
    assumption: self.heardNews = True
    params:
    - numHeardNews: total number of people that have heard the news
    - toBeHeard: a queue containing the people whose "parents" have shared the news but the user itself
        hasn't personally been informed of the news yet. They will hear the news in the near future,
        as calculated by calcTimeHearNews.
    """
    def shareNews(self, numHeardNews, toBeHeard, unit):
        if random() < self.interest: # then share
            for follower in self.universe.neighbors(self):
                if not follower.heardNews:
                    # timeHearNews: the exact time that the follower should be pushed off the queue and accounted for in numHeardNews
                    timeHearNews = self.calcTimeHearNews(follower)
                    if timeHearNews <= 0:
                        numHeardNews = follower.hearNews(numHeardNews)
                    else:
                        toBeHeard.put((unit + timeHearNews, (self, follower)))
        return numHeardNews

    def __str__(self):
        return f'User {self.index}: (heard news, {self.heardNews}); (interest level, {round(self.interest, 2)})'

    # trivial comparisons for priority queue (doesn't make a difference)
    def __lt__(self, other):
        return self.index < other.index

    def __gt__(self, other):
        return self.index > other.index

    def __eq__(self, other):
        return self.index == other.index

    def __hash__(self):
        return hash(self.index)

    @classmethod
    def printUsers(cls):
        for user in cls.userList:
            print(user)
