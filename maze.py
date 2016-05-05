"""
Source from http://www.roguebasin.com/index.php?title=Dungeon_builder_written_in_Python
"""
from random import *
from math import *


class Maze:

    def __init__(self):
        self.roomList = []
        self.cList = []
        self.corridorList = []

    def makeMap(self, xsize, ysize, fail, b1, mrooms):
        """Generate random layout of rooms, corridors and other features"""
        # makeMap can be modified to accept arguments for values of failed, and percentile of features.
        # Create first room
        self.size_x = xsize
        self.size_y = ysize
        # initialize map to all walls
        self.mapArr = []
        for y in range(ysize):
            tmp = []
            for x in range(xsize):
                tmp.append(1)
            self.mapArr.append(tmp)

        failed = 0

        while failed < fail:
            w, l, t = self.makeRoom()
            ey2 = randrange(ysize - 1 - l) + 1
            ex2 = randrange(xsize - 1 - w) + 1
            roomDone = self.placeRoom(l, w, ex2, ey2, xsize, ysize, t, 0)
            if roomDone == 0:
                failed += 1
            elif roomDone == 1:
                ex, ey, ex2, ey2, et = self.makeExit(len(self.roomList)-1)
                self.makePortal(ex, ey)

        while failed < 2500:
            w, l, t = self.makeCorridor()
            ey2 = randrange(ysize - 1 - l) + 1
            ex2 = randrange(xsize - 1 - w) + 1
            roomDone = self.placeRoom(l, w, ex2, ey2, xsize, ysize, t, 0)
            if roomDone == 0:
                failed += 1

        self.finalJoins()
        self.joinAll()
        self.deleteDeadEnd()
        self.check_reacability()
        checked = True
        for y in range(self.size_y):
            for x in range(self.size_x):
                if self.mapArr[y][x] == 0:
                    checked = False
                    break
            if not checked:
                break
        if not checked:
            self.makeMap(xsize, ysize, fail, b1, mrooms)
            
    def deleteDeadEnd(self):
        ranges = [[range(self.size_y), range(self.size_x)],
                  [range(self.size_y - 1, -1, -1), range(self.size_x - 1, -1, -1)],
                  [range(self.size_y - 1, -1, -1), range(self.size_x)],
                  [range(self.size_y), range(self.size_x - 1, -1, -1)]
        ]
        for yrng, xrng in ranges:
            for y in yrng:
                for x in xrng:
                    movement_area = []
                    if self.mapArr[y][x] == 0:
                        neighbours = [[y - 1, x], [y + 1, x], [y, x - 1], [y, x + 1]]
                        try:
                            movement_area = list(filter(lambda x: self.mapArr[x[0]][x[1]] == 0, neighbours))
                        except:
                            pass
                        finally:
                            if len(movement_area) < 2:
                                self.mapArr[y][x] = 1

    def check_reacability(self, point=None):
        if not point:
            found = False
            for y in range(self.size_y):
                for x in range(self.size_x):
                    if self.mapArr[y][x] == 0:
                        self.check_reacability(point=(y, x))
                        found = True
                        break
                if found:
                    break
        else:
            y, x = point
            if self.mapArr[y][x] == 0:
                self.mapArr[y][x] = 8
                neighbours = [[y - 1, x], [y + 1, x], [y, x - 1], [y, x + 1]]
                
                for pnt in neighbours:
                    self.check_reacability(point=pnt)
        
    def joinAll(self):
        # room -> (h, w, x ,y)
        united = self.roomList
        for corridor in self.corridorList:
            try:
                united.index(corridor)
            except ValueError:
                united.append(corridor)
        for room in united:
            headings = [0, 1, 2, 3]
            trial = 100
            while headings and trial:
                heading = choice(headings)
                if heading == 0:  # North wall
                    rx = randrange(room[1]) + room[2]
                    ry = room[3] - 1
                    rx2 = rx
                    ry2 = ry - 1
                elif heading == 1:  # East wall
                    ry = randrange(room[0]) + room[3]
                    rx = room[2] + room[1]
                    rx2 = rx + 1
                    ry2 = ry
                elif heading == 2:  # South wall
                    rx = randrange(room[1]) + room[2]
                    ry = room[3] + room[0]
                    rx2 = rx
                    ry2 = ry + 1
                elif heading == 3:  # West wall
                    ry = randrange(room[0]) + room[3]
                    rx = room[2] - 1
                    rx2 = rx - 1
                    ry2 = ry
                if ry2 < self.size_y and rx2 < self.size_x and self.mapArr[ry2][rx2] == 0:
                    self.mapArr[ry][rx] = 0
                    headings.pop(headings.index(heading))
                else:
                    trial -= 1
                # if self.mapArr[ry][rx] == 2:  # If space is a wall, exit
                #    self.mapArr[ry][rx]

    def makeRoom(self):
        """Randomly produce room size"""
        rtype = 5
        rwide = randrange(5, 10)
        rlong = randrange(5, 10)
        return rwide, rlong, rtype

    def makeCorridor(self):
        """Randomly produce corridor length and heading"""
        clength = randrange(3, 21)
        heading = randrange(4)
        if heading == 0:  # North
            wd = 1
            lg = -clength
        elif heading == 1:  # East
            wd = clength
            lg = 1
        elif heading == 2:  # South
            wd = 1
            lg = clength
        elif heading == 3:  # West
            wd = -clength
            lg = 1
        return wd, lg, heading

    def placeRoom(self, ll, ww, xposs, yposs, xsize, ysize, rty, ext):
        """Place feature if enough space and return canPlace as true or false"""
        # Arrange for heading
        xpos = xposs
        ypos = yposs
        if ll < 0:
            ypos += ll + 1
            ll = abs(ll)
        if ww < 0:
            xpos += ww + 1
            ww = abs(ww)
        # Make offset if type is room
        if rty == 5:
            if ext == 0 or ext == 2:
                offset = randrange(ww)
                xpos -= offset
            else:
                offset = randrange(ll)
                ypos -= offset
        # Then check if there is space
        canPlace = 1
        if rty != 5:

            ww = ((ww + xpos + 1) - (xsize - 1)) > 0 and ww - ((ww + xpos + 1) - (xsize - 1)) or ww
            ll = ((ll + ypos + 1) - ysize) > 0 and ll - ((ll + ypos + 1) - ysize) or ll
            if ww <= 0:
                canPlace = 0
                return canPlace
            if ll <= 0:
                canPlace = 0
                return canPlace

        if ww + xpos + 1 > xsize - 1 or ll + ypos + 1 > ysize:
            canPlace = 0
            return canPlace
        elif xpos < 1 or ypos < 1:
            canPlace = 0
            return canPlace
        else:
            for j in range(ll):
                for k in range(ww):
                    if self.mapArr[(ypos) + j][(xpos) + k] != 1:
                        canPlace = 2
        # If there is space, add to list of rooms
        if canPlace == 1:
            temp = [ll, ww, xpos, ypos]
            self.roomList.append(temp)
            self.corridorList.extend(rty == 5 and [] or [temp])
            for j in range(ll + 2):  # Then build walls
                for k in range(ww + 2):
                    self.mapArr[(ypos - 1) + j][(xpos - 1) + k] = 2
            for j in range(ll):  # Then build floor
                for k in range(ww):
                    self.mapArr[ypos + j][xpos + k] = 0
        return canPlace  # Return whether placed is true/false

    def makeExit(self, rn):
        """Pick random wall and random point along that wall"""
        room = self.roomList[rn]
        x_range = list(range(room[1]))
        y_range = list(range(room[0]))
        rw_range = list(range(4))
        found = False
        while rw_range:
            rw = choice(rw_range)
            if rw == 0:  # North wall
                rx = choice(x_range) + room[2]
                ry = room[3] - 1
                rx2 = rx3 = rx
                ry2 = ry - 1
                ry3 = ry - 2
            elif rw == 1:  # East wall
                ry = choice(y_range) + room[3]
                rx = room[2] + room[1]
                rx2 = rx + 1
                rx3 = rx + 2
                ry2 = ry3 = ry
            elif rw == 2:  # South wall
                rx = choice(x_range) + room[2]
                ry = room[3] + room[0]
                rx2 = rx3 = rx
                ry2 = ry + 1
                ry3 = ry + 2
            elif rw == 3:  # West wall
                ry = choice(y_range) + room[3]
                rx = room[2] - 1
                rx2 = rx - 1
                rx3 = rx + 2
                ry2 = ry3 = ry
            if (rx2 < self.size_x and
                ry2 < self.size_y and
                rx3 < self.size_x and
                ry3 < self.size_y and
                1 < ry < self.size_y - 3 and
                1 < rx < self.size_x - 3 and
                self.mapArr[ry][rx] == 2):  # If space is a wall, exit)
                found = True
                break
            else:
                if rw in [0, 2]:
                    x_range.pop(x_range.index((rx - room[2])))
                    if not x_range:
                        rw_range.pop(rw_range.index(0))
                        rw_range.pop(rw_range.index(2))
                if rw in [1, 3]:
                    y_range.pop(y_range.index((ry - room[3])))
                    if not y_range:
                        rw_range.pop(rw_range.index(1))
                        rw_range.pop(rw_range.index(3))
        if not found:
            print(room)
            print("delete room index:{}".format(rn))
                
        return rx, ry, rx2, ry2, rw

    def makePortal(self, px, py):
        """Create doors in walls"""
        ptype = randrange(30)
        if ptype > 90:  # Secret door
            self.mapArr[py][px] = 5
            return
        elif ptype > 75:  # Closed door
            self.mapArr[py][px] = 4
            return
        elif ptype > 40:  # Open door
            self.mapArr[py][px] = 3
            return
        else:  # Hole in the wall
            self.mapArr[py][px] = 0

    def joinCorridor(self, cno, xp, yp, ed, psb):
        """Check corridor endpoint and make an exit if it links to another room"""
        cArea = self.roomList[cno]
        if xp != cArea[2] or yp != cArea[3]:  # Find the corridor endpoint
            endx = xp - (cArea[1] - 1)
            endy = yp - (cArea[0] - 1)
        else:
            endx = xp + (cArea[1] - 1)
            endy = yp + (cArea[0] - 1)
        checkExit = []
        if ed == 0:  # North corridor
            if endx > 1:
                coords = [endx - 2, endy, endx - 1, endy]
                checkExit.append(coords)
            if endy > 1:
                coords = [endx, endy - 2, endx, endy - 1]
                checkExit.append(coords)
            if endx < self.size_x - 2:
                coords = [endx + 2, endy, endx + 1, endy]
                checkExit.append(coords)
        elif ed == 1:  # East corridor
            if endy > 1:
                coords = [endx, endy - 2, endx, endy - 1]
                checkExit.append(coords)
            if endx < self.size_x - 2:
                coords = [endx + 2, endy, endx + 1, endy]
                checkExit.append(coords)
            if endy < self.size_y - 2:
                coords = [endx, endy + 2, endx, endy + 1]
                checkExit.append(coords)
        elif ed == 2:  # South corridor
            if endx < self.size_x - 2:
                coords = [endx + 2, endy, endx + 1, endy]
                checkExit.append(coords)
            if endy < self.size_y - 2:
                coords = [endx, endy + 2, endx, endy + 1]
                checkExit.append(coords)
            if endx > 1:
                coords = [endx - 2, endy, endx - 1, endy]
                checkExit.append(coords)
        elif ed == 3:  # West corridor
            if endx > 1:
                coords = [endx - 2, endy, endx - 1, endy]
                checkExit.append(coords)
            if endy > 1:
                coords = [endx, endy - 2, endx, endy - 1]
                checkExit.append(coords)
            if endy < self.size_y - 2:
                coords = [endx, endy + 2, endx, endy + 1]
                checkExit.append(coords)
        for xxx, yyy, xxx1, yyy1 in checkExit:  # Loop through possible exits
            if self.mapArr[yyy][xxx] == 0:  # If joins to a room
                if randrange(100) < psb:  # Possibility of linking rooms
                    self.makePortal(xxx1, yyy1)

    def finalJoins(self):
        """Final stage, loops through all the corridors to see if any can be joined to other rooms"""
        for x in self.cList:
            self.joinCorridor(x[0], x[1], x[2], x[3], 100)

    def printt(self):
        for y in range(self.size_y):
            line = ""
            line2 = ""
            for x in range(self.size_x):
                if self.mapArr[y][x] == 0:
                    line += " "
                    line2 += "0"
                if self.mapArr[y][x] == 1:
                    line += "#"
                    line2 += "1"
                if self.mapArr[y][x] == 2:
                    line += "#"
                    line2 += "2"
                if self.mapArr[y][x] in [3,4,5,8]:
                    line += " "
                    line2 += str(self.mapArr[y][x])
            print(line, line2)
# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    startx = 50   # map width
    starty = 50   # map height
    themap = Maze()
    themap.makeMap(startx, starty, 100, 10, 30)
    themap.printt()
