from celltype import *


class Cell:
    def __init__(self, x, y, maze, cell_type='empty'):
        self.maze = maze
        if x >= maze.width or y >= maze.height:
            raise ValueError("Position outside bounds of maze.")
        self.x = x
        self.y = y
        self.cell_type = getattr(CellType, cell_type)

    def __repr__(self):
        return "<Cell({}, {}): {}>".format(self.x, self.y, self.cell_type.key)

    def __str__(self):
        return self.cell_type.display

    def is_carveable(self):
        return (
            self.cell_type == EmptyCell and
            not self.is_edge() and
            len(self.neighbors(cell_type=EmptyCell)) >= 3
        )

    def is_edge(self):
        # len(self.neighbors()) != 4  de olabilir
        return (
            self.x == 0 or
            self.x == self.maze.width - 1 or
            self.y == 0 or
            self.y == self.maze.height - 1
        )

    def neighbors(self, carveable=False, cell_type=None):
        return [i for i in [
            self.north(carveable=carveable),
            self.east(carveable=carveable),
            self.south(carveable=carveable),
            self.west(carveable=carveable)
        ] if i and ((i.cell_type == cell_type) if cell_type else True)]

    def north(self, carveable=False):
        if self.y >= self.maze.height - 1:
            return None
        cell = self.maze[self.x][self.y + 1]
        if carveable and not cell.is_carveable():
            return None
        return cell

    def east(self, carveable=False):
        if self.x >= self.maze.width - 1:
            return None
        cell = self.maze[self.x + 1][self.y]
        if carveable and not cell.is_carveable():
            return None
        return cell

    def south(self, carveable=False):
        if self.y < 1:
            return None
        cell = self.maze[self.x][self.y - 1]
        if carveable and not cell.is_carveable():
            return None
        return cell

    def west(self, carveable=False):
        if self.x < 1:
            return None
        cell = self.maze[self.x - 1][self.y]
        if carveable and not cell.is_carveable():
            return None
        return cell
