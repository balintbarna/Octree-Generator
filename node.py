import numpy as np
from point import Point

class NodeConfig:
    def __init__(self) -> None:
        self.min_points_to_break = 10


class Node:
    def __init__(self, center, edge_length, config = NodeConfig()) -> None:
        self._points = []
        self._center: Point = center
        self._edge_length: float = edge_length
        self._config: NodeConfig = config
        self._children = None


    def filter_points(self, points):
        if type(points) is not list:
            raise "points not list"
        min = Point.fromList([a - self._edge_length / 2 for a in self._center.values])
        max = Point.fromList([a + self._edge_length / 2 for a in self._center.values])
        remainder = []
        for point in points:
            if point.x >= min.x and point.x <= max.x and point.y >= min.y and point.y <= max.y and point.z >= min.z and point.z <= max.z:
                self._points.append(point)
            else:
                remainder.append(point)
        return remainder


    def propagate(self):
        if not self._children and len(self._points) >= self._config.min_points_to_break:
            self._children = []
            for modulator in range(8):
                directions = np.array([((modulator >> axis) % 2) * 2 - 1 for axis in range(3)])
                center = Point.fromList(self._center.values + directions*(self._edge_length/4))
                self._children.append(Node(center, self._edge_length / 2, self._config))
        if self._children:
            for child in self._children:
                self._points = child.filter_points(self._points)
                child.propagate()
            if len(self._points) > 0:
                print("node: {}".format(self))
                raise "error: children didn't eat up all the parent node points"

    
    def get_all_end_nodes(self):
        nodes = []
        if self._children and len(self._children) > 0:
            for child in self._children:
                nodes.extend(child.get_all_end_nodes())
        else:
            nodes.append(self)
        return nodes
    

    def __str__(self) -> str:
        return "center: {}\nlength: {}\npoints: {}\nchildren: {}".format(self._center, self._edge_length, self._points, self._children)


    def __repr__(self) -> str:
        return str(self)


    @property
    def center(self):
        return self._center


    @property
    def length(self):
        return self._edge_length
