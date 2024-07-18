#import chessVisuals
import pygame

from chessPieces import Pawn, Rook, Knight, Bishop, Queen, King
from chessPlayer import Player

class ChessBoard:
    def __init__(self):
        # Initialize an 8x8 chess board with None values
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.setup_board()

    def setup_board(self):
        # Initialize pieces on the board
        for i in range(8):
            self.board[1][i] = Pawn('black',1,i)  # Place black pawns on the second row
            self.board[6][i] = Pawn('white',6,i)  # Place white pawns on the seventh row

        # List defining the placement of major pieces
        placement = [
            Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook
        ]

        # Place major pieces on the first and last rows
        for i, piece in enumerate(placement):
            self.board[0][i] = piece('black',0,i)  # Place black pieces on the first row
            self.board[7][i] = piece('white',7,i)  # Place white pieces on the last row

    def retrievePieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece and piece.color == color:
                    pieces.append(piece)
        return pieces

    def applyMove(self, move, moving_player, moving_piece):
        print("start of apply move")
        if "castle" in move:
            self.applyCastle(move, moving_piece)
            return 0

        #update moved pieces self.x and y coords
        x, y = move
    
        #if piece captured then add to captured pieces of moving player
        if self.board[x][y]:
            moving_player.addToCaptured(self.board[x][y])
            
        #make moved-to location new piece and moved-from location None
        self.board[x][y] = moving_piece
        self.board[moving_piece.getX()][moving_piece.getY()] = None

        moving_piece.updatePosition(x, y)

        if (moving_piece.__str__() == 'P' and move[0] == 0) or (moving_piece.__str__() == 'p' and move[0] == 7):
            promote_input = input("q/r/n/b")
            if promote_input == 'q':
                self.board[x][y] = Queen(moving_player.color, x, y)
            if promote_input == 'r':
                self.board[x][y] = Rook(moving_player.color, x, y)
            if promote_input == 'n':
                self.board[x][y] = Knight(moving_player.color, x, y)
            if promote_input == 'b':
                self.board[x][y] = Bishop(moving_player.color, x, y)

                
        '''    #self.board[moving_piece.getX()][moving_piece.getY()] = 
        if moving_piece.__str__() == 'p' and move[0] == 7:
            print("BPawn has made it to back rank")'''

        if moving_piece.__str__() == 'k' or moving_piece.__str__() == 'K' or moving_piece.__str__() == 'R' or moving_piece.__str__() == 'r':
            moving_piece.update_has_moved(True)

    def applyCastle(self, move, moving_piece):
        if move == "castleR": #((moving_piece.getX(), 6))
            self.board[moving_piece.getX()][6] = self.board[moving_piece.getX()][4]
            self.board[moving_piece.getX()][6].updatePosition(moving_piece.getX(),6)
            self.board[moving_piece.getX()][4] = None

            self.board[moving_piece.getX()][5] = self.board[moving_piece.getX()][7]
            self.board[moving_piece.getX()][5].updatePosition(moving_piece.getX(), 5)
            self.board[moving_piece.getX()][7] = None
        else:
            self.board[moving_piece.getX()][2] = self.board[moving_piece.getX()][4]
            self.board[moving_piece.getX()][2].updatePosition(moving_piece.getX(), 2)
            self.board[moving_piece.getX()][4] = None

            self.board[moving_piece.getX()][3] = self.board[moving_piece.getX()][0]
            self.board[moving_piece.getX()][3].updatePosition(moving_piece.getX(), 3)
            self.board[moving_piece.getX()][0] = None

    def boardVictory(self, playerw, playerb):
        for i in playerw.captured_pieces:
            if i.__str__() == 'k':
                return playerw
        for j in playerb.captured_pieces:
            if j.__str__() == 'K':
                return playerb
        return None
    

    def display(self):
        # Display the board
        for row in self.board:
            print(" ".join([str(piece) if piece else '.' for piece in row]))
        print()
