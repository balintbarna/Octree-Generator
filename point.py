class Point(object):
    def __init__(self, **kwargs):
        """Sets all values once given
        whatever is passed in kwargs
        """
        for k, v in kwargs.items():
            object.__setattr__(self, k, v)


    @classmethod
    def create(cls, x, y, z, data):
        return cls(_x=x, _y=y, _z=z, _data=data)
    

    @staticmethod
    def fromList(list):
        if len(list) == 3:
            return Point.create(list[0], list[1], list[2], None)
        elif len(list) == 4:
            return Point.create(list[0], list[1], list[2], list[3])
        else:
            raise "wrong format list for point"


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
    

    def __str__(self) -> str:
        return "x: {}\ny: {}\nz: {}\ndata: {}\n".format(self.x, self.y, self.z, self.data)


    def __repr__(self) -> str:
        return str(self)
    
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    @property
    def z(self):
        return self._z
    
    @property
    def coords(self):
        return (self.x, self.y, self.z)
    
    @property
    def data(self):
        return self._data



if __name__ == "__main__":
    p =Point.create(1, 2, 3, "data")
    print(str(p))
