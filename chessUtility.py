import pygame
import copy
from chessColors import black, white, lightblue, lightgray, blue

square_size = 100
# Load images
pieceImages = {
    'P': pygame.image.load('chessImages/wpawn.png'),
    'p': pygame.image.load('chessImages/bpawn.png'),
    'R': pygame.image.load('chessImages/wrook.png'),
    'r': pygame.image.load('chessImages/brook.png'),
    'N': pygame.image.load('chessImages/wknight.png'),
    'n': pygame.image.load('chessImages/bknight.png'),
    'B': pygame.image.load('chessImages/wbishop.png'),
    'b': pygame.image.load('chessImages/bbishop.png'),
    'Q': pygame.image.load('chessImages/wqueen.png'),
    'q': pygame.image.load('chessImages/bqueen.png'),
    'K': pygame.image.load('chessImages/wking.png'),
    'k': pygame.image.load('chessImages/bking.png')
}
pieceImagesSmall = {
    'R': pygame.transform.scale(pygame.image.load('chessImages/wrook.png'), (50, 50)),
    'r': pygame.transform.scale(pygame.image.load('chessImages/brook.png'), (50, 50)),
    'N': pygame.transform.scale(pygame.image.load('chessImages/wknight.png'), (50, 50)),
    'n': pygame.transform.scale(pygame.image.load('chessImages/bknight.png'), (50, 50)),
    'B': pygame.transform.scale(pygame.image.load('chessImages/wbishop.png'), (50, 50)),
    'b': pygame.transform.scale(pygame.image.load('chessImages/bbishop.png'), (50, 50)),
    'Q': pygame.transform.scale(pygame.image.load('chessImages/wqueen.png'), (50, 50)),
    'q': pygame.transform.scale(pygame.image.load('chessImages/bqueen.png'), (50, 50))
}

# Define a function to draw pieces
# chessboard is ChessBoard object of which the board variable is subscripted
def draw_pieces(gameWindow, board):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece:
                pieceCode = board[row][col].__str__()
                gameWindow.blit(pieceImages[pieceCode], pygame.Rect((col*100) + 5, (row*100) + 5, 100, 100))

# draw tiles + lines + pieces
def draw_board(gameWindow, board):
    for row in range(8):
        for col in range(8):
            rect = pygame.Rect((col*square_size), (row*square_size), square_size, square_size)
            if (row + col) % 2 == 0:
                pygame.draw.rect(gameWindow, white, rect)
            else:
                pygame.draw.rect(gameWindow, lightgray, rect)
            pygame.draw.rect(gameWindow, black, rect, 1)
    draw_pieces(gameWindow, board)

def draw_lines(gameWindow):
    for i in range(8):
        for j in range(8):
            rect = pygame.Rect((i*square_size), (j*square_size), square_size, square_size)
            pygame.draw.rect(gameWindow, black, rect, 1)

