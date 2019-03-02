"""
Rules:

Gameboard is 8x8, with the center 4 tiles being taken up by 4 disks, 2 of each color, and same
colored disks being in diagonal with each other.

Players take alternating turns, black goes first, if a player has no legal moves, his turn is skipped.
If neither player has legal moves, the game ends, otherwise the game ends when the board is filled.

Pieces can only be placed where there exists at least one straight occupied line between the new piece
and another same colored pieces, with one or more contiguous different colored piece(s) between them.
After the piece is placed, the different colored cintiguous piece(s) lying on a straight line between the 
new piece and any old same colored pieces are flipped to the same color.

Scoring is based on the number of pieces on the board, 1 point per piece of your color.
"""

import graphics

"""First step is to create the gameboard. First idea to do so is to create 64 'tile' objects
which look like squares on the screen and contain information on whether they are 'black,' 'white,'
or 'empty.'"""

"""First idea seems rather infesible, instead trying to create a 'board' object which stores the information
of tiles inside a 2D array"""

"""Unfortunately, I had to move back to first idea in order to be able to remove pieces once they are no
longer needed. While storing data inside the board allows me to place pieces without issue, it doesn't
give me the ability to remove pieces from the board to free up memory."""


screen = graphics.GraphWin("Othello Python Game", 800, 800)
screen.update()

class Board(graphics.Rectangle):
    def __init__(self, p1, p2):
        graphics.Rectangle.__init__(self, p1, p2)
        self.tiles = [[]]
        for i in range(8):
            self.tiles.append([])
            for j in range(8):
                self.tiles[i].append('')

        self.clear_board()
        self.setFill('white')
        self.setOutline('black')
        self.setWidth(5)
        self.draw(screen)
        self.draw_grid()

    def clear_board(self):
        for i in range(8):
            for j in range(8):
                self.tiles[i][j] = 'empty'

        self.tiles[3][3] = 'white'
        self.tiles[4][3] = 'black'
        self.tiles[3][4] = 'black'
        self.tiles[4][4] = 'white'

    def draw_grid(self):
        for i in range(8):
            aLine = graphics.Line(graphics.Point((i+1)*80,720), graphics.Point((i+1)*80, 80))
            aLine.setWidth(4)
            aLine.setFill('black')
            aLine.draw(screen)
            
            aLine = graphics.Line(graphics.Point(80,(i+1)*80), graphics.Point(720,(i+1)*80))
            aLine.setWidth(4)
            aLine.setFill('black')
            aLine.draw(screen)

    def is_on_board(self, x, y):
        if x < 0 or x > 7 or y < 0 or y > 7:
            return False
        else:
            return True

    def place_black(self, x, y):
        """Place a black piece, if called on a legal location, first places a black piece on the location,
        then flips the white pieces lying on a straight line between that piece and another black piece
        before passing the turn. Does nothing otherwise."""
        
        if not self.is_on_board(x,y) or gameboard.tiles[x][y] != 'empty':
            return
        to_flip = []
        for dx, dy in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            temp_x, temp_y = x, y
            temp_x += dx
            temp_y += dy
            if self.is_on_board(temp_x,temp_y) and gameboard.tiles[temp_x][temp_y] == 'white':
                temp_x += dx
                temp_y += dy
                if not self.is_on_board(temp_x,temp_y):
                    continue
                while gameboard.tiles[temp_x][temp_y] == 'white':
                    temp_x += dx
                    temp_y += dy
                    if not self.is_on_board(temp_x,temp_y):
                        break
                if not self.is_on_board(temp_x, temp_y):
                    continue
                if gameboard.tiles[temp_x][temp_y] == 'black':
                    while True:
                        temp_x -= dx
                        temp_y -= dy
                        if temp_x == x and temp_y == y:
                            break
                        to_flip.append([temp_x, temp_y])
        if not to_flip:
            return

        gameboard.tiles[x][y] = 'black'
        for x,y in to_flip:
            gameboard.tiles[x][y] = 'black'
        update_tiles()
        return
                    



gameboard = Board(graphics.Point(80,720), graphics.Point(720,80))

#creates a 2D list of every single tile
tiles = [[graphics.Circle(graphics.Point(80 * (i + 1) + 40, 80 * (j + 1) + 40), 25) for j in range(8)] for i in range(8)]

def update_tiles():
    for i in range(8):
        for j in range(8):
            if not tiles[i][j].canvas:
                if gameboard.tiles[i][j] == 'white':
                    tiles[i][j].setWidth(2)
                    tiles[i][j].draw(screen)
                if gameboard.tiles[i][j] == 'black':
                    tiles[i][j].setWidth(2)
                    tiles[i][j].setFill('black')
                    tiles[i][j].draw(screen)
            else:
                if gameboard.tiles[i][j] == 'white':
                    tiles[i][j].setWidth(2)
                if gameboard.tiles[i][j] == 'black':
                    tiles[i][j].setWidth(2)
                    tiles[i][j].setFill('black')
            if gameboard.tiles[i][j] == 'empty':
                tiles[i][j].undraw()


gameboard.place_black(3,2)
update_tiles()
