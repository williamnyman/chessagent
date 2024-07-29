#import chessVisuals
import pygame
from chessChessboard import ChessBoard
from chessPlayer import Player
from chessPieces import Pawn, Rook, Knight, Bishop, Queen, King
from chessColors import black
from chessUtility import square_size, pieceImages

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
            print(f"White in check: {self.gameboard.checkCheck(self.playerwhite, self.playerblack)}")
            if self.gameboard.checkCheck(self.playerwhite, self.playerblack):
                self.playerwhite.change_square_color(gameWindow, self.playerwhite.getKingLocation(), (255,0,0))
                rect = pygame.Rect((self.playerwhite.getKingLocation()[0]*square_size), (self.playerwhite.getKingLocation()[1]*square_size), square_size, square_size)
                pygame.draw.rect(gameWindow, black, rect, 1)
                gameWindow.blit(pieceImages['K'], pygame.Rect((self.playerwhite.getKingLocation()[1]*100) + 5, (self.playerwhite.getKingLocation()[0]*100) + 5, 100, 100))

            pygame.display.flip()

            self.playerwhite.populate_pieces(self.gameboard)
            #print("MADE IT PAST populate_pieces")
            selected_piece, chosen_move = self.playerwhite.chooseMove(self.gameboard, gameWindow)
            #print("MADE IT PAST selecting piece and chosen move")
            self.gameboard.applyMove(chosen_move, self.playerwhite, selected_piece, gameWindow)
            #print("MADE IT PAST applyMove")

        else:
            print(f"Black in check: {self.gameboard.checkCheck(self.playerblack, self.playerwhite)}")
            if self.gameboard.checkCheck(self.playerblack, self.playerwhite):
                self.playerblack.change_square_color(gameWindow, self.playerblack.getKingLocation(), (255,0,0))
                rect = pygame.Rect((self.playerblack.getKingLocation()[0]*square_size), (self.playerwhite.getKingLocation()[1]*square_size), square_size, square_size)
                pygame.draw.rect(gameWindow, black, rect, 1)
                gameWindow.blit(pieceImages['k'], pygame.Rect((self.playerblack.getKingLocation()[1]*100) + 5, (self.playerblack.getKingLocation()[0]*100) + 5, 100, 100))

            pygame.display.flip()

            self.playerblack.populate_pieces(self.gameboard)
            selected_piece, chosen_move = self.playerblack.chooseMove(self.gameboard, gameWindow)
            self.gameboard.applyMove(chosen_move, self.playerblack, selected_piece, gameWindow)

        self.ticker += 1

    def checkVictory(self):
        return self.gameboard.boardVictory(self.playerwhite, self.playerblack)