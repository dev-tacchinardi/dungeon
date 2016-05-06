import time
from PIL import Image

from celltype import EmptyCell
from maze import Maze


if __name__ == '__main__':
    maze = Maze(51, 51)
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
                value = 128
            elif maze[x][y].cell_type == EmptyCell:
                value = 0
            else:
                value = 255
            row.extend([value] * image_size)
        pixels.extend(row * image_size)

    image = Image.frombytes(
        'L', (maze.width * image_size, maze.height * image_size),
        bytes([p for p in pixels])
    )
    image.show()
