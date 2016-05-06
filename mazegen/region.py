from cell import Cell
from celltype import EmptyCell, FloorCell


class Region:
    id = 1

    def __init__(self):
        self.id = Region.id
        Region.id += 1

        self.cells = []

    def __iadd__(self, other):
        if not isinstance(other, Cell):
            raise TypeError("rhs must be Cell instance")
        if other in self.cells:
            raise ValueError("Cell already in region.")
        self.cells.append(other)
        return self

    def around(self, connecting=False):
        empty_cells = []
        for cell in self.cells:
            for c in cell.neighbors(cell_type=EmptyCell):
                if not connecting or len(c.neighbors(cell_type=FloorCell)) == 2:
                    empty_cells.append(c)
        return list(set(empty_cells))
