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




center = Point.fromList([(np.min(v) + np.max(v)) / 2 for v in values.values])
print("center: {}".format(center.values))
centered = pcarr - center.values
edge_length = 2*np.amax(np.abs(centered))
print("edge length: {}".format(edge_length))
root_node = Node(center, edge_length)
outliers = root_node.filter_points([Point.fromList(a) for a in pcarr])
if len(outliers) > 0:
    raise "there are outliers"
root_node.propagate()
end_nodes = root_node.get_all_end_nodes()
print("number of end nodes: {}".format(len(end_nodes)))
nodes = Point.create(
    [node.center.x for node in end_nodes],
    [node.center.y for node in end_nodes],
    [node.center.z for node in end_nodes]
)
sizes = [node.length for node in end_nodes]


fig = plt.figure(figsize=plt.figaspect(0.5))

ax = fig.add_subplot(1, 2, 1, projection='3d')
ax.title.set_text("Full point cloud")
ax.scatter(values.x, values.y, values.z, c=values.z, cmap='viridis', linewidth=0.5)

ax = fig.add_subplot(1, 2, 2, projection='3d')
ax.title.set_text("Octree nodes visualized")
ax.scatter(nodes.x, nodes.y, nodes.z, c=nodes.z, cmap='viridis', linewidth=0.5)

plt.show()


print("done")