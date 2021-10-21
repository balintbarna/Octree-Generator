import numpy as np
import json
import matplotlib.pyplot as plt
from math import floor
from point import Point
from node import Node

with open("allPointsList.json") as f1:
    pcdata = json.load(f1)
    if type(pcdata) is not list:
        print("Data stream is not list!")
        exit()
    pcarr = np.array(pcdata)
    print("cloud data shape: {}".format(pcarr.shape))

    with open("allPointsTypeList.json") as f2:
        typedata = json.load(f2)
        if type(typedata) is not list:
            print("Data stream is not list!")
            exit()
        typearr = np.array(typedata)
        print("type data shape: {}".format(typearr.shape))

        if not len(pcarr) == len(typearr):
            print("array counts do not match: {} vs {}".format(len(pcarr), len(typearr)))
            exit()

        values = Point.create(pcarr[:, 0], pcarr[:, 1], pcarr[:, 2], typearr)


center = Point.fromList([(np.min(v) + np.max(v)) / 2 for v in values.coords])
print("center: {}".format(center.coords))
centered = pcarr - list(center.coords)
edge_length = 2*np.amax(np.abs(centered))
print("edge length: {}".format(edge_length))
root_node = Node(center, edge_length)
outliers = root_node.filter_points([Point.create(value[0], value[1], value[2], typearr[index]) for index, value in enumerate(pcarr)])
if len(outliers) > 0:
    raise "there are outliers"
root_node.propagate()
end_nodes = root_node.get_all_end_nodes()
print("number of end nodes: {}".format(len(end_nodes)))

def data_to_color(data):
    if data == "void":
        return "black"
    elif data == "IfcWallStandardCase":
        return "yellow"
    elif data == "IfcSpace":
        return "blue"
    elif data == "IfcSlab":
        return "red"
    elif data == "IfcDoor":
        return "white"
    else:
        print("no color set for {}".format(data))
        return "gray"
colors = [data_to_color(node.data) for node in end_nodes]
nodes = Point.create(
    [node.center.x for node in end_nodes],
    [node.center.y for node in end_nodes],
    [node.center.z for node in end_nodes],
    colors,
)
sizes = [node.length for node in end_nodes]


fig = plt.figure(figsize=plt.figaspect(0.5))
colors = [data_to_color(data) for data in values.data]
ax = fig.add_subplot(1, 2, 1, projection='3d')
ax.title.set_text("Full point cloud")
ax.scatter(values.x, values.y, values.z, c=colors, cmap='viridis', linewidth=0.5)

ax = fig.add_subplot(1, 2, 2, projection='3d')
ax.title.set_text("Octree nodes visualized")
ax.scatter(nodes.x, nodes.y, nodes.z, c=nodes.data, cmap='viridis', linewidth=0.5)

plt.show()


print("done")