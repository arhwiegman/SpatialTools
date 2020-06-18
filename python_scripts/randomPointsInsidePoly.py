# random points inside polygon
from matplotlib.plot import plt
import numpy as np
from shapely.geometry import Polygon, Point

poly = Polygon([(141.4378366, -25.95915986), 
				(165.4279876, -29.43400298), 
				(163.1382942, -47.65345814), 
				(133.1675418, -42.99807751)])

def randomPointsWithin(poly, num_points):
    min_x, min_y, max_x, max_y = poly.bounds

    points = []

    while len(points) < num_points:
        random_point = Point([random.uniform(min_x, max_x), random.uniform(min_y, max_y)])
        if (random_point.within(poly)):
            points.append(random_point)
    return (points)

# %% This is a cell

# randCirlcsInsidePoly -------------------------------------------------------
# create randomly selected points inside a polygon with a specified radius
def randomCirclesInsidePoly(poly, numPoints=1, radius=1,sides=64):
    import numpy as np
    from shapely.geometry import Polygon, Point
    min_x, min_y, max_x, max_y = poly.bounds
    circles = []
    while len(circles) < numPoints:
        # generate random uniform number between min and max of bounds
        randomPoint = Point([np.random.uniform(min_x, max_x), np.random.uniform(min_y, max_y)])
        randomCircle = randomPoint.buffer(radius,sides)
        if (randomCircle.within(poly)):
            circles.append(randomCircle)
    return(circles)

circs = randomCirclesWithinPoly(poly)

#print(circs)
#import matplotlib.pyplot as plt
print(circs)
# %% 


