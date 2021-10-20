class Point(object):
    def __init__(self, **kwargs):
        """Sets all values once given
        whatever is passed in kwargs
        """
        for k, v in kwargs.items():
            object.__setattr__(self, k, v)

    @classmethod
    def create(cls, x, y, z):
        return cls(x=x, y=y, z=z)
    
    @staticmethod
    def fromList(list):
        return Point.create(list[0], list[1], list[2])

    def __getattribute__(self, item):
        result = super(Point, self).__getattribute__(item)
        if item == '__dict__':
            return dict(**result)
        return result

    def __setattr__(self, *args):
        """Disables setting attributes via
        item.prop = val or item['prop'] = val
        """
        raise TypeError('Immutable objects cannot have properties set after init')

    def __delattr__(self, *args):
        """Disables deleting properties"""
        raise TypeError('Immutable objects cannot have properties deleted')
    
    @property
    def values(self):
        return [self.x, self.y, self.z]

if __name__ == "__main__":
    p =Point.create(1, 2, 3)
    print("x: {}\ny: {}\nz: {}".format(p.x, p.y, p.z))