import numpy as np
import haversine as hs


class City:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

    def distance(self, city):
        xDis = abs(self.x - city.x)
        yDis = abs(self.y - city.y)
        distance = hs.haversine((self.x, self.y), (city.x, city.y), unit='km')
        return distance

    def __repr__(self):
        return self.name #+ "(" + str(self.x) + "," + str(self.y) + ")"