'''
def validate_move(move, moving_piece, chessboard, playerTurnColor, playerNotTurnColor):
    dummyboard = copy.deepcopy(chessboard)
    if "ep" in move:
        piece_getting_taken = dummyboard.last_move[0]

        if move == "epWL":
            dummyboard.board[moving_piece.x - 1][moving_piece.y - 1] = moving_piece
            dummyboard.board[moving_piece.x][moving_piece.y] = None
            moving_piece.updatePosition(moving_piece.x - 1, moving_piece.y - 1)
        elif move == "epWR":
            dummyboard.board[moving_piece.x - 1][moving_piece.y + 1] = moving_piece
            dummyboard.board[moving_piece.x][moving_piece.y] = None
            moving_piece.updatePosition(moving_piece.x - 1, moving_piece.y + 1)
        elif move == "epBL":
            dummyboard.board[moving_piece.x + 1][moving_piece.y - 1] = moving_piece
            dummyboard.board[moving_piece.x][moving_piece.y] = None
            moving_piece.updatePosition(moving_piece.x + 1, moving_piece.y - 1)
        elif move == "epBR":
            dummyboard.board[moving_piece.x + 1][moving_piece.y + 1] = moving_piece
            dummyboard.board[moving_piece.x][moving_piece.y] = None
            moving_piece.updatePosition(moving_piece.x + 1, moving_piece.y + 1)
        dummyboard.board[piece_getting_taken.x][piece_getting_taken.y] = None
    
        if "castle" in move:
            dummyboard.applyCastle(move, moving_piece)
            return 0
        
    



    if check after move applied to dummy board:
        return false


def applyMove(self, move, moving_player, moving_piece, gameWindow):
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
    
        #if piece captured then add to captured pieces of moving player
        if self.board[x][y]:
            moving_player.addToCaptured(self.board[x][y])
            
        #make moved-to location new piece and moved-from location None
        self.board[x][y] = moving_piece
        self.board[moving_piece.getX()][moving_piece.getY()] = None

        moving_piece.updatePosition(x, y)

        if (moving_piece.__str__() == 'P' and move[0] == 0) or (moving_piece.__str__() == 'p' and move[0] == 7):
            self.promote_pawn(x, y, moving_player, moving_piece, gameWindow) 

        if moving_piece.__str__() == 'k' or moving_piece.__str__() == 'K' or moving_piece.__str__() == 'R' or moving_piece.__str__() == 'r':
            moving_piece.update_has_moved(True)

    def applyCastle(self, move, moving_piece):
        #print(f"Applying castle or move {move} of piece {moving_piece.__str__()} done by player {moving_piece.color}")

        if move == "castleR": #((moving_piece.getX(), 6))
            self.board[moving_piece.getX()][6] = self.board[moving_piece.getX()][4]
            print(f"about to update position of {self.board[moving_piece.getX()][6]}")
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
    
    def promote_pawn(self, x, y, moving_player, moving_piece, gameWindow):
        potential_pieces_w = [('R',(0, 0)), ('B', (50, 0)), ('N', (0, 50)), ('Q', (50, 50))]
        potential_pieces_b = [('r',(0, 0)), ('b', (50, 0)), ('n', (0, 50)), ('q', (50, 50))]

        draw_board(gameWindow, self.board)
        #print("SELF PASS WORKED")

        colors = [white, lightgray]
        if moving_player.color == "white":
            moving_player.change_square_color(gameWindow, (x, y), colors[y % 2])
            for i, start in potential_pieces_w:
                gameWindow.blit(pieceImagesSmall[i], pygame.Rect((y*100) + start[1], (x*100) + start[0], 50, 50))
        else:
            moving_player.change_square_color(gameWindow, (x, y), colors[y % 2])
            for i, start in potential_pieces_b:
                gameWindow.blit(pieceImagesSmall[i], pygame.Rect((y*100) + start[1], (x*100) + start[0], 50, 50))

        pygame.display.flip()
        promote_selection = None
        promote_selection = random.choice(('queen','rook','knight','bishop'))

        while not promote_selection:
            #pygame.time.wait(100)
            #print("MADE IT TO start of select piece")
            for event in pygame.event.get():
                #print(f"FIRST LINE IN FOR LOOP event : {event}")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #print("PAST IF mouse down STATEMENT")
                    pos = pygame.mouse.get_pos()
                    col = pos[0] # -1?
                    row = pos[1] # -1?
                    print(f"Clicked on  {col}, {row}")
                    print("JUST GOT MOUSE POS")
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
                        print("looping again")
                        pygame.event.clear()

        if promote_selection == 'queen':
            self.board[x][y] = Queen(moving_player.color, x, y)
        if promote_selection == 'rook':
            self.board[x][y] = Rook(moving_player.color, x, y)
        if promote_selection == 'knight':
            self.board[x][y] = Knight(moving_player.color, x, y)
        if promote_selection == 'bishop':
            self.board[x][y] = Bishop(moving_player.color, x, y)

        #print("JUST DID A PROMOTION")
                        
    def applyep(self, move, moving_player, moving_piece):
        piece_getting_taken = self.last_move[0]

        if move == "epWL":
            self.board[moving_piece.x - 1][moving_piece.y - 1] = moving_piece
            self.board[moving_piece.x][moving_piece.y] = None
            moving_piece.updatePosition(moving_piece.x - 1, moving_piece.y - 1)
        elif move == "epWR":
            self.board[moving_piece.x - 1][moving_piece.y + 1] = moving_piece
            self.board[moving_piece.x][moving_piece.y] = None
            moving_piece.updatePosition(moving_piece.x - 1, moving_piece.y + 1)
        elif move == "epBL":
            self.board[moving_piece.x + 1][moving_piece.y - 1] = moving_piece
            self.board[moving_piece.x][moving_piece.y] = None
            moving_piece.updatePosition(moving_piece.x + 1, moving_piece.y - 1)
        elif move == "epBR":
            self.board[moving_piece.x + 1][moving_piece.y + 1] = moving_piece
            self.board[moving_piece.x][moving_piece.y] = None
            moving_piece.updatePosition(moving_piece.x + 1, moving_piece.y + 1)

        self.board[piece_getting_taken.x][piece_getting_taken.y] = None
        
        moving_player.addToCaptured(piece_getting_taken)

'''

def draw_all(): #DONT KNOW PARAMS YET
    print("Draw all function!")
