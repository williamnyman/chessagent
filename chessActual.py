import pygame
import sys
from chessGame import ChessGame
from chessColors import white, black, blue, lightblue, lightgray

from chessUtility import pieceImages, draw_pieces, draw_board, xyz

pygame.init()

# Define the size of the squares
square_size = 100

#####################
bwins = 0
wwins = 0
draws = 0
for i in range(1000):
#####################

    game1 = ChessGame()
    draw = False
    #print("GAME 1 is chessgame")
    #board1 = game1.gameboard.board
    #print("Board 1 = game1.gameboard.board")
    while not game1.checkVictory():
            if game1.ticker > 500:
                draw = True
                break

            #print("Start of while loop")
            
            # Fill the background
            xyz.fill(white)

            draw_board(game1.gameboard.board)

            # Update the display
            pygame.display.flip()

            game1.gameTurn()
            
       
    if draw:
          draws = draws + 1
          print("DRAW")

    else:
        if game1.checkVictory().color == "white":
            wwins = wwins + 1
        else:
            bwins = bwins + 1
        print(f"{game1.checkVictory().color} wins! -------------------------------")


#####################
#####################

# exit the game once !running, that condition will change when game is over
print(f"White wins: {wwins}")
print(f"Black wins: {bwins}")
print(f"Draws: {draws}")

pygame.quit()
sys.exit()