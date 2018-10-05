from numpy.random import gamma

class User:

    def __init__(self, universe, index):
        self.universe = universe
        self.index = index
        self.probShare = gamma(2)
        self.heardNews = False
        self.avgActivityLevel = gamma(2) # activity level = probability the user sees certain news

    def hearNews(self):
        self.heardNews = True

    # assumption: heardNews = True
    def shareNews(self, numHeardNews=0):
        for follower in self.universe.neighbors(self):
            if gamma(2) <= self.universe[self][follower]['weight'] and not follower.heardNews:
                follower.hearNews()
                numHeardNews += 1
        return numHeardNews

    def __str__(self):
        return f'User {self.index}: (heard news, {self.heardNews}); (activity level, {round(self.avgActivityLevel, 2)})'

    @classmethod
    def printUsers(cls):
        for user in cls.userList:
            print(user)
