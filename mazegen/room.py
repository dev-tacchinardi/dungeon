

class Room:
    MIN_WIDTH = 5
    MIN_HEIGHT = 5
    MAX_WIDTH = 20
    MAX_HEIGHT = 20

    def __init__(self, pos_x, pos_y, width, height):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height

    def __str__(self):
        return "(%s, %s), (%s, %s)" % (self.left, self.bottom, self.right, self.top)

    @property
    def left(self):
        return self.pos_x

    @property
    def right(self):
        return self.pos_x + self.width

    @property
    def bottom(self):
        return self.pos_y

    @property
    def top(self):
        return self.pos_y + self.height

    def overlaps(self, room):
        # https://silentmatt.com/rectangle-intersection/
        return (
            self.left < room.right and
            self.right > room.left and
            self.bottom < room.top and
            self.top > room.bottom
        )

    def is_adjacent_to(self, room=None, pos=None):
        if room:
            if ((self.left < room.right) ^
                    (self.right > room.left) ^
                    (self.bottom < room.top) ^
                    (self.top > room.bottom)):
                return (
                    self.left == room.right or
                    self.right == room.left or
                    self.bottom == room.top or
                    self.top == room.bottom
                )
            else:
                return False
        elif pos:
            # is the position inside the room?
            if self.left <= pos[0] < self.right and self.bottom <= pos[1] < self.top:
                return True
            # if distance^2 > 1, there's no adjacency
            else:
                dist_x = min(abs(pos[0] - self.left), abs(pos[0] - self.right))
                dist_y = min(abs(pos[1] - self.bottom), abs(pos[1] - self.top))
                return (dist_x + dist_y) <= 1
        else:
            raise ValueError("Need either a room or a position to check adjacency!")
