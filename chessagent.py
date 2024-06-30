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
        #update moved pieces x and y coords
        x,y = move
        moving_piece.updateX(x)
        moving_piece.updateY(y)

        #if piece captured then add to captured pieces of moving player
        if self.board[x][y] != None:
            moving_player.addToCaptured(self.board[x][y])
            
        #make moved-to location new piece and moved-from location None
        self.board[x][y] = moving_piece
        self.board[moving_piece.getX()][moving_piece.getY()] = None

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

    def populate_pieces(self, chessboard):
        self.pieces = chessboard.retrievePieces(self.color)

    def selectPiece(self, chessboard):
        for i in self.pieces:
            print(i.__str__())

        selectedPiece = int(input("Which piece would you like to move (enter index starting at 0 of piece)"))
        return self.pieces[selectedPiece]
    
    def chooseMove(self, chessboard):
        currPiece = self.selectPiece(chessboard)
        currMoves = currPiece.legal_moves(currPiece.getX(),currPiece.getY(),chessboard)

        for i in currMoves:
            print(i)
        selectedMove = input("Which move would you like to make (enter index starting at 0 of move)")
        return selectedMove
    
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
    
    def updateX(self, new):
        self.x = new

    def updateY(self, new):
        self.y = new


class Pawn(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)

    def legal_moves(self, x, y, chessboard):
        moves = []
        if self.color == 'white':
            if chessboard.board[x-1][y] is None:
                moves.append((x-1, y))
            if x == 6 and chessboard.board[x-2][y] is None:
                moves.append((x-2, y))
        else:
            if chessboard.board[x+1][y] is None:
                moves.append((x+1, y))
            if x == 1 and chessboard.board[x+2][y] is None:
                moves.append((x+2, y))
        return moves
    
    def __str__(self):
        return 'P' if self.color == 'white' else 'p'

class Rook(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)

    def legal_moves(self, x, y, chessboard):
        moves = []

        #down
        for i in range(x + 1, 8):
            if chessboard.board[i][y] is None:
                moves.append((i, y))
            elif chessboard.board[i][y].color != self.color:
                moves.append((i, y))
                break
            else:
                break

        #up
        for i in range(x - 1, -1, -1):
            if chessboard.board[i][y] is None:
                moves.append((i, y))
            elif chessboard.board[i][y].color != self.color:
                moves.append((i, y))
                break
            else:
                break

        #right
        for j in range(y + 1, 8):
            if chessboard.board[x][j] is None:
                moves.append((x, j))
            elif chessboard.board[x][j].color != self.color:
                moves.append((x, j))
                break
            else:
                break
        
        #down
        for j in range(y - 1, -1, -1):
            if chessboard.board[x][j] is None:
                moves.append((x, j))
            elif chessboard.board[x][j].color != self.color:
                moves.append((x, j))
                break
            else:
                break
        return moves
    
    def __str__(self):
        return 'R' if self.color == 'white' else 'r'

class Knight(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)

    def legal_moves(self, x, y, chessboard):
        knight_moves = ((-1,-2),(-2,-1),(1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1))
        moves = []
        for add_x, add_y in knight_moves:
            if -1 < x + add_x and x + add_x < 8 and -1 < y + add_y and y + add_y < 8: 
                if not chessboard.board[x+add_x][y+add_y] or (chessboard.board[x+add_x][y+add_y] and chessboard.board[x+add_x][y+add_y].color != self.color):
                    moves.append((x+add_x,y+add_y))
        
        return moves
    
    def __str__(self):
        return 'N' if self.color == 'white' else 'n'
    
class Bishop(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)

    def legal_moves(self, x, y, chessboard):
        moves = []
        #up left
        i,j = x,y
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
        i,j = x,y
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
        i,j = x,y
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
        i,j = x,y
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
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
    
    def legal_moves(self, x, y, chessboard):
        moves = []

        #down
        for i in range(x + 1, 8):
            if chessboard.board[i][y] is None:
                moves.append((i, y))
            elif chessboard.board[i][y].color != self.color:
                moves.append((i, y))
                break
            else:
                break

        #up
        for i in range(x - 1, -1, -1):
            if chessboard.board[i][y] is None:
                moves.append((i, y))
            elif chessboard.board[i][y].color != self.color:
                moves.append((i, y))
                break
            else:
                break

        #right
        for j in range(y + 1, 8):
            if chessboard.board[x][j] is None:
                moves.append((x, j))
            elif chessboard.board[x][j].color != self.color:
                moves.append((x, j))
                break
            else:
                break
        
        #down
        for j in range(y - 1, -1, -1):
            if chessboard.board[x][j] is None:
                moves.append((x, j))
            elif chessboard.board[x][j].color != self.color:
                moves.append((x, j))
                break
            else:
                break

        #up left
        i,j = x,y
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
        i,j = x,y
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
        i,j = x,y
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
        i,j = x,y
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

    def legal_moves(self, x, y, chessboard):
        king_moves = ((0,1),(1,0),(0,-1),(-1,0),(1,1),(-1,-1),(1,-1),(-1,1))
        moves = []
        for add_x, add_y in king_moves:
            if -1 < x + add_x and x + add_x < 8 and -1 < y + add_y and y + add_y < 8: 
                if not chessboard.board[x+add_x][y+add_y] or (chessboard.board[x+add_x][y+add_y] and chessboard.board[x+add_x][y+add_y].color != self.color):
                    moves.append((x+add_x,y+add_y))
        
        return moves

    def __str__(self):
        return 'K' if self.color == 'white' else 'k'
        


# Example usage
chess_board = ChessBoard()
chess_board.display()

play1 = Player('black')
play2 = Player('white')

play1.populate_pieces(chess_board)
play2.populate_pieces(chess_board)

#white knights are both moving to same spot
play2.chooseMove(chess_board)

#test