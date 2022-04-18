from typing import List
from test_data import polygon
from shapely.geometry import Point, Polygon


class triangulation(polygon):
    def __init__(self, n):
        super().__init__(n)
        super().generate()
        self.name = {}
        self.partition = []
        # naming of points to identify the intersecting ones
        for i in range(len(self.poly.exterior.coords)-1):
            self.name[self.poly.exterior.coords[i]] = i
    # dp is a n*n matrix storing permeter

    def tri_perimeter(self, points: Polygon):
        perimeter = 0
        for i in range(len(points.exterior.coords)-1):
            x = points.exterior.coords[i]
            y = points.exterior.coords[i+1]
            perimeter = perimeter +\
                Point(x[0], x[1]).distance(
                    Point(y[0], y[1]))
        return perimeter

    def dynamic(self, points: Polygon, dp):
        # dp is a 2d matrix storing the perimeter of the polygons formed by the diagonals of two indexed points
        if len(points.exterior.coords)-1 == 3:
            i = self.name[points.exterior.coords[0]]
            j = self.name[points.exterior.coords[2]]
            dp[i][j] = self.tri_perimeter(points)
            #dp[j][i] = dp[i][j]
            return dp[i][j]

        length = len(points.exterior.coords)-1
        min_peri = float('inf')
        i_min = float('-inf')
        j_min = float('-inf')
        for i in range(length):
            for j in range(i+2, length):
                # note first and last(here second last) cannot be diagonals
                if i == 0 and j == length-1:
                    continue
                point1 = self.name[points.exterior.coords[i]]
                point2 = self.name[points.exterior.coords[j]]
                if dp[point1][point2] == float('-inf'):
                    x, y = points.exterior.xy
                    x1 = x[i:j+1]
                    y1 = y[i:j+1]
                    z = zip(x1, y1)
                    dp[point1][point2] = self.dynamic(Polygon(z), dp)
                    x2 = x[j:length]+x[0:i+1]
                    y2 = y[j:length]+y[0:i+1]
                    z = zip(x2, y2)
                    dp[point2][point1] = self.dynamic(Polygon(z), dp)
                if dp[point1][point2]+dp[point2][point1] < min_peri:
                    min_peri = dp[point1][point2]+dp[point2][point1]
                    i_min = point1
                    j_min = point2
        self.partition.append(sorted((i_min, j_min)))
        return min_peri


p = triangulation(5)
print(p.name)
dp = [[float('-inf') for i in range(len(p.name))] for i in range(len(p.name))]
p.dynamic(p.poly, dp)
print(p.partition)
p.plot()
