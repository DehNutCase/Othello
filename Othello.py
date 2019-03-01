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
