import pygame
import sys
from chessGame import ChessGame
from chessColors import white, black, blue, lightblue, lightgray

from chessUtility import pieceImages, draw_pieces, draw_board


pygame.init()

# make game window and title
gameWindow = pygame.display.set_mode((1200, 1000))
pygame.display.set_caption("Will Nyman's Chess Game")

# Define the size of the squares
square_size = 100

#####################
bwins = 0
wwins = 0
for i in range(5000):
#####################

    game1 = ChessGame()
    #print("GAME 1 is chessgame")
    #board1 = game1.gameboard.board
    #print("Board 1 = game1.gameboard.board")
    while not game1.checkVictory():
            #print("Start of while loop")
            
            # Fill the background
            gameWindow.fill(white)

            draw_board(gameWindow, game1.gameboard.board)

            # Update the display
            pygame.display.flip()

            game1.gameTurn(gameWindow)
            
        
    if game1.checkVictory().color == "white":
          wwins = wwins + 1
    else:
          bwins = bwins + 1

#####################
    print(f"{game1.checkVictory().color} wins!")
#####################

    # exit the game once !running, that condition will change when game is over
print(f"White wins: {wwins}")
print(f"Black wins: {bwins}")

pygame.quit()
sys.exit()