import pygame
from chessColors import lightblue, lightgray, black, white

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

square_size = 100

# Define a function to draw pieces
def draw_pieces(gameWindow, boardprime):
    for row in range(8):
        for col in range(8):
            piece = boardprime[row][col]
            if piece:
                pieceCode = boardprime[row][col].__str__()
                gameWindow.blit(pieceImages[pieceCode], pygame.Rect((col*square_size) + 5, (row*square_size) + 5, square_size, square_size))

def draw_board(gameWindow, chessboard):
    # Fill the background
    gameWindow.fill(white)

    # Draw the chessboard + pieces
    for row in range(8):
        for col in range(8):
            rect = pygame.Rect((col*square_size), (row*square_size), square_size, square_size)
            if (row + col) % 2 == 0:
                pygame.draw.rect(gameWindow, white, rect)
            else:
                pygame.draw.rect(gameWindow, lightgray, rect)
            pygame.draw.rect(gameWindow, black, rect, 1)
    draw_pieces(gameWindow, chessboard)

    # Update the display
    pygame.display.flip()

def draw_lines(gameWindow):
    for i in range(8):
        for j in range(8):
            rect = pygame.Rect((i*square_size), (j*square_size), square_size, square_size)
            pygame.draw.rect(gameWindow, black, rect, 1)