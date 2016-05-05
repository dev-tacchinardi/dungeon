import random

from mazegen.cell import Cell
from mazegen.celltype import EmptyCell, FloorCell
from mazegen.room import Room


class Maze:
    ROOM_TRIES = 300
    DISCARD_ADJACENT_CHANCE = 90

    _rooms = []
    grid = None  # will store a 2D array

    def __init__(self, width, height):
        if width % 2 == 0 or height % 2 == 0:
            raise ValueError("Maze height and width must be odd.")
        self.width = width
        self.height = height
        self.grid = [
            [Cell(x, y, self, cell_type=EmptyCell.key) for x in range(width)]
            for y in range(height)
        ]

    def __str__(self):
        ret = '='.join(['' for _ in range(0, self.width + 5)]) + '\n'
        for y in reversed(range(self.height)):
            line = '| '
            for x in range(self.width):
                line += str(self.grid[x][y])
            ret += line + ' |\n'
        ret += '='.join(['' for _ in range(0, self.width + 5)])
        return ret

    def __getitem__(self, item):
        if not isinstance(item, int):
            raise ValueError("Index must be an integer.")
        return self.grid[item]

    def cells(self):
        for x in range(0, self.width):
            for y in range(0, self.height):
                yield self[x][y]

    def generate(self):
        return (
            self._generate_rooms() and
            self._flood()
        )

    def _generate_rooms(self):
        self._rooms = []
        for i in range(Maze.ROOM_TRIES):
            pos_x = random.randrange(1, self.width - Room.MAX_WIDTH)
            pos_y = random.randrange(1, self.height - Room.MAX_HEIGHT)
            width = random.randint(Room.MIN_WIDTH, Room.MAX_WIDTH)
            height = random.randint(Room.MIN_HEIGHT, Room.MAX_HEIGHT)

            new_room = Room(pos_x, pos_y, width, height)
            for room in self._rooms:
                if new_room.overlaps(room):
                    break
                if new_room.is_adjacent_to(room=room):
                    if random.randrange(100) < Maze.DISCARD_ADJACENT_CHANCE:
                        break
            else:
                self._rooms.append(new_room)

        for room in self._rooms:
            for i in range(room.pos_x, room.pos_x + room.width):
                for j in range(room.pos_y, room.pos_y + room.height):
                    self.grid[i][j] = Cell(i, j, maze=self, cell_type=FloorCell.key)

        print('{} rooms generated'.format(len(self._rooms)))
        return True

    def _flood(self):
        def find_origin():
            for c in self.cells():
                # import pdb; pdb.set_trace()
                if c.type != EmptyCell:
                    continue
                if len(c.neighbors(carveable=True)) == 4:
                    return c
            return None

        while True:
            origin = find_origin()
            if not origin:
                break
            self.grid[origin.x][origin.y] = Cell(origin.x, origin.y, self, FloorCell.key)

            valid_cells = [origin]
            while len(valid_cells) != 0:
                cell = random.choice(valid_cells)
                carveable_neighbors = cell.neighbors(carveable=True)
                if carveable_neighbors:
                    to_carve = random.choice(carveable_neighbors)
                    carved_cell = Cell(to_carve[0], to_carve[1], self, FloorCell.key)
                    self.grid[to_carve[0]][to_carve[1]] = carved_cell
                    valid_cells.append(carved_cell)
                    # print(maze)
                else:
                    valid_cells.remove(cell)
        return True


if __name__ == '__main__':
    maze = Maze(51, 51)
    while not maze.generate():
        print('Generation failed, retrying...')
    print(maze)
