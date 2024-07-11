import pygame
import sys
pygame.init()

gameWindow = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Will Nyman's Chess Game")

# Define colors
white = (255, 255, 255)
lightgray = (211, 211, 211)

# Define the size of the squares
square_size = 100

# Run the game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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

    # Update the display
    pygame.display.flip()

