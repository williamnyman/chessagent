import tkinter as tk

root = tk.Tk()
root.title("Chess Game")

w, h = 800, 800
rows, cols = 8, 8
cell_size = 100

canvas = tk.Canvas(root, width=w, height=h)
canvas.pack()

# Draw the Chessboard
def draw_chessboard():
    colors = ["white", "gray"]
    for row in range(rows):
        for col in range(cols):
            color = colors[(row + col) % 2]
            x1 = col * cell_size
            y1 = row * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size
            canvas.create_rectangle(x1, y1, x2, y2, fill=color)

# Load and display pieces
def load_pieces():
    pieces = {}
    for piece in ["wpawn", "bpawn", "wrook", "brook", "wknight", "bknight", "wbishop", "bbishop", "wqueen", "bqueen", "wking", "bking"]:
        pieces[piece] = PhotoImage(file=f"chessimages/{piece}.png")
    return pieces

def place_pieces(pieces):
    # Example piece placement
    initial_board = [
        ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
        ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
        [None] * 8,
        [None] * 8,
        [None] * 8,
        [None] * 8,
        ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
        ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"]
    ]

    for row in range(rows):
        for col in range(cols):
            piece = initial_board[row][col]
            if piece:
                x = col * cell_size + cell_size // 2
                y = row * cell_size + cell_size // 2
                canvas.create_image(x, y, image=pieces[piece])



# Draw the chessboard and pieces
draw_chessboard()
pieces = load_pieces()
place_pieces(pieces)

# Run the application
root.mainloop()