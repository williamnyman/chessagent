import pygame
import copy
import random
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

# Define universal gameWindow that will be used instead of gameWindow which is passed in redundantly
xyz = pygame.display.set_mode((1200, 1000))
pygame.display.set_caption("Will Nyman's Chess Game")

# Define a function to draw pieces
# chessboard is ChessBoard object of which the board variable is subscripted
def draw_pieces(board):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece:
                pieceCode = board[row][col].__str__()
                xyz.blit(pieceImages[pieceCode], pygame.Rect((col*100) + 5, (row*100) + 5, 100, 100))

# draw tiles + lines + pieces
def draw_board(board):
    for row in range(8):
        for col in range(8):
            rect = pygame.Rect((col*square_size), (row*square_size), square_size, square_size)
            if (row + col) % 2 == 0:
                pygame.draw.rect(xyz, white, rect)
            else:
                pygame.draw.rect(xyz, lightgray, rect)
            pygame.draw.rect(xyz, black, rect, 1)
    draw_pieces(board)

def draw_lines():
    for i in range(8):
        for j in range(8):
            rect = pygame.Rect((i*square_size), (j*square_size), square_size, square_size)
            pygame.draw.rect(xyz, black, rect, 1)


def draw_all(): #DONT KNOW PARAMS YET
    print("Draw all function!")

