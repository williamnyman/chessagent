#import chessVisuals
import pygame
import random
import copy
from chessColors import lightgray, white

from chessPieces import Piece, Pawn, Rook, Knight, Bishop, Queen, King
from chessPlayer import Player

from chessUtility import pieceImages, pieceImagesSmall, draw_board, draw_pieces, xyz


class ChessBoard:
    def __init__(self):
        # Initialize an 8x8 chess board with None values
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.setup_board()
        self.last_move = None

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
        if "ep" in move:
            self.applyep(move, moving_player, moving_piece)
            return 0

        move_initial = (moving_piece.x, moving_piece.y)
        self.last_move = (moving_piece, move_initial, move)

        if "castle" in move:
            self.applyCastle(move, moving_piece)
            return 0

        #update moved pieces self.x and y coords
        x, y = move
        #if self.board[x][y].__str__() in ('K', 'k'):
            # moving player wins
            # the only way a player should be able to capture the king is if the other player was in check and had no legal moves to be made
        #if piece captured then add to captured pieces of moving player
        #if self.board[x][y]:
            #moving_player.addToCaptured(self.board[x][y])

            
        #make moved-to location new piece and moved-from location None
        self.board[x][y] = moving_piece
        self.board[moving_piece.getX()][moving_piece.getY()] = None

        moving_piece.updatePosition(x, y)

        if (moving_piece.__str__() == 'P' and move[0] == 0) or (moving_piece.__str__() == 'p' and move[0] == 7):
            self.promote_pawn(x, y, moving_player, moving_piece) 

        if moving_piece.__str__() == 'k' or moving_piece.__str__() == 'K' or moving_piece.__str__() == 'R' or moving_piece.__str__() == 'r':
            moving_piece.update_has_moved(True)

    def apply_temp_move(self, move, moving_player, moving_piece):
        if "ep" in move:
            self.applyep(move, moving_player, moving_piece)
            return 0
        
        if "castle" in move:
            self.applyCastle(move, moving_piece)
            return 0
        
        x, y = move

        if self.board[x][y]:
            moving_player.addToCaptured(self.board[x][y])
            
        self.board[x][y] = moving_piece
        self.board[moving_piece.getX()][moving_piece.getY()] = None

        moving_piece.updatePosition(x, y)

    def applyCastle(self, move, moving_piece):
        #print(f"Applying castle or move {move} of piece {moving_piece.__str__()} done by player {moving_piece.color}")

        castleDict = {"castleR" : (6,4,5,7), "castleL" : (2,4,3,0)}

        self.board[moving_piece.getX()][castleDict[move][0]] = self.board[moving_piece.getX()][castleDict[move][1]]
        self.board[moving_piece.getX()][castleDict[move][0]].updatePosition(moving_piece.getX(),castleDict[move][0])
        self.board[moving_piece.getX()][castleDict[move][1]] = None

        self.board[moving_piece.getX()][castleDict[move][2]] = self.board[moving_piece.getX()][castleDict[move][3]]
        self.board[moving_piece.getX()][castleDict[move][2]].updatePosition(moving_piece.getX(), castleDict[move][2])
        self.board[moving_piece.getX()][castleDict[move][3]] = None
        
    def promote_pawn(self, x, y, moving_player, moving_piece):
        potential_pieces_w = [('R',(0, 0)), ('B', (50, 0)), ('N', (0, 50)), ('Q', (50, 50))]
        potential_pieces_b = [('r',(0, 0)), ('b', (50, 0)), ('n', (0, 50)), ('q', (50, 50))]

        draw_board(self.board)

        colors = [white, lightgray]
        if moving_player.color == "white":
            moving_player.change_square_color((x, y), colors[y % 2])
            for i, start in potential_pieces_w:
                xyz.blit(pieceImagesSmall[i], pygame.Rect((y*100) + start[1], (x*100) + start[0], 50, 50))
        else:
            moving_player.change_square_color((x, y), colors[y % 2])
            for i, start in potential_pieces_b:
                xyz.blit(pieceImagesSmall[i], pygame.Rect((y*100) + start[1], (x*100) + start[0], 50, 50))

        pygame.display.flip()
        promote_selection = None
        promote_selection = random.choice(('queen','rook','knight','bishop'))

        while not promote_selection:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    col = pos[0] # -1?
                    row = pos[1] # -1?
                    #print(f"Clicked on  {col}, {row}")
                    #print("JUST GOT MOUSE POS")
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
                        #print("looping again")
                        pygame.event.clear()

        promotion_dict = {'queen' : Queen(moving_player.color, x, y), 'rook' : Rook(moving_player.color, x, y), 'knight' : Knight(moving_player.color, x, y), 'bishop' : Bishop(moving_player.color, x, y)}
        self.board[x][y] = promotion_dict[promote_selection]
        #print("JUST DID A PROMOTION")
                        
    def applyep(self, move, moving_player, moving_piece):
        piece_getting_taken = self.last_move[0]

        ep_dict = {"epWL" : (-1, -1), "epWR" : (-1, 1), "epBL" : (1, -1), "epBR" : (1, 1)}
        addx, addy = ep_dict[move][0], ep_dict[move][1]

        self.board[moving_piece.x + addx][moving_piece.y + addy] = moving_piece
        self.board[moving_piece.x][moving_piece.y] = None
        moving_piece.updatePosition(moving_piece.x + addx, moving_piece.y + addy)

        self.board[piece_getting_taken.x][piece_getting_taken.y] = None
        moving_player.addToCaptured(piece_getting_taken)

    def boardVictory(self, playerw, playerb):
        for i in playerw.captured_pieces:
            if i.__str__() == 'k':
                return playerw
        for j in playerb.captured_pieces:
            if j.__str__() == 'K':
                return playerb
        return None
    
    def checkCheck(self, playerTurn, playerNotTurn):
        dummyboard = copy.deepcopy(self)
        playerTurn.populate_pieces(dummyboard)
        playerNotTurn.populate_pieces(dummyboard)

        #notTurnMoves = []
        for notTurnPiece in playerNotTurn.pieces:
            for notTurnMove in notTurnPiece.legal_moves(dummyboard):
                if notTurnMove == playerTurn.getKingLocation():
                    return True
        
        return False

    def display(self):
        # Display the board
        for row in self.board:
            print(" ".join([str(piece) if piece else '.' for piece in row]))
        print()