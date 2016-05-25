import time
import sys
from PIL import Image

from celltype import EmptyCell
from maze import Maze


if __name__ == '__main__':
    width, height = 75, 75
    if len(sys.argv) >= 3:
        width = int(sys.argv[1])
        height = int(sys.argv[2])

    maze = Maze(width, height)
    t1 = time.clock()
    while not maze.generate():
        t2 = time.clock()
        print('Generation failed in {} seconds, retrying...'.format(t2 - t1))
        t1 = time.clock()
    t3 = time.clock()
    print('Generation SUCCESS in {} seconds.'.format(t3 - t1))

    image_size = 5

    pixels = []
    for y in reversed(range(maze.height)):
        row = []
        for x in range(maze.width):
            if x == 0 and y == 0:
                value = (255, 0, 0)
            elif maze[x][y].cell_type == EmptyCell:
                value = (0, 0, 0)
            else:
                value = (255, 255, 255)
            row.extend([value[0]] * image_size + [value[1]] * image_size + [value[2]] * image_size)
        pixels.extend(row * image_size)

    image = Image.frombytes(
        'RGB', (maze.width * image_size, maze.height * image_size),
        bytes([p for p in pixels])
    )
    image.show()
