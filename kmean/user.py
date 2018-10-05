from numpy.random import gamma

INTEREST_THRESHOLD = 0.75

class User:

    def __init__(self, universe, index):
        self.universe = universe
        self.index = index
        self.heardNews = False
        self.interestLevel = gamma(2, scale=2.0) # activity level = probability the user sees certain news

    def hearNews(self):
        self.heardNews = True

    # assumption: heardNews = True
    def shareNews(self, numHeardNews=0):
        if self.interestLevel >= INTEREST_THRESHOLD: # then share
            for follower in self.universe.neighbors(self):
                if not follower.heardNews:
                    follower.hearNews()
                    numHeardNews += 1
        return numHeardNews

    def __str__(self):
        return f'User {self.index}: (heard news, {self.heardNews}); (activity level, {round(self.avgActivityLevel, 2)})'

    @classmethod
    def printUsers(cls):
        for user in cls.userList:
            print(user)
