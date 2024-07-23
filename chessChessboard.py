#import chessVisuals
import pygame
from chessColors import lightgray, white

from chessPieces import Pawn, Rook, Knight, Bishop, Queen, King
from chessPlayer import Player

'''
pieceImages = {
    'P': pygame.image.load('chessImages/wpawn.png'),
    'p': pygame.image.load('chessImages/bpawn.png'),
    'R': pygame.image.load('chessImages/wrook.png'),
    'r': pygame.image.load('chessImages/brook.png'),
    'N': pygame.image.load('chessImages/wknight.png'),
    'n': pygame.image.load('chessImages/bknight.png'),
    'B': pygame.image.load('chessImages/wbishop.png'),
    'b': pygame.image.load('chessImages/bbishop.png'),
    'Q': pygame.image.load('chessImages/wqueen.png'),
    'q': pygame.image.load('chessImages/bqueen.png'),
    'K': pygame.image.load('chessImages/wking.png'),
    'k': pygame.image.load('chessImages/bking.png')
}

pieceImagesSmall = {
    'R': pygame.transform.scale(pygame.image.load('chessImages/wrook.png'), (50, 50)),
    'r': pygame.transform.scale(pygame.image.load('chessImages/brook.png'), (50, 50)),
    'N': pygame.transform.scale(pygame.image.load('chessImages/wknight.png'), (50, 50)),
    'n': pygame.transform.scale(pygame.image.load('chessImages/bknight.png'), (50, 50)),
    'B': pygame.transform.scale(pygame.image.load('chessImages/wbishop.png'), (50, 50)),
    'b': pygame.transform.scale(pygame.image.load('chessImages/bbishop.png'), (50, 50)),
    'Q': pygame.transform.scale(pygame.image.load('chessImages/wqueen.png'), (50, 50)),
    'q': pygame.transform.scale(pygame.image.load('chessImages/bqueen.png'), (50, 50))
}
'''


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

    def applyMove(self, move, moving_player, moving_piece, gameWindow):
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
            self.promote_pawn(x, y, moving_player, moving_piece, gameWindow) 

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
    
    def promote_pawn(self, x, y, moving_player, moving_piece, gameWindow):
        potential_pieces_w = [('R',(0, 0)), ('B', (50, 0)), ('N', (0, 50)), ('Q', (50, 50))]
        potential_pieces_b = [('r',(0, 0)), ('b', (50, 0)), ('n', (0, 50)), ('q', (50, 50))]
        colors = [white, lightgray]
        if moving_player.color == "white":
            moving_player.change_square_color(gameWindow, (x, y), colors[y % 2])
            for i, start in potential_pieces_w:
                gameWindow.blit(pieceImagesSmall[i], pygame.Rect((y*100) + start[1], (x*100) + start[0], 50, 50))
        else:
            moving_player.change_square_color(gameWindow, (x, y), colors[y % 2])
            for i, start in potential_pieces_b:
                gameWindow.blit(pieceImagesSmall[i], pygame.Rect((y*100) + start[1], (x*100) + start[0], 50, 50))

        pygame.display.flip()

        promote_selection = None
        while not promote_selection:
            #pygame.time.wait(100)
            #print("MADE IT TO start of select piece")
            for event in pygame.event.get():
                #print(f"FIRST LINE IN FOR LOOP event : {event}")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #print("PAST IF mouse down STATEMENT")
                    pos = pygame.mouse.get_pos()
                    col = pos[0] # -1?
                    row = pos[1] # -1?
                    print(f"Clicked on  {col}, {row}")
                    print("JUST GOT MOUSE POS")
                    #pygame.time.wait(1500)

                    if y * 100 < col and col < y * 100 + 50:
                        if x * 100 < row and row < x * 100 + 50:
                            promote_selection = "rook"
                        elif x*100 + 50 < row and row < x*100 + 100:
                            promote_selection = "bishop"
                    elif y * 100 + 50 < col and col < y * 100 + 100: # 2 or 4
                        if x*100 < row and row < x*100 + 50:
                            promote_selection = "knight"
                        elif x*100 + 50 < row and row < x*100 + 100:
                            promote_selection = "queen"
                    else:
                        print("looping again")
                        pygame.event.clear()
        if promote_selection == 'queen':
            self.board[x][y] = Queen(moving_player.color, x, y)
        if promote_selection == 'rook':
            self.board[x][y] = Rook(moving_player.color, x, y)
        if promote_selection == 'knight':
            self.board[x][y] = Knight(moving_player.color, x, y)
        if promote_selection == 'bishop':
            self.board[x][y] = Bishop(moving_player.color, x, y)
                        

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