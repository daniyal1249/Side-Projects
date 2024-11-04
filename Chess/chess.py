import turtle
import math as m
import os

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
        self.x = x  # integer
        self.y = y  # integer
        self.color = color
        self.stamp_id = None

    def draw(self, x=None, y=None):
        global all_pieces

        if x is not None and y is not None:
            self.x, self.y = x, y

        pointer.up()
        pointer.goto(self.x + 0.5, self.y + 0.5)
        pointer.color(self.color)
        pointer.shape(self.shape)
        pointer.shapesize(2, 2)
        
        if self.stamp_id is not None:
            pointer.clearstamp(self.stamp_id)
        for piece in all_pieces:
            if piece is self:
                continue
            if (piece.x, piece.y) == (self.x, self.y):
                pointer.clearstamp(piece.stamp_id)
                all_pieces.remove(piece)
                break
        self.stamp_id = pointer.stamp()


class King(ChessPiece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        if self.color == 'white':
            self.shape = shape_dict['wK']
        else:
            self.shape = shape_dict['bK']

    def gen_possible_moves(self, all_pieces):
        possible_moves = {(i, j) for i in range(self.x - 1, self.x + 2) 
                         for j in range(self.y - 1, self.y + 2) 
                         if 0 <= i < 8 and 0 <= j < 8 
                         and (i, j) != (self.x, self.y)}

        for piece in all_pieces:  # need to remove pawn diagonal cases
            if (piece.x, piece.y) in possible_moves and piece.color == self.color:
                possible_moves.remove((piece.x, piece.y))
            
            elif piece.color != self.color and piece not in kings and piece not in pawns:
                for pos in piece.gen_possible_moves(all_pieces).intersection(possible_moves):
                    possible_moves.remove(pos)

            elif piece.color != self.color and piece in kings:
                for pos in piece.gen_possible_moves(set()).intersection(possible_moves):
                    possible_moves.remove(pos)

        return possible_moves
        
class Queen(ChessPiece):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        if self.color == 'white':
            self.shape = shape_dict['wQ']
        else:
            self.shape = shape_dict['bQ']

    def gen_possible_moves(self, all_pieces):
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

    def gen_possible_moves(self, all_pieces):
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

    def gen_possible_moves(self, all_pieces):
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

    def gen_possible_moves(self, all_pieces):
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

    def gen_possible_moves(self, all_pieces):  # check if color switch works
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
        self.square_width = 4.8
        self.stamp_id_set = set()
        self.highlight = None

    def draw_square(self, x, y, color, outline):
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
            
        pointer.shapesize(self.square_width, self.square_width)  # check values later
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
            self.stamp_id_set.add(self.draw_square(piece.x, piece.y, 'yellow', outline=True))
            for pos in possible_moves:
                self.stamp_id_set.add(self.draw_square(*pos, 'gray', outline=True))
        else:
            self.highlight = None

    def display_message(self, message):
        pointer.up()
        pointer.goto(4, 4)  # Position at center
        pointer.write(message, align="center", font=("Arial", 24, "bold"))


class Check():  # can still move kings next to each other
    def __init__(self):
        self.attacker = None
        
    def set_attacker(self, piece):
        if piece.color == 'white':
            opp_king_index = 1
        else:
            opp_king_index = 0
            
        if (kings[opp_king_index].x, kings[opp_king_index].y) in piece.gen_possible_moves(all_pieces):
            self.attacker = piece
        else:
            self.attacker = None

    def filter_moves(self, piece):
        if piece.color == 'white':
            king_index = 0
        else:
            king_index = 1

        # if self.attacker is not None and piece in kings:
        #     other_pieces = [elem for elem in all_pieces if elem != piece]
        #     return piece.gen_possible_moves(all_pieces).difference(self.attacker.gen_possible_moves(other_pieces))
        
        if self.attacker is not None and piece not in kings:
            filtered_moves = piece.gen_possible_moves(all_pieces).intersection(self.attacker.gen_possible_moves(all_pieces))
            x, y = piece.x, piece.y
            for pos in filtered_moves.copy():
                piece.x, piece.y = pos
                if (kings[king_index].x, kings[king_index].y) in self.attacker.gen_possible_moves(all_pieces):
                    filtered_moves.remove(pos)

            piece.x, piece.y = x, y
            if (self.attacker.x, self.attacker.y) in piece.gen_possible_moves(all_pieces):
                filtered_moves.add((self.attacker.x, self.attacker.y))

            return filtered_moves

        else:
            return piece.gen_possible_moves(all_pieces)  # check if it makes copy


def click_pos(x, y):
    global click_x, click_y, click_processed
    click_x, click_y = m.floor(x), m.floor(y)
    click_processed = False

def switch_player(player):
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

# Set up board and pieces
board = Board()
check = Check()
kings = [King(4, 0, 'white'), King(4, 7, 'black')]
queens = [Queen(3, 0, 'white'), Queen(3, 7, 'black')]
rooks = [Rook(0, 0, 'white'), Rook(7, 0, 'white'), Rook(0, 7, 'black'), Rook(7, 7, 'black')]
bishops = [Bishop(2, 0, 'white'), Bishop(5, 0, 'white'), Bishop(2, 7, 'black'), Bishop(5, 7, 'black')]
knights = [Knight(1, 0, 'white'), Knight(6, 0, 'white'), Knight(1, 7, 'black'), Knight(6, 7, 'black')]
pawns = [Pawn(i, j, color) for i in range(8) for j, color in zip([1, 6], ['white', 'black'])]
all_pieces = kings + queens + rooks + bishops + knights + pawns

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
        total_moves = set()

        # Selecting a piece
        for piece in all_pieces:  # try dictionary approach
            total_moves.update(check.filter_moves(piece))
            if (click_x, click_y) == (piece.x, piece.y) and piece.color == player:
                possible_moves = check.filter_moves(piece)
                board.highlight_square(piece, possible_moves)
            
        # Moving a piece
        if board.highlight and (click_x, click_y) in possible_moves:
            board.highlight.draw(click_x, click_y)
            check.set_attacker(board.highlight)
            board.highlight_square(piece=None, possible_moves=None, highlight=False)
            possible_moves = set()
            player = switch_player(player)

        # Checkmate
        if check.attacker and not total_moves:
            board.display_message("Checkmate!")
            checkmate = True
        total_moves.clear()
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