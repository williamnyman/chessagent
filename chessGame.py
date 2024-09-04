#import chessVisuals
import pygame
from chessChessboard import ChessBoard
from chessPlayer import Player
from chessPieces import Pawn, Rook, Knight, Bishop, Queen, King
from chessColors import black
from chessUtility import square_size, pieceImages, xyz

class ChessGame:
    def __init__(self):
        self.gameboard = ChessBoard()
        self.playerblack = Player('black')
        self.playerwhite = Player('white')
        self.ticker = 0
        self.victor = None
        self.victory = 0

    def startGame(self):
        '''victory = False 
        while not self.checkVictory():
            #print("about to do game turn")
            self.gameTurn()
        print(f"{self.checkVictory().color} player wins!")'''

        while not self.victory:
            #print("about to do game turn")
            self.gameTurn()
            if self.checkVictory():
                self.victory = True 
        print(f"{self.checkVictory().color} player wins!")
        
    def gameTurn(self):

        if self.ticker % 2 == 0:
            #print(f"White in check: {self.gameboard.checkCheck(self.playerwhite, self.playerblack)}")
            if self.gameboard.checkCheck(self.playerwhite, self.playerblack):
                self.playerwhite.change_square_color(self.playerwhite.getKingLocation(), (255,0,0))
                rect = pygame.Rect((self.playerwhite.getKingLocation()[0]*square_size), (self.playerwhite.getKingLocation()[1]*square_size), square_size, square_size)
                pygame.draw.rect(xyz, black, rect, 1)
                xyz.blit(pieceImages['K'], pygame.Rect((self.playerwhite.getKingLocation()[1]*100) + 5, (self.playerwhite.getKingLocation()[0]*100) + 5, 100, 100))

            pygame.display.flip()

            self.playerwhite.populate_pieces(self.gameboard)
            selected_piece, chosen_move = self.playerwhite.chooseMove(self.gameboard)
            self.gameboard.applyMove(chosen_move, self.playerwhite, selected_piece)

        else:
            #print(f"Black in check: {self.gameboard.checkCheck(self.playerblack, self.playerwhite)}")
            if self.gameboard.checkCheck(self.playerblack, self.playerwhite):
                self.playerblack.change_square_color(self.playerblack.getKingLocation(), (255,0,0))
                rect = pygame.Rect((self.playerblack.getKingLocation()[0]*square_size), (self.playerwhite.getKingLocation()[1]*square_size), square_size, square_size)
                pygame.draw.rect(xyz, black, rect, 1)
                xyz.blit(pieceImages['k'], pygame.Rect((self.playerblack.getKingLocation()[1]*100) + 5, (self.playerblack.getKingLocation()[0]*100) + 5, 100, 100))

            pygame.display.flip()

            self.playerblack.populate_pieces(self.gameboard)
            selected_piece, chosen_move = self.playerblack.chooseMove(self.gameboard)
            self.gameboard.applyMove(chosen_move, self.playerblack, selected_piece)

        self.ticker += 1

    def checkVictory(self):
        #return self.gameboard.boardVictory(self.playerwhite, self.playerblack)
        #pygame.time.wait(2000)
        if self.ticker >= 2:
            if self.ticker % 2 == 0:
                playerTurn = self.playerwhite
                playerNotTurn = self.playerblack
            else:
                playerTurn = self.playerblack
                playerNotTurn = self.playerwhite

            if self.gameboard.checkCheck(playerTurn, playerNotTurn):
                has_legal_moves = False
                for piece in playerTurn.pieces:
                    if piece.legal_moves_val(self.gameboard):
                        has_legal_moves = True
                        break

                if not has_legal_moves:
                    return playerNotTurn
        
            return None

