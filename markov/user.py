from random import random

class User:

    def __init__(self, universe, index):
        self.universe = universe
        self.index = index
        self.heardNews = False

    def hearNews(self, numHeardNews):
        self.heardNews = True
        return numHeardNews + 1

    def __str__(self):
        return f'User {self.index}: (heard news, {self.heardNews}); (activity level, {round(self.avgActivityLevel, 2)})'

    @classmethod
    def printUsers(cls):
        for user in cls.userList:
            print(user)
