#import chessVisuals
import pygame
import random
#from chessPieces import Pawn, Rook, Knight, Bishop, Queen, King
from chessColors import white, black, blue, lightblue, lightgray

from chessUtility import pieceImages, draw_pieces, xyz
               
class Player:
    def __init__(self, color):
        self.color = color
        self.pieces = []
        self.captured_pieces = []

    def takeTurn(self, chessboard):
        self.selectPiece()
        self.chooseMove(chessboard)

    def getKingLocation(self):
        for i in self.pieces:
            if i.__str__() in ('K', 'k'):
                #print(f"{i.__str__()} at {i.x, i.y}")
                return (i.x, i.y)
        
        #print("UH OH")

    def populate_pieces(self, chessboard):
        self.pieces = chessboard.retrievePieces(self.color)

    def make_random_move_choice(self, chessboard):
        potential_moves = []
        for i in self.pieces:
            for j in i.legal_moves(chessboard):
                potential_moves.append((i, j))

        return random.choice(potential_moves)

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
                    
    def change_square_color(self, coord, color):
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
        pygame.draw.rect(xyz, color, rect)

    
    def chooseMove(self, chessboard):
        return self.make_random_move_choice(chessboard)
        
        print("MADE IT TO start of chooseMove func")
        currPiece = self.selectPiece(chessboard)
        currMoves = currPiece.legal_moves_val(chessboard)
        print("currPiece and currMoves established")

        print(currMoves)

        if not currMoves:
            currPiece = None
            return self.chooseMove(chessboard)
        
        for i in currMoves:
            print(f"Changing color of {i}")
            if i == "castleR":
                row, col = currPiece.getX(), 6
            elif i == "castleL":
                row, col = currPiece.getX(), 2
            elif i == "epWL":
                row, col = currPiece.x - 1, currPiece.y - 1
            elif i == "epWR":
                row, col = currPiece.x - 1, currPiece.y + 1
            elif i == "epBL":
                row, col = currPiece.x + 1, currPiece.y - 1
            elif i == "epBR":
                row, col = currPiece.x + 1, currPiece.y + 1
            else:
                row, col = i
            self.change_square_color((row, col), blue)
            rect = pygame.Rect(col*100, row*100, 100, 100)
            pygame.draw.rect(xyz, black, rect, 1)
        draw_pieces(chessboard.board)

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
                    
                    if (row, col) in currMoves or "castleR" in currMoves or "castleL" in currMoves or "epWL" in currMoves or "epWR" in currMoves or "epBL" in currMoves or "epBR" in currMoves:
                        if (row, col) == (currPiece.getX(), 6) and "castleR" in currMoves:
                            print(f"selected {'castleR'}")
                            return currPiece, "castleR"
                        elif (row, col) == (currPiece.getX(), 2) and "castleL" in currMoves:
                            print(f"selected {'castleL'}")
                            return currPiece, "castleL"
                        elif (row, col) == (currPiece.x - 1, currPiece.y - 1) and "epWL" in currMoves:
                            return currPiece, "epWL"
                        elif (row, col) == (currPiece.x - 1, currPiece.y + 1) and "epWR" in currMoves:
                            return currPiece, "epWR"
                        elif (row, col) == (currPiece.x + 1, currPiece.y - 1) and "epBL" in currMoves:
                            return currPiece, "epBL"
                        elif (row, col) == (currPiece.x + 1, currPiece.y + 1) and "epBR" in currMoves:
                            return currPiece, "epBR"
                        else:
                            pygame.event.clear()
                            return currPiece, (row, col)
                        
                    #clicked on current piece should take back to piece selection
                    elif (row, col) == (currPiece.getX(), currPiece.getY()):
                        for i in currMoves:
                            x, y = i
                            print(f"Changing color of {i}")
                            if (x + y) % 2 == 0:
                                self.change_square_color(i, white)
                            else:
                                self.change_square_color(i, lightgray)

                        for i in range(8):
                            for j in range(8):
                                rect = pygame.Rect(i*100, j*100, 100, 100)
                                pygame.draw.rect(xyz, black, rect, 1)
                        draw_pieces(chessboard.board)


                        pygame.display.flip()

                        currPiece = None
                        return self.chooseMove(chessboard)

                    #clicked on nothing important should stay at move selection
                    print("looping again")
        
                     
    def addToCaptured(self, p):
        self.captured_pieces.append(p)