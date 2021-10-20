import numpy as np
import json
import matplotlib.pyplot as plt
from math import floor
from point import Point
from node import Node

file = open("allPointsList.json")
pcdata = json.load(file)
if type(pcdata) is not list:
    print("Data stream is not list!")
    exit()
pcarr = np.array(pcdata)
print("data shape: {}".format(pcarr.shape))
values = Point.create(pcarr[:, 0], pcarr[:, 1], pcarr[:, 2])


fig = plt.figure()
ax = plt.axes(projection='3d')
# Data for a three-dimensional line
zline = np.linspace(0, 15, 1000)
xline = np.sin(zline)
yline = np.cos(zline)
ax.plot3D(xline, yline, zline, 'gray')
# Data for three-dimensional scattered points
zdata = 15 * np.random.random(100)
xdata = np.sin(zdata) + 0.1 * np.random.randn(100)
ydata = np.cos(zdata) + 0.1 * np.random.randn(100)
ax.scatter3D(values.x, values.y, values.z, c=values.z, cmap='Greens')


center = Point.fromList([(np.min(v) + np.max(v)) / 2 for v in values.values])
print("center: {}".format(center.values))
centered = pcarr - center.values
edge_length = 2*np.amax(np.abs(centered))
print("edge length: {}".format(edge_length))
root_node = Node(center, edge_length)
root_node.filter_points([Point.fromList(a) for a in pcarr])

print("done")