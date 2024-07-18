#import chessVisuals
import pygame
import random
from chessPieces import Pawn, Rook, Knight, Bishop, Queen, King
from chessColors import white, black, blue, lightblue, lightgray

# Load images
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

# Define a function to draw pieces
def draw_pieces(gameWindow, chessboard):
    for row in range(8):
        for col in range(8):
            piece = chessboard.board[row][col]
            if piece:
                pieceCode = chessboard.board[row][col].__str__()
                gameWindow.blit(pieceImages[pieceCode], pygame.Rect((col*100) + 5, (row*100) + 5, 100, 100))

class Player:
    def __init__(self, color):
        self.color = color
        self.pieces = []
        self.captured_pieces = []

    def takeTurn(self, chessboard):
        self.selectPiece()
        self.chooseMove(chessboard)

    def populate_pieces(self, chessboard):
        self.pieces = chessboard.retrievePieces(self.color)

    def selectPiece(self, chessboard):
        while True:
            #pygame.time.wait(100)
            #print("MADE IT TO start of select piece")
            for event in pygame.event.get():
                #print(f"FIRST LINE IN FOR LOOP event : {event}")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #print("PAST IF mouse down STATEMENT")
                    pos = pygame.mouse.get_pos()
                    col = (pos[0] // 100) # -1?
                    row = (pos[1] // 100) # -1?
                    print(f"Clicked on column {col}, row {row}")
                    print("JUST GOT MOUSE POS")
                    #pygame.time.wait(1500)
                    
                    if chessboard.board[row][col] in self.pieces:
                        print(f"selected {chessboard.board[row][col]}")
                        pygame.event.clear()
                        return chessboard.board[row][col]
                    else:
                        print("looping again")
                        pygame.event.clear()
                        return self.selectPiece(chessboard)
                    
    def change_sqaure_color(self, gameWindow, coord, hue):
        if coord == "castleR":
            if self.color == "white":
                x, y = (7, 6)
            else:
                x, y = (0, 6)
        elif coord == "castleL":
            if self.color == "white":
                x, y = (7, 2)
            else:
                x, y = (0, 2)
        else:
            x, y = coord
        rect = pygame.Rect(y*100, x*100, 100, 100)
        pygame.draw.rect(gameWindow, hue, rect)
    
    def chooseMove(self, chessboard, gameWindow):
        print("MADE IT TO start of chooseMove func")
        currPiece = self.selectPiece(chessboard)
        currMoves = currPiece.legal_moves(chessboard)

        print(currMoves)

        if not currMoves:
            currPiece = None
            return self.chooseMove(chessboard, gameWindow)
        
        for i in currMoves:
            print(f"Changing color of {i}")
            if i == "castleR":
                row, col = currPiece.getX(), 6
            elif i == "castleL":
                row, col = currPiece.getX(), 2
            else:
                row, col = i
            self.change_sqaure_color(gameWindow, i, blue)
            rect = pygame.Rect(col*100, row*100, 100, 100)
            pygame.draw.rect(gameWindow, black, rect, 1)
        draw_pieces(gameWindow, chessboard)

        pygame.display.flip()

        while True:
            pygame.time.wait(100)
            #print("MADE IT TO start of selecting move")
            for event in pygame.event.get():
                #print(f"FIRST LINE IN FOR LOOP event : {event}")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print("PAST IF mouse down STATEMENT")
                    pos = pygame.mouse.get_pos()
                    col = pos[0] // 100 # -1?
                    row = pos[1] // 100 # -1?
                    print(f"Clicked on column {col}, row {row}")
                    print("JUST GOT MOUSE POS")
                    #pygame.time.wait(1500)
                    
                    if (row, col) in currMoves or "castleR" in currMoves or "castleL" in currMoves:
                        if (row, col) == (currPiece.getX(), 6) and "castleR" in currMoves:
                            print(f"selected {'castleR'}")
                            return currPiece, "castleR"
                        elif (row, col) == (currPiece.getX(), 2) and "castleL" in currMoves:
                            print(f"selected {'castleL'}")
                            return currPiece, "castleL"
                        else:
                            pygame.event.clear()
                            return currPiece, (row, col)
                        
                    #clicked on current piece should take back to piece selection
                    elif (row, col) == (currPiece.getX(), currPiece.getY()):
                        for i in currMoves:
                            x, y = i
                            print(f"Changing color of {i}")
                            if (x + y) % 2 == 0:
                                self.change_sqaure_color(gameWindow, i, white)
                            else:
                                self.change_sqaure_color(gameWindow, i, lightgray)

                        for i in range(8):
                            for j in range(8):
                                rect = pygame.Rect(i*100, j*100, 100, 100)
                                pygame.draw.rect(gameWindow, black, rect, 1)
                        draw_pieces(gameWindow, chessboard)


                        pygame.display.flip()

                        currPiece = None
                        return self.chooseMove(chessboard, gameWindow)

                    #clicked on nothing important should stay at move selection
                    print("looping again")
    
    def addToCaptured(self, p):
        self.captured_pieces.append(p)
