from numpy.random import gamma
from random import random
import math

K = 1
DECAY_RATE = 0.9 # decay parameter for probability of sending an impulse
ALPHA = 0.5 # tuning parameter for impulse

class Community:
    # Note: cannot set a universe class varible b/c multiple threads would share and modify it

    """
    params:
    - universe: the universe of all communities, shared by all communities
    - id: unique to each community
    - informedRatio: ratio of users in the community informed about the news
    - pop: the number of users in the community
    - conductance: a constant from 0-1 that determines how strongly connected the community is
        - Higher conductance = higher avg followers within the community
    - impulse: an accelerator variable that propels the news spreading for
        a different community
    - impulseStrength: determines the relative strength of the community's message
        to other communities
    """
    def __init__(self, universe, id, pop, hasInformed):
        self.id = id
        probInform = 0.02*random()
        self.informedRatio = probInform if hasInformed else 0
        self.pop = pop
        self.conductance = random()
        self.impulse = 0
        self.impulseStrength = math.sqrt(pop**2 * self.informedRatio)

    """
    Updates the community's impulse
    params:
    - other: Another community
    """
    def updateImpulse(self, other):
        self.impulse += self.impulseStrength*other.pop/self.pop

    """
    Calculates the informed population after an updated time interval
    params:
    - time: elapsed dissemination time in hours
    """
    def calcPopInform(self, time):
        return min(int(K*self.conductance*time/math.log(self.pop)*self.pop) + self.impulseStrength, self.pop)

    def __str__(self):
        return str(self.id)

    """
    params:
    - G: universe of communities
    - a, b: communities
    Return value: the edge connection (probability of impulse) shared from a to b
    """
    @classmethod
    def getProbImpulse(cls, G, a, b):
        if a in G and b in G[a] and 'weight' in G[a][b]:
            return G[a][b]['weight']
        return 0

    """
    params:
    - G: universe of communities
    - a, b: communities
    """
    @classmethod
    def updateProbImpulse(cls, G, a, b):
        G[a][b]['weight'] += ALPHA*a.impulseStrength

    """
    If there is a connection between a and b, decay it
    params:
    - G: universe of communities
    - a, b: communities
    """
    @classmethod
    def decayProbImpulse(cls, G, a, b):
        if a in G and b in G[a] and 'weight' in G[a][b]:
            G[a][b]['weight'] = DECAY_RATE*cls.getProbImpulse(G, a, b)
