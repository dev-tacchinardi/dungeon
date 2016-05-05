from mazegen.celltype import *


class Cell:
    def __init__(self, x, y, maze=None, cell_type='empty'):
        self.maze = maze
        if maze and (x >= maze.width or y >= maze.height):
            raise ValueError("Position outside bounds of maze.")
        self.x = x
        self.y = y
        self.type = getattr(CellType, cell_type)

    def __repr__(self):
        return "<Cell({}, {}): {}>".format(self.x, self.y, self.type.key)

    def __str__(self):
        return self.type.display

    def is_carveable(self):
        if not self.maze:
            raise Exception("Cell.maze must be set for this operation.")
        return self.type == EmptyCell and len(self.neighbors()) >= 3

    def north(self, carveable=False):

        margin = 2 if carveable else 1
        if self.maze and (
                        self.y >= self.maze.height - margin or
                        ((self.maze[self.x][self.y+1].type != EmptyCell) if carveable else False)
        ):
            return None
        return self.x, self.y + 1

    def east(self, carveable=False):

        margin = 2 if carveable else 1
        if self.maze and (
                        self.x >= self.maze.width - margin or
                        ((self.maze[self.x+1][self.y].type != EmptyCell) if carveable else False)
        ):
            return None
        return self.x + 1, self.y

    def south(self, carveable=False):

        margin = 2 if carveable else 1
        if self.maze and (
                        self.y < margin or
                        ((self.maze[self.x][self.y - 1].type != EmptyCell) if carveable else False)
        ):
            return None
        return self.x, self.y - 1

    def west(self, carveable=False):

        margin = 2 if carveable else 1
        if self.maze and (
                        self.x < margin or
                        ((self.maze[self.x][self.y + 1].type != EmptyCell) if carveable else False)
        ):
            return None
        return self.x - 1, self.y

    def neighbors(self, carveable=False):
        return [i for i in [
            self.north(carveable=carveable),
            self.east(carveable=carveable),
            self.south(carveable=carveable),
            self.west(carveable=carveable)
        ] if i]
