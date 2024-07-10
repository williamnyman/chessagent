import tkinter as tk
from tkinter import PhotoImage

root = tk.Tk()
root.title("Chess Game")

w, h = 1600, 1000
rows, cols = 8, 8
cell_size = 100

canvas = tk.Canvas(root, width=w, height=h,)
canvas.pack(side="left")

initial_board = [
        ["brook", "bknight", "bbishop", "bqueen", "bking", "bbishop", "bknight", "brook"],
        ["bpawn", "bpawn", "bpawn", "bpawn", "bpawn", "bpawn", "bpawn", "bpawn"],
        [None] * 8,
        [None] * 8,
        [None] * 8,
        [None] * 8,
        ["wpawn", "wpawn", "wpawn", "wpawn", "wpawn", "wpawn", "wpawn", "wpawn"],
        ["wrook", "wknight", "wbishop", "wqueen", "wking", "wbishop", "wknight", "wrook"]
    ]

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
    piece_names = ["wpawn", "bpawn", "wrook", "brook", "wknight", "bknight", "wbishop", "bbishop", "wqueen", "bqueen", "wking", "bking"]
    for piece in piece_names:
        try:
            pieces[piece] = PhotoImage(file=f"chessimages/{piece}.png")
            print(f"Loaded image: chessimages/{piece}.png")
        except Exception as e:
            print(f"Failed to load image: chessimages/{piece}.png - {e}")
    return pieces

def place_pieces(pieces, board):
    for row in range(rows):
        for col in range(cols):
            piece = board[row][col]
            if piece:
                x = col * cell_size + cell_size // 2
                y = row * cell_size + cell_size // 2
                canvas.create_image(x, y, image=pieces[piece])

def change_rectangle_color(coordinate, color):
    x,y = coordinate
    x1 = x * cell_size
    y1 = y * cell_size
    x2 = x1 + cell_size
    y2 = y1 + cell_size
    canvas.create_rectangle(x1, y1, x2, y2, fill=color)

def remove_image(coordinate):
    x,y = coordinate
    colors = ["white", "gray"]
    color = colors[(x+y) % 2]
    change_rectangle_color(coordinate, color)

def place_image(coordinate, piece):
    x,y = coordinate
    imagex = x * cell_size + cell_size // 2
    imagey = y * cell_size + cell_size // 2
    canvas.create_image(imagex, imagey, image=pieces[piece])



# Handle mouse clicks
def on_click(event):
    col = event.x // cell_size
    row = event.y // cell_size
    print(f"Clicked on: {row}, {col}")

# Bind the click event
canvas.bind("<Button-1>", on_click)


# Draw the chessboard and pieces
draw_chessboard()
pieces = load_pieces()
place_pieces(pieces, initial_board)

remove_image((1,1))
remove_image((1,2))
place_image((3,3),"wpawn")



# Run the application
root.mainloop()
