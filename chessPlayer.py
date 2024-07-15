#import chessVisuals
from pynput.mouse import Controller
import pygame
from chessPieces import Pawn, Rook, Knight, Bishop, Queen, King

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
        print("MADE IT TO start of select piece")
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                col = pos[0] // 100
                row = pos[1] // 100
                print(f"Clicked on column {col}, row {row}")
                print("JUST GOT MOUSE POS")
                pygame.time.wait(1500)
                
                if chessboard.board[row][col] in self.pieces:
                    print(f"selected {chessboard.board[row][col]}")
                    return chessboard.board[row][col]
                else:
                    print("looping again")
                    return self.selectPiece(chessboard)
    
    def chooseMove(self, chessboard):
        print("MADE IT TO start of chooseMove func")
        currPiece = self.selectPiece(chessboard)
        currMoves = currPiece.legal_moves(chessboard)

        for i in currMoves:
            print(i)
        selectedMove = currMoves[int(input("Which move would you like to make (enter index starting at 0 of move)"))]
        return currPiece, selectedMove
    
    def addToCaptured(self, p):
        self.captured_pieces.append(p)
