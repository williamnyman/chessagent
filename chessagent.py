class ChessBoard:
    def __init__(self):
        # Initialize an 8x8 chess board with None values
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.setup_board()

    def setup_board(self):
        # Initialize pieces on the board
        for i in range(8):
            self.board[1][i] = Pawn('black')  # Place black pawns on the second row
            self.board[6][i] = Pawn('white')  # Place white pawns on the seventh row

        # List defining the placement of major pieces
        placement = [
            Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook
        ]

        # Place major pieces on the first and last rows
        for i, piece in enumerate(placement):
            self.board[0][i] = piece('black')  # Place black pieces on the first row
            self.board[7][i] = piece('white')  # Place white pieces on the last row

    def display(self):
        # Display the board
        for row in self.board:
            print(" ".join([str(piece) if piece else '.' for piece in row]))
        print()


class Player:
    def __init__(self, color):
        self.color = color
        self.pieces = []

class Piece:
    def __init__(self, color):
        self.color = color

    def legal_moves(self, x, y, board):
        raise NotImplementedError("This method should be overridden in derived classes")


class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)

    def legal_moves(self, x, y, board):
        moves = []
        if self.color == 'white':
            if board[x-1][y] is None:
                moves.append((x-1, y))
            if x == 6 and board[x-2][y] is None:
                moves.append((x-2, y))
        else:
            if board[x+1][y] is None:
                moves.append((x+1, y))
            if x == 1 and board[x+2][y] is None:
                moves.append((x+2, y))
        return moves
    
    def __str__(self):
        return 'P' if self.color == 'white' else 'p'


class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)

    def legal_moves(self, x, y, board):
        moves = []
        for i in range(x + 1, 8):
            if board[i][y] is None:
                moves.append((i, y))
            elif board[i][y].color != self.color:
                moves.append((i, y))
                break
            else:
                break
        for i in range(x - 1, -1, -1):
            if board[i][y] is None:
                moves.append((i, y))
            elif board[i][y].color != self.color:
                moves.append((i, y))
                break
            else:
                break
        for j in range(y + 1, 8):
            if board[x][j] is None:
                moves.append((x, j))
            elif board[x][j].color != self.color:
                moves.append((x, j))
                break
            else:
                break
        for j in range(y - 1, -1, -1):
            if board[x][j] is None:
                moves.append((x, j))
            elif board[x][j].color != self.color:
                moves.append((x, j))
                break
            else:
                break
        return moves
    
    def __str__(self):
        return 'R' if self.color == 'white' else 'r'

class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)

    def legal_moves(self, x, y, board):
        knight_moves = ((-1,-2),(-2,-1),(1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1))
        moves = []
        for add_x, add_y in knight_moves:
            if 1 <= x + add_x and x + add_x <= 8 and 1 <= y + add_y and y + add_y <= 8: 
                if (board[x+add_x][y+add_y].color != self.color) or not board[x+add_x][y+add_y]:
                    moves.append((x+add_x,y+add_y))
        
        return moves





# Define the other pieces: Knight, Bishop, Queen, King similarly
# For brevity, they are not included here

# Example usage
chess_board = ChessBoard()
chess_board.display()
