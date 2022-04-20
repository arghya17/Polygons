from shapely.geometry import Polygon
from matplotlib import pyplot as plt
import random


class polygon:
    def __init__(self, n):
        self.poly = Polygon()
        self.sides = n
        self.range = 50
        if(n*10 > self.range):
            self.range = n*10

    def generate(self):
        random.SystemRandom()
        x = random.sample(range(-self.range, self.range), self.sides)
        y = random.sample(range(-self.range, self.range), self.sides)
        z = list(zip(x, y))
        self.poly = Polygon(z)
        self.poly = self.poly.convex_hull
        n = len(self.poly.exterior.xy[0])-1
        while n < self.sides:
            random.SystemRandom()
            x, y = (random.randint(-self.range, self.range),
                    random.randint(-self.range, self.range))
            x1, y1 = self.poly.exterior.xy
            x1.append(x)
            y1.append(y)
            z = list(zip(x1, y1))
            self.poly = Polygon(z)
            self.poly = self.poly.convex_hull
            n = len(self.poly.exterior.xy[0])-1

    def plot(self):
        x, y = self.poly.exterior.xy
        plt.plot(x, y)
        plt.show()


p = polygon(5)
p.generate()
print(p.poly.exterior.coords[:])
