

class CellType:
    _types = {}

    def __init__(self):
        raise NotImplementedError("Cannot instantiate CellType.")

    @property
    def key(self):
        raise NotImplementedError("Base class CellType cannot be accessed by type key.")

    @staticmethod
    def add_type(klass):
        setattr(CellType, klass.key, klass)


class EmptyCell(CellType):
    def __init__(self):
        super().__init__()

    key = 'empty'
    display = ' '


class FloorCell(CellType):
    def __init__(self):
        super().__init__()

    key = 'floor'
    display = '#'


for c in CellType.__subclasses__():
    CellType.add_type(c)
    print("{} cell type added".format(c.key))


__all__ = ['CellType', 'EmptyCell', 'FloorCell']
