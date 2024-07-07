import tkinter as tk

root = tk.Tk()
root.title("Will Nyman's Chess Game")

w, h = 800, 800
rs, cs = 8, 8
cell_size = 100

canvas = tk.Canvas(root, width= w, height= h)
canvas.pack()

# Draw the Chessboard
def draw_chessboard():
    colors = ["white", "gray"]
    for row in range(rs):
        for col in range(cs):
            color = colors[(row + col) % 2]
            x1 = col * cell_size
            y1 = row * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size
            canvas.create_rectangle(x1, y1, x2, y2, fill=color)