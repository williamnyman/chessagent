import pygame
import sys
from chessGame import ChessGame

pygame.init()

# make game window and title
gameWindow = pygame.display.set_mode((1200, 1000))
pygame.display.set_caption("Will Nyman's Chess Game")

# Define colors (maybe bring this to a different file)
white = (255, 255, 255)
lightgray = (211, 211, 211)
lightblue = (173, 250, 255)

# Define the size of the squares
square_size = 100

# Run the game loop
running = True
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

# Define a function to draw pieces
def draw_pieces(gameWindow, board):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece:
                pieceCode = board[row][col].__str__()
                gameWindow.blit(pieceImages[pieceCode], pygame.Rect(col*square_size, row*square_size, square_size, square_size))


game1 = ChessGame()
board1 = game1.gameboard.board
game1.startGame()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            col = pos[0] // square_size
            row = pos[1] // square_size
            print(f"Clicked on column {col}, row {row}")

    # Fill the background
    gameWindow.fill(white)

    # Draw the chessboard
    for row in range(8):
        for col in range(8):
            rect = pygame.Rect(col*square_size, row*square_size, square_size, square_size)
            if (row + col) % 2 == 0:
                pygame.draw.rect(gameWindow, white, rect)
            else:
                pygame.draw.rect(gameWindow, lightgray, rect)


    # Draw the pieces
    draw_pieces(gameWindow, board1)
    

    # Update the display
    pygame.display.flip()


# exit the game once !running, that condition will change when game is over
pygame.quit()
sys.exit()

