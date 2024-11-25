import os
import time
import math as m
import turtle

screen = turtle.Screen()
screen.setup(width=800, height=800)
screen.screensize(1600, 1600)
screen.setworldcoordinates(0, 0, 8, 8)
screen.tracer(0)

pointer = turtle.Turtle()
pointer.hideturtle()
pointer.speed(0)
pointer.up()

class ChessPiece():
    def __init__(self, x, y, color):
        self.x = x  # integer 0-7
        self.y = y  # integer 0-7
        self.color = color
        self.shape = None
        self.stamp_id = 0

    def draw(self, x=None, y=None):
        if x is not None and y is not None:
            self.x, self.y = x, y
        if self.stamp_id is not None:
            pointer.clearstamp(self.stamp_id)

        pointer.up()
        pointer.goto(self.x + 0.5, self.y + 0.5)
        pointer.color(self.color)
        pointer.shape(self.shape)
        pointer.shapesize(2, 2)

        opponent_pieces = black_pieces if self.color == 'white' else white_pieces
        for piece in opponent_pieces:
            if (piece.x, piece.y) == (self.x, self.y):
                pointer.clearstamp(piece.stamp_id)
                all_pieces.remove(piece)
                opponent_pieces.remove(piece)
                break
        self.stamp_id = pointer.stamp()


