from dungeon_generator.celltype import *


class Cell:
    def __init__(self, x, y, maze, cell_type='empty'):
        self.maze = maze
        if x >= maze.width or y >= maze.height:
            raise ValueError("Position outside bounds of maze.")
        self.x = x
        self.y = y
        self._cell_type = getattr(CellType, cell_type)
        self._neighbors_cache = {
            'all': None,
            'carveable': None,
            'cell_type': {}
        }

    def __repr__(self):
        return "<Cell({}, {}): {}>".format(self.x, self.y, self.cell_type.key)

    def __str__(self):
        return self.cell_type.display

    @property
    def cell_type(self):
        return self._cell_type

    @cell_type.setter
    def cell_type(self, value):
        self._cell_type = value
        for c in self.neighbors():
            c.invalidate_neighbors_cache()

    def invalidate_neighbors_cache(self):
        self._neighbors_cache = {
            'all': None,
            'carveable': None,
            'cell_type': {}
        }

    def neighbors(self, carveable=False, cell_type=None):
        if carveable:
            if self._neighbors_cache['carveable']:
                return self._neighbors_cache['carveable']
        elif cell_type is not None:
            if cell_type.key in self._neighbors_cache['cell_type']:
                return self._neighbors_cache['cell_type'][cell_type.key]
        elif self._neighbors_cache['all']:
            return self._neighbors_cache['all']

        neighbors = [i for i in [
            self.north(carveable=carveable),
            self.east(carveable=carveable),
            self.south(carveable=carveable),
            self.west(carveable=carveable)
        ] if i and ((i.cell_type == cell_type) if cell_type else True)]

        if carveable:
            self._neighbors_cache['carveable'] = neighbors
        elif cell_type:
            self._neighbors_cache['cell_type'][cell_type.key] = neighbors
        else:
            self._neighbors_cache['all'] = neighbors

        return neighbors

    def is_carveable(self):
        return (
            self.cell_type == EmptyCell and
            not self.is_edge() and
            len(self.neighbors(cell_type=EmptyCell)) >= 3
        )

    def is_edge(self):
        return (
            self.x == 0 or
            self.x == self.maze.width - 1 or
            self.y == 0 or
            self.y == self.maze.height - 1
        )

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

    def direction_towards(self, cell):
        if self.x == cell.x:
            if self.y < cell.y:
                return 'north'
            elif self.y > cell.y:
                return 'south'
        elif self.y == cell.y:
            if self.x < cell.x:
                return 'west'
            elif self.x > cell.x:
                return 'east'
        return None
