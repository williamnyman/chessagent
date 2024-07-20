#import chessVisuals
import pygame
from chessChessboard import ChessBoard
from chessPlayer import Player
from chessPieces import Pawn, Rook, Knight, Bishop, Queen, King

class ChessGame:
    def __init__(self):
        self.gameboard = ChessBoard()
        self.playerblack = Player('black')
        self.playerwhite = Player('white')
        self.ticker = 0
        self.victor = None

    def startGame(self):
        while not self.checkVictory():
            self.gameTurn()
        print(f"{self.checkVictory().color} player wins!")
        
    def gameTurn(self, gameWindow):

        if self.ticker % 2 == 0:
            self.playerwhite.populate_pieces(self.gameboard)
            print("MADE IT PAST populate_pieces")
            selected_piece, chosen_move = self.playerwhite.chooseMove(self.gameboard, gameWindow)
            print("MADE IT PAST selecting piece and chosen move")
            self.gameboard.applyMove(chosen_move, self.playerwhite, selected_piece, gameWindow)
            print("MADE IT PAST applyMove")

        else:
            self.playerblack.populate_pieces(self.gameboard)
            selected_piece, chosen_move = self.playerblack.chooseMove(self.gameboard, gameWindow)
            self.gameboard.applyMove(chosen_move, self.playerblack, selected_piece, gameWindow)

        self.ticker += 1

    def checkVictory(self):
        return self.gameboard.boardVictory(self.playerwhite, self.playerblack)