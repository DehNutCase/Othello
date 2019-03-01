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
        

    def clear_board(self):
        for i in range(8):
            for j in range(8):
                self.tiles[i][j] = 'empty'

        self.tiles[3][3] = 'white'
        self.tiles[4][3] = 'black'
        self.tiles[3][4] = 'black'
        self.tiles[4][4] = 'white'


gameboard = Board(graphics.Point(80,720), graphics.Point(720,80))
gameboard.draw(screen)

for i in range(8):
    aLine = graphics.Line(graphics.Point((i+1)*80,720), graphics.Point((i+1)*80, 80))
    aLine.setWidth(4)
    aLine.setFill('black')
    aLine.draw(screen)
    aLine = graphics.Line(graphics.Point(80,(i+1)*80), graphics.Point(720,(i+1)*80))
    aLine.setWidth(4)
    aLine.setFill('black')
    aLine.draw(screen)
