import pygame
import sys
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
    'wpawn': pygame.image.load('chessImages/wpawn.png'),
    'bpawn': pygame.image.load('chessImages/bpawn.png'),
    'wrook': pygame.image.load('chessImages/wrook.png'),
    'brook': pygame.image.load('chessImages/brook.png'),
    'wknight': pygame.image.load('chessImages/wknight.png'),
    'bknight': pygame.image.load('chessImages/bknight.png'),
    'wbishop': pygame.image.load('chessImages/wbishop.png'),
    'bbishop': pygame.image.load('chessImages/bbishop.png'),
    'wqueen': pygame.image.load('chessImages/wqueen.png'),
    'bqueen': pygame.image.load('chessImages/bqueen.png'),
    'wking': pygame.image.load('chessImages/wking.png'),
    'bking': pygame.image.load('chessImages/bking.png'),
}

# Define a function to draw pieces
def draw_pieces(gameWindow, board):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != "--":
                gameWindow.blit(pieceImages[piece], pygame.Rect(col*square_size, row*square_size, square_size, square_size))

# Sample board configuration
board = [
    ["brook", "bknight", "bbishop", "bqueen", "bking", "bbishop", "bknight", "brook"],
    ["bpawn", "bpawn", "bpawn", "bpawn", "bpawn", "bpawn", "bpawn", "bpawn"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["wpawn", "wpawn", "wpawn", "wpawn", "wpawn", "wpawn", "wpawn", "wpawn"],
    ["wrook", "wknight", "wbishop", "wqueen", "wking", "wbishop", "wknight", "wrook"],
]

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
    draw_pieces(gameWindow, board)

    # Update the display
    pygame.display.flip()


# exit the game once !running, that condition will change when game is over
pygame.quit()
sys.exit()

