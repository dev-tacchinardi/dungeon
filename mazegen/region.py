from dungeon_generator.cell import Cell
from dungeon_generator.celltype import EmptyCell, FloorCell


class Region:
    id = 1

    def __init__(self):
        self.id = Region.id
        Region.id += 1

        self.cells = []

    def __eq__(self, other):
        if not isinstance(other, Region):
            raise TypeError("rhs must be Cell instance")
        return self.id == other.id

    def __ne__(self, other):
        if not isinstance(other, Region):
            raise TypeError("rhs must be Cell instance")
        return self.id != other.id

    def __iadd__(self, other):
        if not isinstance(other, Cell):
            raise TypeError("rhs must be Cell instance")
        if other in self.cells:
            raise ValueError("Cell already in region.")
        self.cells.append(other)
        return self

    def __isub__(self, other):
        if not isinstance(other, Cell):
            raise TypeError("rhs must be Cell instance")
        if other not in self.cells:
            raise ValueError("Cell not in region.")
        self.cells.remove(other)
        return self

    def around(self, connecting=False):
        empty_cells = set()
        for cell in self.cells:
            for c in cell.neighbors(cell_type=EmptyCell):
                if not connecting or len(c.neighbors(cell_type=FloorCell)) == 2:
                    empty_cells.add(c)
        return list(empty_cells)
