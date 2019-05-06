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
    """New Comments: Creating a 'Board' object has it initialize a 2d list called 'tiles' to keep track
       of whether a given tile is empty, filled with a black piece, or filled with a white piece.
       
       The size of the board is based on the two points you pass into it when initializing the board object."""
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
        self.turn = 'black'

    def clear_board(self):
        """New Comments: This method sets all tiles in the board to 'empty' and then places 2 white and 2 black tiles in the middle 4 squares to start a 
           new game of Othello."""
        for i in range(8):
            for j in range(8):
                self.tiles[i][j] = 'empty'


        self.tiles[3][3] = 'white'
        self.tiles[4][3] = 'black'
        self.tiles[3][4] = 'black'
        self.tiles[4][4] = 'white'

    def draw_grid(self):
        """New Comments: Draw grid is a helper method that does nothing except drawing an 8 by 8 gameboard (used when initializing the 'board' object)."""
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
        """New Comments: A helper method that determines whether a given combination of x and y coordinates is on the gameboard."""
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
            if self.is_on_board(temp_x,temp_y) and self.tiles[temp_x][temp_y] == 'white':
                temp_x += dx
                temp_y += dy
                if not self.is_on_board(temp_x,temp_y):
                    continue
                while self.tiles[temp_x][temp_y] == 'white':
                    temp_x += dx
                    temp_y += dy
                    if not self.is_on_board(temp_x,temp_y):
                        break
                if not self.is_on_board(temp_x, temp_y):
                    continue
                if self.tiles[temp_x][temp_y] == 'black':
                    while True:
                        temp_x -= dx
                        temp_y -= dy
                        if temp_x == x and temp_y == y:
                            break
                        to_flip.append([temp_x, temp_y])
        if not to_flip:
            return

        self.tiles[x][y] = 'black'
        self.turn = 'white'
        for x,y in to_flip:
            self.tiles[x][y] = 'black'
        update_tiles()
        return

    def place_white(self, x, y):
        """New comments: Same thing as 'place_black' execept it places white pieces instead."""
        if not self.is_on_board(x,y) or gameboard.tiles[x][y] != 'empty':
            return
        to_flip = []
        for dx, dy in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            temp_x, temp_y = x, y
            temp_x += dx
            temp_y += dy
            if self.is_on_board(temp_x,temp_y) and self.tiles[temp_x][temp_y] == 'black':
                temp_x += dx
                temp_y += dy
                if not self.is_on_board(temp_x,temp_y):
                    continue
                while self.tiles[temp_x][temp_y] == 'black':
                    temp_x += dx
                    temp_y += dy
                    if not self.is_on_board(temp_x,temp_y):
                        break
                if not self.is_on_board(temp_x, temp_y):
                    continue
                if self.tiles[temp_x][temp_y] == 'white':
                    while True:
                        temp_x -= dx
                        temp_y -= dy
                        if temp_x == x and temp_y == y:
                            break
                        to_flip.append([temp_x, temp_y])
        if not to_flip:
            return

        self.tiles[x][y] = 'white'
        self.turn = 'black'
        for x,y in to_flip:
            self.tiles[x][y] = 'white'
        update_tiles()
        return

    def black_moves(self):
        """New comment: Helper method that tests whether or not black has a legal move."""
        legal_moves = []
        for x in range(8):
            for y in range(8):
                if gameboard.tiles[x][y] != 'empty':
                    continue
                to_flip = []
                for dx, dy in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
                    temp_x, temp_y = x, y
                    temp_x += dx
                    temp_y += dy
                    if self.is_on_board(temp_x,temp_y) and self.tiles[temp_x][temp_y] == 'white':
                        temp_x += dx
                        temp_y += dy
                        if not self.is_on_board(temp_x,temp_y):
                            continue
                        while self.tiles[temp_x][temp_y] == 'white':
                            temp_x += dx
                            temp_y += dy
                            if not self.is_on_board(temp_x,temp_y):
                                break
                        if not self.is_on_board(temp_x, temp_y):
                            continue
                        if self.tiles[temp_x][temp_y] == 'black':
                            while True:
                                temp_x -= dx
                                temp_y -= dy
                                if temp_x == x and temp_y == y:
                                    break
                                to_flip.append([temp_x, temp_y])
                if to_flip:
                    legal_moves.append([x,y])
        return legal_moves

    def white_moves(self):
        """New comment: Helper method that tests whether or not white has a legal move."""
        legal_moves = []
        for x in range(8):
            for y in range(8):
                if gameboard.tiles[x][y] != 'empty':
                    continue
                to_flip = []
                for dx, dy in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
                    temp_x, temp_y = x, y
                    temp_x += dx
                    temp_y += dy
                    if self.is_on_board(temp_x,temp_y) and self.tiles[temp_x][temp_y] == 'black':
                        temp_x += dx
                        temp_y += dy
                        if not self.is_on_board(temp_x,temp_y):
                            continue
                        while self.tiles[temp_x][temp_y] == 'black':
                            temp_x += dx
                            temp_y += dy
                            if not self.is_on_board(temp_x,temp_y):
                                break
                        if not self.is_on_board(temp_x, temp_y):
                            continue
                        if self.tiles[temp_x][temp_y] == 'white':
                            while True:
                                temp_x -= dx
                                temp_y -= dy
                                if temp_x == x and temp_y == y:
                                    break
                                to_flip.append([temp_x, temp_y])
                if to_flip:
                    legal_moves.append([x,y])
        return legal_moves

    def get_score(self):
        """New comment: Helper method that counts up all the tiles on the board to see how many have black pieces on them and how many have white."""
        black = 0
        white = 0
        for x in range(8):
            for y in range(8):
                if gameboard.tiles[x][y] == 'black':
                    black += 1
                if gameboard.tiles[x][y] == 'white':
                    white += 1
        return [black, white]
                    
    def game_over(self):
        """New comment: Helper method that opens a box informing the player the game is over and also the scores of each player---starts a new game if you click twice after the box appears."""
        game_over_screen = graphics.Rectangle(graphics.Point(100,200), graphics.Point(700,600))
        game_over_screen.setFill('black')
        game_over_screen.draw(screen)

        game_over_text = graphics.Text(graphics.Point(400,300), 'Game Over! (Click Twice To Rematch)')
        game_over_text.setTextColor('white')
        game_over_text.setSize(24)
        game_over_text.draw(screen)

        white_score = graphics.Text(graphics.Point(250,400), 'White: ' + str(gameboard.get_score()[1]))
        white_score.setTextColor('white')
        white_score.setSize(24)
        white_score.draw(screen)

        black_score = graphics.Text(graphics.Point(550,400), 'Black: ' + str(gameboard.get_score()[0]))
        black_score.setTextColor('white')
        black_score.setSize(24)
        black_score.draw(screen)

        screen.getMouse()
        screen.getMouse()

        game_over_screen.undraw()
        game_over_text.undraw()
        white_score.undraw()
        black_score.undraw()
        self.clear_board()
        update_tiles()
        

        
                



