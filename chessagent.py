class ChessGame:
    def __init__(self):
        self.gameboard = ChessBoard()
        self.playerblack = Player('black')
        self.playerwhite = Player('white')
        self.ticker = 2
        self.victor = None

    def startGame(self):
        while not self.checkVictory():
            self.gameTurn()
        print(f"{self.checkVictory().color} player wins!14")
        
    def gameTurn(self):
        self.gameboard.display()

        if self.ticker % 2 == 0:
            self.playerwhite.populate_pieces(self.gameboard)
            selected_piece, chosen_move = self.playerwhite.chooseMove(self.gameboard)
            self.gameboard.applyMove(chosen_move, self.playerwhite, selected_piece)
            print("Chosen piece is ")
            print(selected_piece)
            print("Chosen move is ")
            print(chosen_move)

        else:
            self.playerblack.populate_pieces(self.gameboard)
            selected_piece, chosen_move = self.playerblack.chooseMove(self.gameboard)
            self.gameboard.applyMove(chosen_move, self.playerwhite, selected_piece)
            print("Chosen piece is ")
            print(selected_piece)
            print("Chosen move is ")
            print(chosen_move)

        self.ticker += 1

    def checkVictory(self):
        return self.gameboard.boardVictory(self.playerwhite, self.playerblack)
    
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

        if moving_piece.__str__() == 'k' or moving_piece.__str__() == 'K' or moving_piece.__str__() == 'R' or moving_piece.__str__() == 'r':
            moving_piece.update_has_moved(True)

    def applyCastle(self, move, moving_piece):
        if move == "castleR":
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
        print(f"White has captured: {playerw.captured_pieces}")
        print(f"Black has captured: {playerb.captured_pieces}")
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

    def selectPiece(self):
        for i in self.pieces:
            print(i.__str__())

        selectedPiece = int(input("Which piece would you like to move (enter index starting at 0 of piece)"))
        return self.pieces[selectedPiece]
    
    def chooseMove(self, chessboard):
        currPiece = self.selectPiece()
        currMoves = currPiece.legal_moves(chessboard)

        for i in currMoves:
            print(i)
        selectedMove = currMoves[int(input("Which move would you like to make (enter index starting at 0 of move)"))]
        return currPiece, selectedMove
    
    def addToCaptured(self, p):
        self.captured_pieces.append(p)

        
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
    
    def updatePosition(self, new_x, new_y):
        self.x = new_x
        self.y = new_y


class Pawn(Piece):
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
        return moves
    
    def __str__(self):
        return 'P' if self.color == 'white' else 'p'

class Rook(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.has_moved = False

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

        if chessboard.board[self.x][5] == None and chessboard.board[self.x][6] == None:
            if (chessboard.board[self.x][7].__str__() == 'R' or chessboard.board[self.x][7].__str__() == 'r') and chessboard.board[self.x][7].has_moved == False:
                #moves.append((self.x, 6))
                moves.append("castleR")
        if chessboard.board[self.x][3] == None and chessboard.board[self.x][2] == None and chessboard.board[self.x][1] == None:
            if (chessboard.board[self.x][0].__str__() == 'R' or chessboard.board[self.x][0].__str__() == 'r') and chessboard.board[self.x][0].has_moved == False:
                #moves.append((self.x, 2))
                moves.append("castleL")



        return moves

    def __str__(self):
        return 'K' if self.color == 'white' else 'k'

game1 = ChessGame()
game1.startGame()


