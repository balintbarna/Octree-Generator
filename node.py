from point import Point

class NodeConfig:
    def __init__(self) -> None:
        self.min_points_to_break = 10


class Node:
    def __init__(self, center, edge_length, config = NodeConfig()) -> None:
        self._points = []
        self._center: Point = center
        self._edge_length: float = edge_length
        self._config = config


    def filter_points(self, points):
        if type(points) is not list:
            raise "points not list"
        min = Point.fromList([a - self._edge_length / 2 for a in self._center.values])
        max = Point.fromList([a + self._edge_length / 2 for a in self._center.values])
        remainder = []
        for point in points:
            if point.x >= min.x and point.x <= max.x:
                self._points.append(point)
            else:
                remainder.append(point)
        return remainder


    def propagate(self):
        if not self._children and len(self._points) >= self._min_points_to_propagate:
            self._children = []
            for modulator in range(8):
                directions = [((modulator >> axis) % 2) * 2 - 1 for axis in range(3)]
                center = Point.fromList(self._center.values + self._edge_length*directions)
                self._children.append(Node(center, self._edge_length / 2, self._config))
        if self._children:
            for child in self._children:
                self._points = child.filter_points(self._points)
                child.propagate()
                pass
