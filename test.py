import tkinter as tk

class ChessBoardGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Chess Board")
        self.canvas = tk.Canvas(self.master, width=400, height=400)
        self.canvas.pack()
        self.draw_board()
        self.place_pieces()
        self.selected_piece = None
        self.canvas.bind('<Button-1>', self.click)

    def draw_board(self):
        colors = ["white", "gray"]
        for i in range(8):
            for j in range(8):
                color = colors[(i + j) % 2]
                x0, y0 = j * 50, i * 50
                x1, y1 = x0 + 50, y0 + 50
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)

    def place_pieces(self):
        self.pieces = {}
        white_pieces = {
            'R': 'a1', 'N': 'b1', 'B': 'c1', 'Q': 'd1', 'K': 'e1', 'B2': 'f1', 'N2': 'g1', 'R2': 'h1',
            'P0': 'a2', 'P1': 'b2', 'P2': 'c2', 'P3': 'd2', 'P4': 'e2', 'P5': 'f2', 'P6': 'g2', 'P7': 'h2'
        }
        black_pieces = {
            'r': 'h8', 'n': 'g8', 'b': 'f8', 'q': 'd8', 'k': 'e8', 'b2': 'c8', 'n2': 'b8', 'r2': 'a8',
            'p0': 'h7', 'p1': 'g7', 'p2': 'f7', 'p3': 'e7', 'p4': 'd7', 'p5': 'c7', 'p6': 'b7', 'p7':'a7'
        }
        for piece, position in white_pieces.items():
            self.place_piece(piece, position, 'white')
        for piece, position in black_pieces.items():
            self.place_piece(piece, position, 'black')

    def place_piece(self, piece, position, color):
        row, col = self.parse_position(position)
        x, y = col * 50 + 25, row * 50 + 25
        self.pieces[piece] = {'position': position, 'color': color}
        self.canvas.create_text(x+1, y+1, text=piece, font=("Arial", 24), fill='white' if color == 'black' else 'black', tags=piece)
        self.canvas.create_text(x, y, text=piece, font=("Arial", 24), fill=color, tags=piece)

    def click(self, event):
        x, y = event.x, event.y
        col = x // 50
        row = y // 50
        clicked_position = chr(ord('a') + col) + str(8 - row)
        piece_clicked = self.get_piece_clicked(clicked_position)
        if piece_clicked:
            self.selected_piece = piece_clicked
        elif self.selected_piece:
            self.move_piece(clicked_position)

    def get_piece_clicked(self, position):
        for piece, data in self.pieces.items():
            if data['position'] == position:
                return piece
        return None

    def move_piece(self, new_position):
        if new_position != self.pieces[self.selected_piece]['position']:
            if self.is_valid_move(new_position):
                self.pieces[self.selected_piece]['position'] = new_position
                self.redraw_board()
                self.selected_piece = None

    def is_valid_move(self, new_position):
        piece_type = self.selected_piece[0]  # первая буква имени фигуры
        current_position = self.pieces[self.selected_piece]['position']
        piece_color = self.pieces[self.selected_piece]['color']

        # Правила для пешки
        if piece_type.lower() == 'p':
            col_diff = abs(ord(current_position[0]) - ord(new_position[0]))
            row_diff = int(new_position[1]) - int(current_position[1])
            # Шаг на одну клетку вперед
            if col_diff == 0 and row_diff == 1 and self.is_empty(new_position):
                return True
            # Первый ход: шаг на две клетки вперед
            elif col_diff == 0 and row_diff == 2 and current_position[1] == '2' and self.is_empty(new_position):
                return True
            # Атака по диагонали
            elif col_diff == 1 and row_diff == 1 and not self.is_empty(new_position) and self.is_opponent(new_position, piece_color):
                return True
            else:
                return False
        # Другие правила для других фигур могут быть добавлены здесь

        return True  # Вернуть True, если ход разрешен для других фигур или если правила не определены

    def is_empty(self, position):
        for piece, data in self.pieces.items():
            if data['position'] == position:
                return False
        return True

    def is_opponent(self, position, piece_color):
        for piece, data in self.pieces.items():
            if data['position'] == position and data['color'] != piece_color:
                return True
        return False


    def redraw_board(self):
        self.canvas.delete('all')
        self.draw_board()
        for piece, data in self.pieces.items():
            self.place_piece(piece, data['position'], data['color'])

    def parse_position(self, position):
        col = ord(position[0]) - ord('a')
        row = 8 - int(position[1])
        return row, col

root = tk.Tk()
app = ChessBoardGUI(root)
root.mainloop()
