import chessVisuals
from chessPieces import Pawn, Rook, Knight, Bishop, Queen, King

class Player:
    def __init__(self, color):
        self.color = color
        self.pieces = []
        self.captured_pieces = []

    def takeTurn(self, chessboard):
        self.selectPiece()
        self.chooseMove(chessboard)

    def populate_pieces(self, chessboard):
        self.pieces = chessboard.retrievePieces(self.color)

    def selectPiece(self):
        for i in self.pieces:
            print(i.__str__())
        selectedPiece = int(input("Which piece would you like to move (enter index starting at 0 of piece)"))
        return self.pieces[selectedPiece]
    
    def chooseMove(self, chessboard):
        currPiece = self.selectPiece()
        currMoves = currPiece.legal_moves(chessboard)

        for i in currMoves:
            print(i)
        selectedMove = currMoves[int(input("Which move would you like to make (enter index starting at 0 of move)"))]
        return currPiece, selectedMove
    
    def addToCaptured(self, p):
        self.captured_pieces.append(p)