gameboard = Board(graphics.Point(80,720), graphics.Point(720,80))

#creates a 2D list of every single tile
"""New comment: This basically creates a bunch of objects that don't have names, but you can still access them by calling their location in the this.
   Very handy if you need to make a large number of objects. (Since you can either use a list initalization like I did or even a for loop."""
tiles = [[graphics.Circle(graphics.Point(80 * (i + 1) + 40, 80 * (j + 1) + 40), 25) for j in range(8)] for i in range(8)]

def update_tiles():
    """New Comment: This is a function rather than a method, which is extremely stupid---never do this in a serious program, either everything should be functions,
       which isn't recommended for something like this, or all helper functions/methods should be helper methods. This function ONLY works if the gameboard is named 'gameboard,' and 
       you have to remember that it's not a helper method whenever you call it.
       
       What it does is that every time you call it it checks the state of the board and places white pieces on tiles that are white, places black pieces on tiles that are blaw, and undraws,
       that is, removes any piece currently on the tile, if the tile is supposed to be empty."""
    for i in range(8):
        for j in range(8):
            if not tiles[i][j].canvas:
                if gameboard.tiles[i][j] == 'white':
                    tiles[i][j].setWidth(2)
                    tiles[i][j].setFill('white')
                    tiles[i][j].draw(screen)
                if gameboard.tiles[i][j] == 'black':
                    tiles[i][j].setWidth(2)
                    tiles[i][j].setFill('black')
                    tiles[i][j].draw(screen)
            else:
                if gameboard.tiles[i][j] == 'white':
                    tiles[i][j].setFill('white')
                    tiles[i][j].setWidth(2)
                if gameboard.tiles[i][j] == 'black':
                    tiles[i][j].setWidth(2)
                    tiles[i][j].setFill('black')
            if gameboard.tiles[i][j] == 'empty':
                tiles[i][j].undraw()
update_tiles()


while True:
    """New Comment: This is the code that actually runs the game, so to speak. Since all the complicated coding is already done, all it doesn it take mouse inputs, and either places a new tile if the move is allowed
       before trying to pass the turn (if the other person doesn't have a valid move, their turn is skipped), or not placing a tile if it's an illegal move and doesn't try to pass the turn. If the game is over it runs
       the game over helper method which displays the score and restart the game if you click twice."""
    click = screen.getMouse()
    if gameboard.turn == 'black':
        if not gameboard.black_moves():
            gameboard.game_over()
        gameboard.place_black(int(click.x/80 - 1), int(click.y/80 - 1))
        if not gameboard.white_moves():
            gameboard.turn = 'black'
            print 'another black turn'
        
        
    if gameboard.turn == 'white':
        if not gameboard.white_moves():
            gameboard.game_over()
        gameboard.place_white(int(click.x/80 - 1), int(click.y/80 - 1))
        if not gameboard.black_moves():
            gameboard.turn = 'white'
            print 'another white turn'

        

