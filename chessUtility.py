import pygame
from chessColors import black, white, lightblue, lightgray, blue

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

#NEED TO CHANGE ONE OF THESE SO THAT THEY ARE GETTING THE SAME TYPE OF PARAMETER
#GO LOOK AT WHAT IS PASSED IN WHEN THEY ARE CALLED ACROSS ALL FILES AND FIGURE IT OUT

# Define a function to draw pieces
# from chessActual - board paramter is a grid - is subscripted
def draw_pieces(gameWindow, board):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece:
                pieceCode = board[row][col].__str__()
                gameWindow.blit(pieceImages[pieceCode], pygame.Rect((col*square_size) + 5, (row*square_size) + 5, square_size, square_size))

# Define a function to draw pieces
# from Player - chessboard is ChessBoard object of which the board variable is subscripted
def draw_pieces(gameWindow, chessboard):
    for row in range(8):
        for col in range(8):
            piece = chessboard.board[row][col]
            if piece:
                pieceCode = chessboard.board[row][col].__str__()
                gameWindow.blit(pieceImages[pieceCode], pygame.Rect((col*100) + 5, (row*100) + 5, 100, 100))
    

def draw_board(): # DONT KNOW PARAMS YET
    print("Draw board function!")

def draw_lines(): # DONT KNOW PARAMS YET
    print("Draw lines function!")

def draw_all(): #DONT KNOW PARAMS YET
    print("Draw all function!")