class King(ChessPiece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        if self.color == 'white':
            self.shape = shape_dict['wK']
        else:
            self.shape = shape_dict['bK']

    def gen_possible_moves(self):
        possible_moves = {(i, j) for i in range(self.x - 1, self.x + 2) 
                         for j in range(self.y - 1, self.y + 2) 
                         if 0 <= i < 8 and 0 <= j < 8 
                         and (i, j) != (self.x, self.y)}

        for piece in all_pieces:
            if (piece.x, piece.y) in possible_moves and piece.color == self.color:
                possible_moves.remove((piece.x, piece.y))

            elif piece in kings and piece.color != self.color:
                for pos in possible_moves.copy():
                    if abs(piece.x - pos[0]) <= 1 and abs(piece.y - pos[1]) <= 1:
                        possible_moves.remove(pos)

        return possible_moves
        
class Queen(ChessPiece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        if self.color == 'white':
            self.shape = shape_dict['wQ']
        else:
            self.shape = shape_dict['bQ']

    def gen_possible_moves(self):
        possible_moves = {(i, j) for i in range(self.x - 7, self.x + 8) 
                          for j in range(self.y - 7, self.y + 8) 
                          if 0 <= i < 8 and 0 <= j < 8 
                          and ((i == self.x or j == self.y) 
                          or abs(i - self.x) == abs(j - self.y)) 
                          and (i, j) != (self.x, self.y)}
        
        for piece in all_pieces:
            if (piece.x, piece.y) in possible_moves:
                start_index = 1
                if piece.color == self.color:
                    start_index = 0

                norm_constant = max(abs(piece.x - self.x), abs(piece.y - self.y))
                dir_vec = [(piece.x - self.x) // norm_constant, (piece.y - self.y) // norm_constant]
                for i in range(start_index, 7):
                    if (piece.x + (i * dir_vec[0]), piece.y + (i * dir_vec[1])) in possible_moves:
                        possible_moves.remove((piece.x + (i * dir_vec[0]), piece.y + (i * dir_vec[1])))

        return possible_moves

class Rook(ChessPiece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        if self.color == 'white':
            self.shape = shape_dict['wR']
        else:
            self.shape = shape_dict['bR']

    def gen_possible_moves(self):
        possible_moves = {(i, j) for i in range(self.x - 7, self.x + 8) 
                          for j in range(self.y - 7, self.y + 8) 
                          if 0 <= i < 8 and 0 <= j < 8 
                          and (i == self.x or j == self.y) 
                          and (i, j) != (self.x, self.y)}
        
        for piece in all_pieces:
            if (piece.x, piece.y) in possible_moves:
                start_index = 1
                if piece.color == self.color:
                    start_index = 0

                norm_constant = max(abs(piece.x - self.x), abs(piece.y - self.y))
                dir_vec = [(piece.x - self.x) // norm_constant, (piece.y - self.y) // norm_constant]
                for i in range(start_index, 7):
                    if (piece.x + (i * dir_vec[0]), piece.y + (i * dir_vec[1])) in possible_moves:
                        possible_moves.remove((piece.x + (i * dir_vec[0]), piece.y + (i * dir_vec[1])))

        return possible_moves

class Bishop(ChessPiece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        if self.color == 'white':
            self.shape = shape_dict['wB']
        else:
            self.shape = shape_dict['bB']

    def gen_possible_moves(self):
        possible_moves = {(i, j) for i in range(self.x - 7, self.x + 8) 
                          for j in range(self.y - 7, self.y + 8) 
                          if 0 <= i < 8 and 0 <= j < 8 
                          and abs(i - self.x) == abs(j - self.y) 
                          and (i, j) != (self.x, self.y)}

        for piece in all_pieces:
            if (piece.x, piece.y) in possible_moves:
                start_index = 1
                if piece.color == self.color:
                    start_index = 0

                norm_constant = max(abs(piece.x - self.x), abs(piece.y - self.y))
                dir_vec = [(piece.x - self.x) // norm_constant, (piece.y - self.y) // norm_constant]
                for i in range(start_index, 7):
                    if (piece.x + (i * dir_vec[0]), piece.y + (i * dir_vec[1])) in possible_moves:
                        possible_moves.remove((piece.x + (i * dir_vec[0]), piece.y + (i * dir_vec[1])))

        return possible_moves

class Knight(ChessPiece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        if self.color == 'white':
            self.shape = shape_dict['wN']
        else:
            self.shape = shape_dict['bN']

    def gen_possible_moves(self):
        possible_moves = {(i, j) for i in range(self.x - 2, self.x + 3) 
                          for j in range(self.y - 2, self.y + 3) 
                          if ((abs(i - self.x) == 2 and abs(j - self.y) == 1) 
                          or (abs(i - self.x) == 1 and abs(j - self.y) == 2)) 
                          and 0 <= i < 8 and 0 <= j < 8}
        
        for piece in all_pieces:
            if (piece.x, piece.y) in possible_moves and piece.color == self.color:
                possible_moves.remove((piece.x, piece.y))

        return possible_moves

class Pawn(ChessPiece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        if self.color == 'white':
            self.shape = shape_dict['wP']
        else:
            self.shape = shape_dict['bP']

    def gen_possible_moves(self):
        if self.color == 'white':
            vstep = 1
        else:
            vstep = -1
        possible_moves = {(self.x, self.y + vstep)} if 0 <= self.y + vstep < 8 else set()
        if (self.y == 1 and vstep == 1) or (self.y == 6 and vstep == -1):
            possible_moves.add((self.x, self.y + (2 * vstep)))

        for piece in all_pieces:
            if (piece.x, piece.y) in possible_moves:
                for i in range(2):
                    if (piece.x, piece.y + (i * vstep)) in possible_moves:
                        possible_moves.remove((piece.x, piece.y + (i * vstep)))       

            if (piece.x, piece.y) == (self.x + 1, self.y + vstep) \
                or (piece.x, piece.y) == (self.x - 1, self.y + vstep):
                if piece.color != self.color:
                    possible_moves.add((piece.x, piece.y))

        return possible_moves


class Board():
    def __init__(self):
        self.square_width = 4.8  # check value later
        self.stamp_id_set = set()
        self.highlight = None

    def draw_square(self, x, y, color, outline, width=None):
        pointer.up()
        pointer.goto(x + 0.5, y + 0.5)

        if outline:
            if color == 'yellow':
                pointer.shape(shape_dict['yellow'])
            elif color == 'gray':
                pointer.shape(shape_dict['gray'])
        else:
            pointer.color(color)
            pointer.shape('square')
            
        if width is None:
            width = self.square_width
        pointer.shapesize(width, width)
        return pointer.stamp()

    def draw(self):
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    self.draw_square(i, j, 'tan', outline=False)

    def highlight_square(self, piece, possible_moves, highlight=True):  # modify default params
        for stamp in self.stamp_id_set:
            pointer.clearstamp(stamp)
        self.stamp_id_set.clear()

        if highlight:
            self.highlight = piece
            self.stamp_id_set.add(self.draw_square(piece.x, piece.y, color='yellow', outline=True))
            for pos in possible_moves:
                self.stamp_id_set.add(self.draw_square(*pos, color='gray', outline=True))
        else:
            self.highlight = None

    def display_message(self, message, duration=None):
        text_pointer = turtle.Turtle()
        text_pointer.hideturtle()
        text_pointer.speed(0)
        text_pointer.up()
        text_pointer.color("black")

        # Create white background
        for i in range(5, 11):
            for j in range(7, 9):
                self.draw_square(i/2 - 1/4, j/2 - 1/4, 'white', outline=False, width=self.square_width/2)

        lines = message.split("\n")
        for i, line in enumerate(lines):
            y_pos = 4 - (i * 0.5)  # y coordinate of each line
            text_pointer.goto(4, y_pos)
            text_pointer.write(line, align="center", font=("Arial", 30, "bold"))

        if duration is not None:
            time.sleep(duration)
            text_pointer.clear()


def in_check(player, opponent_pieces=None):
    king_index = 0 if player == 'white' else 1
    if opponent_pieces is None:
        opponent_pieces = black_pieces[1:] if player == 'white' else white_pieces[1:]
    for piece in opponent_pieces:
        if (kings[king_index].x, kings[king_index].y) in piece.gen_possible_moves():
            return True
    return False

def restrict_moves(piece, possible_moves):
    x, y = piece.x, piece.y
    opp_pieces = black_pieces[1:] if piece.color == 'white' else white_pieces[1:]

    valid_moves = set()
    for pos in possible_moves:
        piece.x, piece.y = pos
        opp_pieces_mod = [elem for elem in opp_pieces if (elem.x, elem.y) != pos]
        if not in_check(piece.color, opp_pieces_mod):
            valid_moves.add(pos)
    piece.x, piece.y = x, y

    return valid_moves


def click_pos(x, y):
    global click_x, click_y, click_processed
    click_x, click_y = m.floor(x), m.floor(y)
    click_processed = False

def opponent(player):
    if player == 'white':
        return 'black'
    else:
        return 'white'


# Load images
shape_dict = {}
for piece_type in ['K', 'Q', 'R', 'B', 'N', 'P']:
    shape_dict[f'w{piece_type}'] = os.path.join('shapes', f'w{piece_type}.gif')
    shape_dict[f'b{piece_type}'] = os.path.join('shapes', f'b{piece_type}.gif')

for path in shape_dict.values():
    screen.addshape(path)

for color in ['yellow', 'gray']:
    shape_dict[color] = os.path.join('shapes', f'{color}_outline.gif')
    screen.addshape(shape_dict[color])

# Initialize board and pieces
board = Board()
kings = [King(4, 0, 'white'), King(4, 7, 'black')]
queens = [Queen(3, 0, 'white'), Queen(3, 7, 'black')]
rooks = [Rook(0, 0, 'white'), Rook(7, 0, 'white'), Rook(0, 7, 'black'), Rook(7, 7, 'black')]
bishops = [Bishop(2, 0, 'white'), Bishop(5, 0, 'white'), Bishop(2, 7, 'black'), Bishop(5, 7, 'black')]
knights = [Knight(1, 0, 'white'), Knight(6, 0, 'white'), Knight(1, 7, 'black'), Knight(6, 7, 'black')]
pawns = [Pawn(i, j, color) for j, color in zip([1, 6], ['white', 'black']) for i in range(8)]
white_pieces = kings[:1] + queens[:1] + rooks[:2] + bishops[:2] + knights[:2] + pawns[:8]
black_pieces = kings[1:] + queens[1:] + rooks[2:] + bishops[2:] + knights[2:] + pawns[8:]
all_pieces = white_pieces + black_pieces

# Initialize variables
click_x, click_y = None, None
click_processed = True
possible_moves = set()
player = 'white'
checkmate = False

def update_game():
    global click_processed, possible_moves, player, checkmate

    if checkmate:
        return

    if not click_processed:
        # Selecting a piece
        player_pieces = white_pieces if player == 'white' else black_pieces
        for piece in player_pieces:  # try dictionary approach
            if (click_x, click_y) == (piece.x, piece.y):
                possible_moves = restrict_moves(piece, piece.gen_possible_moves())
                board.highlight_square(piece, possible_moves)
            
        # Moving a piece
        if board.highlight and (click_x, click_y) in possible_moves:
            board.highlight.draw(click_x, click_y)
            board.highlight_square(piece=None, possible_moves=None, highlight=False)
            possible_moves = set()
            player = opponent(player)

        # Checkmate
        if in_check(player):
            total_moves = set()
            player_pieces = white_pieces if player == 'white' else black_pieces
            for piece in player_pieces:
                total_moves.update(restrict_moves(piece, piece.gen_possible_moves()))
            if not total_moves:
                board.display_message(f"CHECKMATE\n{opponent(player).upper()} WINS")
                checkmate = True
            else:
                pass

        click_processed = True

    screen.update()
    screen.ontimer(update_game, 100)
    
def main():
    screen.listen()
    screen.onscreenclick(click_pos)
    board.draw()
    for piece in all_pieces:
        piece.draw()
    update_game()
    turtle.done()

main()