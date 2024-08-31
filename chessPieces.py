#import chessVisuals
import pygame
import copy
import chessPlayer

class Piece:
    #initialize piece and set color to passed in color (either black or white)
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y

    #returns all of the legal moves that piece can make
    def legal_moves(self, board):
        raise NotImplementedError("This method should be overridden in derived classes")
    
    def getX(self):
        return self.x
        
    def getY(self):
        return self.y
    
    def getColor(self):
        return self.color
    
    def updatePosition(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

    def validate_move(self, move, chessboard):
        print(f"ATTEMPTING TO VALIDATE : {self.__str__()} move to {move}")
        color = "white" if self.color == "white" else "black"
        notcolor = "black" if self.color == "white" else "white"

        copy_piece = copy.deepcopy(self)
        print("piece copy created")
        copy_board = copy.deepcopy(chessboard)
        print("validate board copy created")
        copy_board.display()
        

        playerTurnCopy = chessPlayer.Player(color) #import Player?
        playerTurnCopy.populate_pieces(copy_board)
        playerNotTurnCopy = chessPlayer.Player(notcolor)

        copy_board.apply_temp_move(move, playerTurnCopy, self)

        if copy_board.checkCheck(playerTurnCopy, playerNotTurnCopy):
            print(f"{self.__str__()} move to {move} NOT VALID returning False")
            return False
        else:
            print(f"{self.__str__()} move to {move} VALID returning True")
            return True

class Pawn(Piece):
    def __init__(self, color, x, y):
            super().__init__(color, x, y)
            self.turns_moved = 0
            self.made_2jump_lastturn = False

    def increment_turns_moved(self):
        self.turns_moved = self.turns_moved + 1

    def legal_moves(self, chessboard):
        moves = []
        if self.color == 'white':
            if chessboard.board[self.x-1][self.y] is None:
                moves.append((self.x-1, self.y))
                if self.x == 6 and chessboard.board[self.x-2][self.y] is None:
                    moves.append((self.x-2, self.y))

            white_pawn_moves = [(-1,-1),(-1,1)]
            for add_x, add_y in white_pawn_moves:
                if -1 < self.x + add_x and self.x + add_x < 8 and -1 < self.y + add_y and self.y + add_y < 8:
                    if chessboard.board[self.x+add_x][self.y+add_y] and chessboard.board[self.x+add_x][self.y+add_y].color != self.color:
                        moves.append((self.x + add_x, self.y + add_y))

            if chessboard.last_move:
                if chessboard.last_move[0].__str__() == 'p':
                    if (chessboard.last_move[1], chessboard.last_move[2]) == ((self.x-2,self.y-1),(self.x,self.y-1)):
                        moves.append("epWL")
                    if (chessboard.last_move[1], chessboard.last_move[2]) == ((self.x-2,self.y+1),(self.x,self.y+1)):
                        moves.append("epWR")

                    
        else:
            if chessboard.board[self.x+1][self.y] is None:
                moves.append((self.x+1, self.y))
                if self.x == 1 and chessboard.board[self.x+2][self.y] is None:
                    moves.append((self.x+2, self.y))

            black_pawn_moves = [(1,-1),(1,1)]
            for add_x, add_y in black_pawn_moves:
                if -1 < self.x + add_x and self.x + add_x < 8 and -1 < self.y + add_y and self.y + add_y < 8:
                    if chessboard.board[self.x+add_x][self.y+add_y] and chessboard.board[self.x+add_x][self.y+add_y].color != self.color:
                        moves.append((self.x + add_x, self.y + add_y))

            if chessboard.last_move:
                if chessboard.last_move[0].__str__() == 'P':
                    if (chessboard.last_move[1], chessboard.last_move[2]) == ((self.x+2,self.y-1),(self.x,self.y-1)):
                        moves.append("epBL")
                    if (chessboard.last_move[1], chessboard.last_move[2]) == ((self.x+2,self.y+1),(self.x,self.y+1)):
                        moves.append("epBR")

        # validate moves
        moves2 = []
        for move in moves:
            if self.validate_move(move, chessboard):
                moves2.append(move)

        return moves2
    
    def __str__(self):
        return 'P' if self.color == 'white' else 'p'

class Rook(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.has_moved = False
    
    def update_has_moved(self, bool):
        self.has_moved = bool

    def legal_moves(self, chessboard):
        moves = []
        #down
        for i in range(self.x + 1, 8):
            if chessboard.board[i][self.y] is None:
                moves.append((i, self.y))
            elif chessboard.board[i][self.y].color != self.color:
                moves.append((i, self.y))
                break
            else:
                break
        #up
        for i in range(self.x - 1, -1, -1):
            if chessboard.board[i][self.y] is None:
                moves.append((i, self.y))
            elif chessboard.board[i][self.y].color != self.color:
                moves.append((i, self.y))
                break
            else:
                break
        #right
        for j in range(self.y + 1, 8):
            if chessboard.board[self.x][j] is None:
                moves.append((self.x, j))
            elif chessboard.board[self.x][j].color != self.color:
                moves.append((self.x, j))
                break
            else:
                break
        #down
        for j in range(self.y - 1, -1, -1):
            if chessboard.board[self.x][j] is None:
                moves.append((self.x, j))
            elif chessboard.board[self.x][j].color != self.color:
                moves.append((self.x, j))
                break
            else:
                break
        return moves
    
    def __str__(self):
        return 'R' if self.color == 'white' else 'r'

class Knight(Piece):
    def legal_moves(self, chessboard):
        knight_moves = ((-1,-2),(-2,-1),(1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1))
        moves = []
        for add_x, add_y in knight_moves:
            if -1 < self.x + add_x and self.x + add_x < 8 and -1 < self.y + add_y and self.y + add_y < 8: 
                if not chessboard.board[self.x+add_x][self.y+add_y] or (chessboard.board[self.x+add_x][self.y+add_y] and chessboard.board[self.x+add_x][self.y+add_y].color != self.color):
                    moves.append((self.x+add_x,self.y+add_y))
        return moves
    
    def __str__(self):
        return 'N' if self.color == 'white' else 'n'
       
class Bishop(Piece):
    def legal_moves(self, chessboard):
        moves = []
        #up left
        i,j = self.x,self.y
        while i > 0 and j > 0:
            i -= 1
            j -= 1
            if chessboard.board[i][j] == None:
                moves.append((i,j))
            elif chessboard.board[i][j].color != self.color:
                moves.append((i,j))
                break
            else:
                break
        #down left
        i,j = self.x,self.y
        while i < 7 and j > 0:
            i += 1
            j -= 1
            if chessboard.board[i][j] == None:
                moves.append((i,j))
            elif chessboard.board[i][j].color != self.color:
                moves.append((i,j))
                break
            else:
                break
        #up right
        i,j = self.x,self.y
        while i > 0 and j < 7:
            i -= 1
            j += 1
            if chessboard.board[i][j] == None:
                moves.append((i,j))
            elif chessboard.board[i][j].color != self.color:
                moves.append((i,j))
                break
            else:
                break
        #down right
        i,j = self.x,self.y
        while i < 7 and j < 7:
            i += 1
            j += 1
            if chessboard.board[i][j] == None:
                moves.append((i,j))
            elif chessboard.board[i][j].color != self.color:
                moves.append((i,j))
                break
            else:
                break
        return moves
    
    def __str__(self):
        return 'B' if self.color == 'white' else 'b'
    
class Queen(Piece):
    def legal_moves(self, chessboard):
        moves = []
        #down
        for i in range(self.x + 1, 8):
            if chessboard.board[i][self.y] is None:
                moves.append((i, self.y))
            elif chessboard.board[i][self.y].color != self.color:
                moves.append((i, self.y))
                break
            else:
                break
        #up
        for i in range(self.x - 1, -1, -1):
            if chessboard.board[i][self.y] is None:
                moves.append((i, self.y))
            elif chessboard.board[i][self.y].color != self.color:
                moves.append((i, self.y))
                break
            else:
                break
        #right
        for j in range(self.y + 1, 8):
            if chessboard.board[self.x][j] is None:
                moves.append((self.x, j))
            elif chessboard.board[self.x][j].color != self.color:
                moves.append((self.x, j))
                break
            else:
                break
        #down
        for j in range(self.y - 1, -1, -1):
            if chessboard.board[self.x][j] is None:
                moves.append((self.x, j))
            elif chessboard.board[self.x][j].color != self.color:
                moves.append((self.x, j))
                break
            else:
                break
        #up left
        i,j = self.x,self.y
        while i > 0 and j > 0:
            i -= 1
            j -= 1
            if chessboard.board[i][j] == None:
                moves.append((i,j))
            elif chessboard.board[i][j].color != self.color:
                moves.append((i,j))
                break
            else:
                break
        #down left
        i,j = self.x,self.y
        while i < 7 and j > 0:
            i += 1
            j -= 1
            if chessboard.board[i][j] == None:
                moves.append((i,j))
            elif chessboard.board[i][j].color != self.color:
                moves.append((i,j))
                break
            else:
                break
        #up right
        i,j = self.x,self.y
        while i > 0 and j < 7:
            i -= 1
            j += 1
            if chessboard.board[i][j] == None:
                moves.append((i,j))
            elif chessboard.board[i][j].color != self.color:
                moves.append((i,j))
                break
            else:
                break
        #down right
        i,j = self.x,self.y
        while i < 7 and j < 7:
            i += 1
            j += 1
            if chessboard.board[i][j] == None:
                moves.append((i,j))
            elif chessboard.board[i][j].color != self.color:
                moves.append((i,j))
                break
            else:
                break
        return moves
    
    def __str__(self):
        return 'Q' if self.color == 'white' else 'q'

class King(Piece):
    def __init__(self, color, x, y):
            super().__init__(color, x, y)
            self.has_moved = False

    def update_has_moved(self, bool):
        self.has_moved = bool

    def legal_moves(self, chessboard):
        king_moves = ((0,1),(1,0),(0,-1),(-1,0),(1,1),(-1,-1),(1,-1),(-1,1))
        moves = []
        for add_x, add_y in king_moves:
            if -1 < self.x + add_x and self.x + add_x < 8 and -1 < self.y + add_y and self.y + add_y < 8: 
                if not chessboard.board[self.x+add_x][self.y+add_y] or (chessboard.board[self.x+add_x][self.y+add_y] and chessboard.board[self.x+add_x][self.y+add_y].color != self.color):
                    moves.append((self.x+add_x, self.y+add_y))

        if chessboard.board[self.x][4].__str__() in ('K', 'k') and chessboard.board[self.x][4].has_moved == False:
            if chessboard.board[self.x][5] == None and chessboard.board[self.x][6] == None:
                if (chessboard.board[self.x][7].__str__() == 'R' or chessboard.board[self.x][7].__str__() == 'r') and chessboard.board[self.x][7] and chessboard.board[self.x][7].has_moved == False:
                    #moves.append((self.x, 6))
                    moves.append("castleR")
            if chessboard.board[self.x][3] == None and chessboard.board[self.x][2] == None and chessboard.board[self.x][1] == None:
                if (chessboard.board[self.x][0].__str__() == 'R' or chessboard.board[self.x][0].__str__() == 'r') and chessboard.board[self.x][0] and chessboard.board[self.x][0].has_moved == False:
                    #moves.append((self.x, 2))
                    moves.append("castleL")
        return moves

    def __str__(self):
        return 'K' if self.color == 'white' else 'k'

