"""
A chess module that does a lot of chess related things.
Will McGugan <will@willmcgugan.com>
http://www.willmcgugan.com
"""

__version__ = '0.0.3'
__program__ = 'chesswm'
__author__ = 'Will McGugan <will@willmcgugan.com>'
__copyright__ = 'Copyright (C) 2005 - 2006 Will McGugan'


# Seems to make a difference..
#import psyco
#psyco.full()

import re
import copy

WHITE, BLACK, UNDEFINED = list(range( 3))

def Opponent(colour):

    return not colour

PIECE_ABBREVIATIONS = "prnbqk."
PAWN, ROOK, KNIGHT, BISHOP, QUEEN, KING, BLANK = PIECE_ABBREVIATIONS

ONGOING, MATE, STALEMATE = list(range(3))

PIECE_NAMES = { 'p':'Pawn', 'r':'Rook', 'n':'Knight', 'b':'Bishop', 'q':'Queen', 'k':'King', '.':'Blank' }

INITIAL_BOARD = 'rnbqkbnr\n' \
                'pppppppp\n' \
                '........\n' \
                '........\n' \
                '........\n' \
                '........\n' \
                'PPPPPPPP\n' \
                'RNBQKBNR'

FILES = [ 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H' ]
RANKS = [ '1', '2', '3', '4', '5', '6', '7', '8' ]

PIECES = {  'P':(WHITE, PAWN),
            'R':(WHITE, ROOK),
            'N':(WHITE, KNIGHT),
            'B':(WHITE, BISHOP),
            'Q':(WHITE, QUEEN),
            'K':(WHITE, KING),
            '.':(UNDEFINED, BLANK),
            'p':(BLACK, PAWN),
            'r':(BLACK, ROOK),
            'n':(BLACK, KNIGHT),
            'b':(BLACK, BISHOP),
            'q':(BLACK, QUEEN),
            'k':(BLACK, KING) }

class Coord(object):

    "Board coordinate"

    def __init__(self, col=None, row=None):

        self.col, self.row = col, row

    def __hash__(self):

        return hash(self.col) ^ hash(self.row)

    @staticmethod
    def from_notation(notation):

        """Creates a coordinate from algebraic notation ie a1, c3 etc."""

        if len(notation) != 2:
            return None

        col = ord(notation[0].lower()) - ord('a')
        row = ord(notation[1].lower()) - ord('1')

        if col < 0 or row < 0:
            return None

        return Coord(col, row)

    @staticmethod
    def direction(pos1, pos2):

        col = cmp(pos2.col, pos1.col)
        row = cmp(pos2.row, pos1.row)
        return Coord(col, row)

    def on_board(self, board=None):

        """Returns True if the coordinate is in the given board. If no board is supplied, a standard 8x8 board is assumed."""

        if board is None:
            cols = 8
            rows = 8
        else:
            cols = board.cols
            rows = board.rows

        return (0 <= self.col < cols) and (0 <= self.row < rows)

        #return  ( self.col >= 0 and self.col < cols and
        #          self.row >= 0 and self.row < rows )

    def __eq__(self, rhs):

        return self.col == rhs.col and self.row == rhs.row

    def __add__(self, rhs):

        return Coord(self.col + rhs.col, self.row + rhs.row)

    def __sub__(self, rhs):

        return Coord(self.col - rhs.col, self.row - rhs.row)

    def __str__(self):

        return chr(ord('a') + self.col) + str(self.row+1)


UP = Coord(0,+1)
DOWN = Coord(0,-1)
LEFT = Coord(-1,0)
RIGHT = Coord(+1,0)

UP_LEFT = UP + LEFT
UP_RIGHT = UP + RIGHT
DOWN_LEFT = DOWN + LEFT
DOWN_RIGHT = DOWN + RIGHT


def MakePiece(char=None, type=BLANK, colour=WHITE):

    """A piece factory.
    This function creates Piece objects."""

    if char is not None:
        assert char in PIECES
        colour, type = PIECES[char]
    else:
        type = type
        colour = colour

    type=type.lower()

    if type == PAWN:
        return Pawn(colour)

    elif type == ROOK:
        return Rook(colour)

    elif type == KNIGHT:
        return Knight(colour)

    elif type == BISHOP:
        return Bishop(colour)

    elif type == QUEEN:
        return Queen(colour)

    elif type == KING:
        return King(colour)

    elif type == BLANK:
        return Blank()

    assert False, "Unknown piece!"


class Piece(object):

    "Base class for a chess piece."

    def __init__(self, type=BLANK, colour=UNDEFINED, position=None):

        self.last_move = None
        self.type = type
        self.colour = colour
        self.position = position


    def __str__(self):

        if self.colour == WHITE:
            return self.type.upper()
        else:
            return self.type


    def duplicate(self, piece):

        """Copies the attributes of another piece.
        This is typically used when a pawn is promoted."""

        self.last_move = piece.last_move
        self.colour = piece.colour
        self.position = piece.position


    def has_moved(self):

        """Returns True if this piece has moved from its initial position."""

        return self.last_move != None


    def just_moved(self, board):

        """Return True if this piece was the last piece to move."""

        return self.last_move == board.move_count-1


    def is_white(self):

        return self.colour == WHITE


    def is_black(self):

        return self.colour == BLACK


    def is_blank(self):

        return self.type == BLANK


    def is_opponent(self, piece):

        if self.colour == UNDEFINED:
            return False
        return self.colour != piece.colour


    def potential_moves(self, board, coord=None):

        """Return an iterable of all potential (disregarding check) moves."""

        return []


    def can_potentialy_attack(self, board, coord):

        """Return True if this piece can attack a coordinate.
        Only the pawn can attach a square it cant move to."""

        for move in self.potential_moves(board):

            if move.is_capture() and move.destination == coord:
                return True

        return False


    def do_move(self, board, move):

        """Do a move.
        The King overrides this when castling, because its more complicated."""

        # If it is a capture move the captures piece to the captures list
        if move.capture:

            board.captures.append( board.remove_piece(move.capture) )

        # remove the piece from its current position
        board.remove_piece(self.position)

        board.place_piece(move.destination, self)

        return self


    def fen_letter(self):

        """Return the letter abbreviation for this piece, upper case for white."""

        if self.is_white():
            return self.type.upper()
        return self.type


class BlankPiece(Piece):

    def __init__(self, position=None):

        Piece.__init__(self, position=position)


    def is_black(self):
        return False

    def is_white(self):
        return False

    def is_opponent(self):
        return False

    def is_blank(self):
        return True

    def fen_letter(self):
        return "."


class Pawn(Piece):

    def __init__(self, colour, position=None):

        Piece.__init__(self, PAWN, colour, position=position)


    def potential_moves(self, board, coord=None):

        if coord is None:
            coord = self.position

        if self.is_white():
            dir = UP
        else:
            dir = DOWN

        def check_promote(move):

            moves = []

            rank = move.destination.row

            if rank == 0 or rank == board.rows-1:

                moves.append(move.clone().promote_to(ROOK))
                moves.append(move.clone().promote_to(KNIGHT))
                moves.append(move.clone().promote_to(BISHOP))
                moves.append(move.clone().promote_to(QUEEN))

            else:

                moves.append(move)

            return moves

        move_ahead = coord + dir

        if move_ahead in board and board[move_ahead].is_blank():

            move = Move(coord, move_ahead)
            for move in check_promote(move):
                yield move

        if not self.has_moved() and board[move_ahead].is_blank():

            move_ahead_two = coord + dir + dir

            if move_ahead_two in board and board[move_ahead_two].is_blank():

                yield Move(coord, move_ahead_two)

        def check_capture(side):

            take = coord + dir + side

            if take in board:

                piece = board[take]

                if not piece.is_blank() and piece.is_opponent(self):

                    move = Move(coord, take, capture=take)
                    return check_promote(move)

                else:

                    en_passant = coord + side

                    if en_passant in board:

                        piece = board[en_passant]

                        if not piece.is_blank():

                            if piece.is_opponent(self) and piece.type == PAWN and piece.just_moved(board):
                                return [Move(coord, take, capture=en_passant, type=Move.EN_PASSANT)]
            return []

        for move in check_capture(LEFT):
            yield move

        for move in check_capture(RIGHT):
            yield move


    def can_potentialy_attack(self, board, coord):

        if self.is_white():
            dir = UP
        else:
            dir = DOWN

        attack = self.position + dir + LEFT
        if attack == coord:
            return True

        attack = self.position + dir + RIGHT
        if attack == coord:
            return True

        return False


class Rook(Piece):

    def __init__(self, colour, position=None):

        Piece.__init__(self, ROOK, colour, position=position)


    def potential_moves(self, board, coord=None):

        if coord is None:
            coord = self.position

        for direction in (UP, DOWN, LEFT, RIGHT):

            for piece in board.walk(coord, direction):

                if piece.is_blank():
                    yield Move(coord, piece.position)
                else:
                    if piece.is_opponent(self):
                        yield Move(coord, piece.position, capture=piece.position)
                    break

    def can_potentialy_attack(self, board, coord):

        col, row = self.position.col, self.position.row
        if coord.col != col and coord.row != row:
            return False

        direction = Coord.direction(self.position, coord)

        return board.test_walk(self.position, direction, coord)


class Knight(Piece):

    MOVES = ( (1,2), (2,1), (2,-1), (1,-2), (-1,2), (-2,1), (-2,-1), (-1,-2) )

    def __init__(self, colour, position=None):

        Piece.__init__(self, KNIGHT, colour, position=position)

    def potential_moves(self, board, coord=None):

        if coord is None:
            coord = self.position

        moves = []

        for m in Knight.MOVES:

            hop = coord + Coord(*m)

            if hop in board:

                piece = board.square(hop)

                if piece.is_blank():
                    yield Move(coord, hop)

                elif piece.is_opponent(self):
                    yield Move(coord, hop, capture=hop)

    def can_potentialy_attack(self, board, coord):

        for m in Knight.MOVES:

            hop = coord + Coord(*m)

            if hop in board and board[hop].position == coord:
                return True

        return False


class Bishop(Piece):

    def __init__(self, colour, position=None):

        Piece.__init__(self, BISHOP, colour, position=position)


    def potential_moves(self, board, coord=None):

        if coord is None:
            coord = self.position

        moves = []

        for direction in (UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT):

            for piece in board.walk(coord, direction):

                if piece.is_blank():
                    yield Move(coord, piece.position)
                else:
                    if piece.is_opponent(self):
                        yield Move(coord, piece.position, capture=piece.position)
                    break

    def can_potentialy_attack(self, board, coord):

        for direction in (UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT):

            if board.test_walk(self.position, direction, coord):
                return True

        return False


class Queen(Piece):

    def __init__(self, colour, position=None):

        Piece.__init__(self, QUEEN, colour, position=position)


    def potential_moves(self, board, coord=None):

        if coord is None:
            coord = self.position

        moves = []

        for direction in (LEFT, RIGHT, UP, DOWN, UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT):

            for piece in board.walk(coord, direction):

                if piece.is_blank():
                    yield Move(coord, piece.position)
                else:
                    if piece.is_opponent(self):
                        yield Move(coord, piece.position, capture=piece.position)
                    break

    def can_potentialy_attack(self, board, coord):

        for direction in (LEFT, RIGHT, UP, DOWN, UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT):

            if board.test_walk(self.position, direction, coord):
                return True

        return False


class King(Piece):

    def __init__(self, colour, position=None):

        Piece.__init__(self, KING, colour, position=position)

    def potential_moves(self, board, coord=None):

        if coord is None:
            coord = self.position

        moves = []

        for direction in (LEFT, RIGHT, UP, DOWN, UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT):

            destination = coord + direction

            if destination in board:
                piece = board.square(destination)

                if piece.is_blank():
                    yield Move(coord, piece.position)
                elif piece.is_opponent(self):
                    yield Move(coord, piece.position, capture=piece.position)

        if not self.has_moved() and not board.is_check(self.colour):

            def check_castle(rook_pos):

                piece = board[rook_pos]

                if piece.is_blank():
                    return False

                rook = piece

                if rook.type != ROOK or rook.has_moved() or self.has_moved():
                    return False

                if rook_pos.col < coord.col:
                    dir = LEFT
                else:
                    dir = RIGHT

                check_board = board.clone()
                step1 = coord+dir
                if step1 not in board or not check_board[step1].is_blank():
                    return False

                if check_board.move_piece(coord, step1).is_check(self.colour):
                    return False

                check_board = board.clone()
                step2 = coord+dir+dir
                if step1 not in board or not check_board[step1].is_blank():
                    return False

                if check_board.move_piece(coord, step2).is_check(self.colour):
                    return False

                return True

            qs_rook = Coord(0, coord.row)
            if check_castle(qs_rook):

                yield Move(coord, coord + LEFT + LEFT, type=Move.CASTLE_QUEENSIDE)

            ks_rook = Coord(board.cols-1, coord.row)
            if check_castle(ks_rook):

                yield Move(coord, coord + RIGHT + RIGHT, type=Move.CASTLE_KINGSIDE)

    def can_potentialy_attack(self, board, coord):

        direction = Coord.direction(self.position, coord)
        return abs(direction.col) <= 1 and abs(direction.row) <= 1

    def can_castle(self, board):

        def check_castle(rook_pos):

            piece = board[rook_pos]

            if piece.is_blank():
                return False

            rook = piece

            if rook.type != ROOK or rook.has_moved() or self.has_moved():
                return False

            if rook_pos.col < coord.col:
                dir = LEFT
            else:
                dir = RIGHT

            check_board = board.clone()
            step1 = coord+dir
            if step1 not in board or not check_board[step1].is_blank():
                return False

            if check_board.move_piece(coord, step1).is_check(self.colour):
                return False

            check_board = board.clone()
            step2 = coord+dir+dir
            if step1 not in board or not check_board[step1].is_blank():
                return False

            if check_board.move_piece(coord, step2).is_check(self.colour):
                return False

            return True

        coord = self.position
        qs_rook = Coord(0, coord.row)
        ks_rook = Coord(board.cols-1, coord.row)

        return check_castle(qs_rook), check_castle(ks_rook)

    def get_rooks(self, board):

        coord = self.position
        qs_rook = Coord(0, coord.row)
        ks_rook = Coord(board.cols-1, coord.row)

        return board[qs_rook], board[ks_rook]


    def do_move(self, board, move):

        if not move.is_castle():
            return super(King, self).do_move(board, move)

        coord = self.position
        if move.type == Move.CASTLE_QUEENSIDE:
            rook_from = Coord(0, coord.row)
            rook_too = move.destination + RIGHT
        elif move.type == Move.CASTLE_KINGSIDE:
            rook_from = Coord(board.cols-1, coord.row)
            rook_too = move.destination + LEFT

        super(King, self).do_move(board, move)

        board.move_piece(rook_from, rook_too)

        rook = board[rook_too]
        rook.last_move = board.move_count

        return self


    def can_potentialy_attack(self, board, coord):

        attack_piece = board[coord]
        if attack_piece.type == KING:
            return False

        return super(King, self).can_potentialy_attack(board, coord)





class ParseError(BaseException):

    def __init__(self, type="unknown", parse_text="", desc=""):

        self.type = type
        self.parse_text = parse_text
        self.desc = desc

    def __str__(self):

        return "%s (%s)"%(self.desc, self.type)


class Board( object ):

    "A chess board."

    PIECES = "PRNBQK"
    RANKS = "abcdefgh"
    FILES = "12345678"

    BLANKS = {}

    @staticmethod
    def get_blank(coord):

        if coord not in Board.BLANKS:
            Board.BLANKS[coord] = BlankPiece(coord)
        return Board.BLANKS[coord]


    def __init__(self, cols=8, rows=8, blank=True):

        self.move_count = 1
        self.half_move_count = 0
        self.pawn_move = 0
        self.last_move = None

        if blank:
            self.set_blank(cols, rows)
            self.captures = []


    def get_turn(self):

        """Whos move is it?"""

        return (BLACK, WHITE)[self.move_count & 1]


    def clone(self):

        #clone = Board(self.cols, self.rows, blank=False)
        #clone.rows = self.rows
        #clone.cols = self.cols
        #clone.move_count = self.move_count
        #clone.half_move_count = self.half_move_count
        #clone.pawn_move = self.pawn_move
        #clone.last_move = self.last_move
        #
        #clone.captures = [piece.clone() for piece in self.captures]
        #
        #clone.squares = copy.deepcopy(self.squares)
        #
        #return clone

        return copy.deepcopy(self)


    def set_blank(self, cols=8, rows=8):

        self.cols = cols
        self.rows = rows
        self.squares = tuple( [None for _ in range(self.rows)] for _ in range(self.cols) )


    def square(self, coord):

        """Return the square for a given coordinate."""

        return self.squares[coord.row][coord.col] or Board.get_blank(coord)


    def piece(self, coord):

        """Returns the piece on a given coordinate, or None"""

        piece = self.square(coord)
        if piece.is_blank():
            return None

        return piece


    def remove_piece(self, coord):

        """Removes the piece from a coordinate, and returns it."""

        piece = self.square(coord)
        self.squares[coord.row][coord.col] = None
        #self.set_blank(coord)
        return piece


    def place_piece(self, coord, piece):

        """Places a piece on the given coordinate."""

        self.squares[coord.row][coord.col] = piece
        #self.square(coord).piece = piece
        piece.position = coord
        return piece


    def move_piece(self, coord1, coord2):

        """Move a piece from coord1 to coord2."""

        piece = self.remove_piece(coord1)
        self.place_piece(coord2, piece)
        return self


    def __getitem__(self, coord):

        """Returns the square on the given coordinate."""

        if isinstance( coord, str ):
            coord = Coord.from_notation(coord)

        return self.square(coord)


    def setup(self, layout, PieceFactory=MakePiece):

        """Sets up the board."""

        for row, line in enumerate(reversed(layout.split('\n'))):

            if row >= self.rows:
                break

            for col, c in enumerate(line):

                if col < self.cols:

                    if c == '.':
                        self.squares[row][col] = None
                    else:
                        piece = PieceFactory(c)
                        piece.position = Coord(col, row)
                        self.squares[row][col] = piece


    def __contains__(self, coord):

        """Returns True if the coordinate is in the board."""

        return coord.on_board(self)


    def __str__(self):

        return self.board_visual()


    def walk(self, coord, direction):

        """Generates all the pieces in the given direction from an initial position, stopping at the edge or the first non-blank piece."""

        def walk_generator(self, coord, direction):

            coord+= direction
            while coord in self:

                piece = self.square(coord)
                coord+= direction

                yield piece

        return walk_generator(self, coord, direction)


    def test_walk(self, coord, direction, dest):

        coord+= direction
        while coord in self:

            piece = self.square(coord)
            if not piece.is_blank():
                return coord == dest

            coord+= direction

        return False


    def piece_in_direction(self, coord, direction, side=None):

        if side is None:
            side = self.get_turn()

        coord+= direction
        while coord in self:

            piece = self.square(coord)
            if not piece.is_blank():
                if piece.colour == side:
                    return piece
                else:
                    return None

            coord+= direction

        return None


    def row(self, row):

        """Returns the pieces in a given row."""

        for n in range(0, self.cols):
            yield self.square(Coord(n, row))


    def col(self, col):

        """Returns the pieces in a given column."""

        for n in range(0, self.rows):
            yield self.square(Coord(col, n))


    def row_pieces(self, row):

        """Returns all the pieces in a row."""

        for piece in self.row(row):
            if not piece.is_blank():
                yield piece


    def col_pieces(self, col):

        """Returns all the pieces in a column."""

        for piece in self.col(col):
            if not piece.is_blank():
                yield piece


    def unique_on_row(self, side, type, row):

        """Returns True if the piece is unique on a give row."""

        count = 0
        for piece in self.row_pieces(row):
            if piece.colour == side and piece.type == type:
                count+= 1
                if count > 1:
                    return False
        return True


    def unique_on_col(self, side, type, col):

        """Returns True if the piece is unique on a give column."""

        count = 0
        for piece in self.col_pieces(col):
            if piece.colour == side and piece.type == type:
                count+= 1
                if count > 1:
                    return False
        return True


    def board_visual(self):

        bv = []

        top = "  +-" + self.cols*"--" + "+"
        bv.append( top )

        for row in reversed(list(range(self.rows))):

            bv.append( ("%i | "%(row+1)) + " ".join( [str(self.square(Coord(col,row)).fen_letter()) for col in range(self.cols)] ) + " |")

        #bv.append( "  +-----------------+")
        bv.append( top )
        bv.append( "    "+" ".join(chr(ord('a')+n) for n in range(self.cols))+"  " )

        bvs = "\n".join(bv)

        return bvs


    def do_move(self, move):

        """Does a move."""

        piece = self.square(move.position)
        assert not piece.is_blank(), "There is no piece on this square!"

        self.half_move_count+= 1

        if move.is_capture() or piece.type == PAWN:
            self.half_move_count = 0

        piece.do_move(self, move)

        piece.last_move = self.move_count

        if piece.type == PAWN:
            self.pawn_move = self.move_count

        if move.promote is not None:

            promoted_piece = MakePiece(move.promote)
            promoted_piece.duplicate(piece)
            self.remove_piece(move.destination)
            self.place_piece(move.destination, promoted_piece)

        self.move_count+= 1

        self.last_move = move.clone()

        return self


    def move(self, move):

        """Does a move. Move can be either a Move class or movetext."""

        if isinstance(move, str):
            move = self.parse(move)

        return self.do_move(move)


    def __iter__(self):

        def square_generator(self):

            for row in range(self.rows):
                for col in range(self.cols):
                    yield self.squares[row][col]

        return square_generator(self)


    def occupied_squares(self, side=None):

        """Returns all the occupied (containing a piece) squares."""

        if side is None:
            def square_generator(self):
                for row in range(self.rows):
                    for col in range(self.cols):
                        piece = self.square(Coord(col, row))
                        #square = self.squares[col][row]
                        if not piece.is_blank():
                            yield square

            return square_generator(self)

        else:

            def square_generator(self, side):
                for row in range(self.rows):
                    for col in range(self.cols):
                        #square = self.squares[col][row]
                        piece = self.square(Coord(col, row))
                        if not piece.is_blank() and piece.colour == side:
                            yield piece

            return square_generator(self, side)


    def get_pieces(self, side, type):

        """Returns a list of all the pieces of a give side / type on the board."""

        return [piece for piece in self.occupied_squares(side=side) if piece.type == type]


    def get_potential_moves(self, side):

        """Returns a list of all potential moves."""

        moves = []

        for piece in self.occupied_squares(side):

            moves+= list(piece.potential_moves(self))

        return moves


    def potential_moves(self, side, type=None):

        """Generates potential moves for a given side / type."""

        if side is None:
            side = self.get_turn()

        def move_generator(self, side):

            for piece in self.occupied_squares(side):

                for move in piece.potential_moves(self):
                    yield move

        def move_generator_type(self, side, type):

            for piece in self.occupied_squares(side):

                if piece.type == type:
                    for move in piece.potential_moves(self):
                        yield move

        if type is None:
            return move_generator(self, side)
        else:
            return move_generator_type(self, side, type)


    def check_legal(self, move, side=None):

        """Return True if a move is legal."""

        if side is None:
            side = self.get_turn()
        test_board = self.clone()
        return not test_board.do_move(move).is_check(side)


    def legal_moves(self, side=None, type=None):

        """Generates legal moves."""

        if side is None:
            side = self.get_turn()

        def move_generator(self, side):

            for move in self.potential_moves(side):

                test_board = self.clone()
                if not test_board.do_move(move).is_check(side):
                    yield move

        def move_generator_type(self, side, type):

            for move in self.potential_moves(side):

                if self[move.position].type != type:
                    continue

                test_board = self.clone()
                if not test_board.do_move(move).is_check(side):
                    yield move

        if type is None:
            return move_generator(self, side)
        else:
            return move_generator_type(self, side, type)


    def any_legal_moves(self, side):

        """Returns True if there are any legal moves."""

        for move in self.legal_moves(side):

            return True

        return False


    def get_legal_moves(self, side, type):

        """Returns a list of legal moves."""

        return list(self.legal_moves(side, type))


    def is_attacked(self, coord, side):

        """Returns True if a piece on the given coordinate could be captured next turn."""

        for move in self.legal_moves(side):

            if move.destination == coord:
                return True

        return False


    def find_king(self, side):

        """Returns the King for a given side."""

        for piece in self.occupied_squares(side):

            if piece.type == KING:
                return piece

        return None


    def is_threatened(self, coord, side):

        """Return True if the given coordinate is threatened (even if actual move would be illegal)."""

        for piece in self.occupied_squares(side):

            if piece.can_potentialy_attack(self, coord):
                return True

        return False


    def is_check(self, side):

        """Return True if in check."""

        king_pos = self.find_king(side).position

        for direction in (LEFT, RIGHT, UP, DOWN, UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT):

            piece = self.piece_in_direction(king_pos, direction, Opponent(side))

            if piece is not None and piece.can_potentialy_attack(self, king_pos):
                return True

        for hop in Knight.MOVES:
            hop = Coord(*hop)
            if hop in self:
                piece = self[hop]
                if not piece.is_blank():
                    if piece.colour != side and piece.can_potentialy_attack(self, king_pos):
                        return True
        return False



        #for square in self.occupied_squares(Opponent(side)):
        #
        #    if square.piece.can_potentialy_attack(self, king_pos):
        #        return True
        #
        #return False

    def is_mate(self, side=None):

        if side is None:
            side = self.get_turn()

        """Return True if board is in mate position."""

        return self.is_check(side) and not self.any_legal_moves(side)


    def is_stalemate(self, side=None):

        """Return True if board is stalemated."""

        if side is None:
            side = self.get_turn()

        return not is_check(side) and not self.any_legal_moves(side)


    def check_result(self, side=None):

        """Returns the status of the board (ONGOING, MATE or STALEMATE)."""

        if side is None:
            side = self.get_turn()

        legal_moves = self.any_legal_moves(side)

        if legal_moves:
            return ONGOING

        if self.is_check(side):
            return MATE
        else:
            return STALEMATE


    def parse(self, movetext):

        move = self.parse_simple_move(movetext)

        if move is not None:
            return move

        move = self.parse_san(movetext)

        return move


    def parse_simple_move(self, movetext):

        """Attempts to parse a move in the form 'e2xe4', or returns None if it can't."""

        valid_chars = Board.PIECES + Board.RANKS + Board.FILES
        movetext = "".join(c for c in movetext if c in valid_chars and c is not " ")

        promote = None
        if len(movetext) == 5:

            promote = movetext[-1]
            if promote not in Board.PIECES:
                return None
            movetext = movetext[:-1]


        if len(movetext) == 4:

            from_pos = Coord.from_notation(movetext[0:2])
            dest_pos = Coord.from_notation(movetext[2:])

            if from_pos is not None and dest_pos is not None:

                for move in self.potential_moves(self.get_turn()):

                    if move.position == from_pos and move.destination == from_pos:

                        if promote is not None and move.promote is not promote:
                            continue

                        return move

        return None


    def parse_san(self, san):

        """parses a move in SAN format."""

        parse_text = san

        # First filter out non-significant characters..
        valid_chars = Board.PIECES + Board.RANKS + Board.FILES + 'oO='
        san = "".join(c for c in san if c in valid_chars and c != " ")

        san_piece = None
        san_col = None
        san_row = None
        san_promote = None
        san_destination = None


        if not len(san):

            raise ParseError("invalid", parse_text, "No significant characters")

        turn = self.get_turn()


        # 'O-O' is queenside castle, 'O-O-O' is kingside
        castle = "".join(c for c in san if c.lower()=='o')
        if len(castle) in (2,3):

            if len(castle) == 2:
                castle_side = Move.CASTLE_KINGSIDE
            else:
                castle_side = Move.CASTLE_QUEENSIDE

            king = self.find_king(turn)

            if king is None:

                raise ParseError("illegal move", parse_text, "No king?")

            #moves = filter(check_castle, king.get_potential_moves(self))
            moves = [move for move in king.potential_moves(self) if move.type == castle_side]

            if len(moves) != 1:

                moves = [move for move in moves if self.check_legal(move, side)]

            if len(moves) != 1:

                raise ParseError("illegal move", parse_text, "Unable to castle")

            return moves[0]


        piece_letter = san[0]

        if len(san) > 2 and piece_letter in Board.PIECES:

            san_piece = piece_letter.lower()
            san = san[1:]

        else:

            san_piece = PAWN


        # Get promotion
        if '=' in san:

            san, promote = san.split('=',1)

            if promote.upper() in Board.PIECES and promote.lower() != PAWN:

                san_promote = promote.lower()


        destination = Coord.from_notation(san[-2:])
        if destination is None or destination not in self:

            raise ParseError("destination error", parse_text, "Destination is not in the board")

        san_destination = destination


        san = san[0:-2]


        if len(san):

            rank_or_file = san[0]

            if rank_or_file in Board.RANKS:

                col = ord(rank_or_file) - ord('a')

                san_col = col

                san = san[1:]

        if len(san):

            rank_or_file = san[0]

            if rank_or_file in Board.FILES:

                row = ord(rank_or_file) - ord('1')

                san_row = row

                san = san[1:]

        moves = []
        for piece in self.occupied_squares(turn):

            def check(test, val):

                if test is None:
                    return True
                return test == val

            if not check(san_piece, piece.type):
                continue

            for move in piece.potential_moves(self):

                if ( check(san_destination, move.destination) and
                     check(san_col, move.position.col) and
                     check(san_row, move.position.row) and
                     check(san_promote, move.promote) ):
                    moves.append(move)

        if len(moves) != 1:

            moves = [move for move in moves if self.check_legal(move, turn)]


        if len(moves) == 0:

            raise ParseError("illegal move", parse_text, "This move is not possible")

        if len(moves) > 1:

            raise ParseError("ambiguous move", parse_text, "Could be more than 1 move")

        return moves[0]


    def full_move_count(self):

        """Returns the full move number. A full move consists of whites move and blacks response."""

        return (self.move_count+1)/2


    def fen(self, simple=False):

        """Returns a FEN string, that encodes the position of the board."""

        fen = []

        for row in reversed(list(range(self.rows))):

            fen_line = []
            blanks = 0

            for col in range(self.rows):
                coord = Coord(col, row)

                piece = self.square(coord)

                if piece.is_blank():
                    blanks+= 1
                else:
                    if blanks:
                        fen_line.append(str(blanks))
                        blanks = 0
                    fen_line.append(piece.fen_letter())

            if blanks:
                fen_line.append(str(blanks))

            fen.append("".join(fen_line))

        fen = "/".join(fen)

        if self.get_turn() == WHITE:
            turn_letter='w'
        else:
            turn_letter='b'

        wk = self.find_king(WHITE)
        bk = self.find_king(BLACK)

        castle = ""
        if wk is not None:
            if not wk.has_moved():
                qsr, ksr = wk.get_rooks(self)
                if ksr and not ksr.has_moved():
                    castle+= "K"
                if qsr and not qsr.has_moved():
                    castle+= "Q"

        if bk is not None:
            if not bk.has_moved():
                qsr, ksr = bk.get_rooks(self)
                if ksr and not ksr.has_moved():
                    castle+= "k"
                if qsr and not qsr.has_moved():
                    castle+= "q"

        if not len(castle):
            castle = "-"

        en_passant_target = "-"
        if self.last_move is not None:
            moved_square = self[self.last_move.destination]
            if not moved_square.is_blank():                
                if piece.type == PAWN and piece.just_moved(self):
                    if piece.is_white():
                        dir = UP
                    else:
                        dir = DOWN
                    en_passant = piece.position - dir
                    en_passant_target = str(en_passant)

        if simple:
            fen+= " %s %s %s"%(turn_letter, castle, en_passant_target)
        else:
            fen+= " %s %s %s %i %i"%(turn_letter, castle, en_passant_target, self.half_move_count, self.full_move_count())

        return fen


    def check_threefold_repetition(self, moves, initial_board):

        """Returns True if the current board state has been repeated 3 times."""

        board = initial_board.clone()

        board_fens = {}

        for move in moves:

            # Use fen as a convenient way to distinguish board positions
            fen = board.get_fen(simple=True)
            board_fens[fen] = board_fens.get(fen, 0) + 1

            if board_fens[fen] == 3:
                return True

        return False


    def check_fifty_move(self):

        """Return True if there have been 50 moves since the last capture or pawn move."""

        return self.half_move_count > 50



class Move(object):

    """Contains the information to describe a single move."""

    PLAIN, CASTLE_QUEENSIDE, CASTLE_KINGSIDE, EN_PASSANT= list(range( 4))

    def __init__(self, position=None, destination=None, type=PLAIN, promote=None, capture=None):

        self.position = position
        self.destination = destination
        self.type = type
        self.promote = promote
        self.capture = capture


    def clone(self):

        ret = Move()
        ret.position = self.position
        ret.destination = self.destination
        ret.type = self.type
        ret.promote = self.promote
        ret.capture = self.capture
        return ret


    def promote_to(self, promote):

        self.promote = promote
        return self


    def is_castle(self):

        return self.type == Move.CASTLE_QUEENSIDE or self.type == Move.CASTLE_KINGSIDE


    def is_capture(self):

        return self.capture is not None


    def __str__(self):

        if self.capture:
            smove = "%sx%s"%(str(self.position), str(self.destination))
        else:
            smove = "%s-%s"%(str(self.position), str(self.destination))
        if self.type == Move.CASTLE_QUEENSIDE:
            smove+= " (castle queenside)"
        elif self.type == Move.CASTLE_KINGSIDE:
            smove+= " (castle kingside)"
        elif self.type == Move.EN_PASSANT:
            smove+= " (en passant)"

        if self.promote is not None:
            smove+= " "+"(promote %s)"%(PIECE_NAMES[self.promote])

        return smove


    def san(self, board, decorate=True):

        piece = board[self.position]

        if self.type == Move.CASTLE_QUEENSIDE:
            return 'O-O-O'
        elif self.type == Move.CASTLE_KINGSIDE:
            return 'O-O'

        promote = ""
        if self.promote is not None:
            promote = "="+self.promote.upper()

        pos = str(self.position)
        dest = str(self.destination)

        piece_letter = ""
        if piece.type != PAWN:
            piece_letter = piece.type.upper()

        def ambiguous_move():
            count = 0
            for move in board.potential_moves(board.get_turn(), piece.type):

                if move.destination == self.destination:
                    count+=1
                    if count > 1:
                        return True
            return False

        if not ambiguous_move():
            from_coord = ""
        else:
            from_coord = ""
            if board.unique_on_col(piece.colour, piece.type, self.position.col):
                from_coord+= pos[0]
            elif board.unique_on_row(piece.colour, piece.type, self.position.row):
                from_coord+= pos[1]

        capture = ""
        if self.is_capture():
            if piece.type == PAWN:
                if len(from_coord):
                    capture = 'x'
            else:
                capture = 'x'

        san = "".join((piece_letter, from_coord, capture, dest, promote))

        if decorate:

            test_board = board.clone().do_move(self)

            san_decorate = ''
            is_check = test_board.is_check(test_board.get_turn())
            if is_check:
                san_decorate= '+'

            if is_check and not test_board.any_legal_moves(test_board.get_turn()):
                san_decorate= '#'

            san+= san_decorate

        return san



class Game(object):

    """Contains information to describe a chess game.
    Including the board, all the moves and external information - such as player info."""

    tag_re = re.compile("""\[(.*)(".*")\]""")

    RESULTS = ("1-0", "0-1", "*")

    def __init__(self):

        self.board = Board()

        self.tags = {}
        self.movetext = ""
        self.moves = []


    def setup(self):

        self.board = self.initial_board()


    def reset(self):

        self.setup()
        self.moves=[]


    def initial_board(self):

        board = Board()
        board.setup(INITIAL_BOARD)
        return board


    def import_pgn(self, pgn_file, parse_movetext=True):

        # Read tags
        for line in pgn_file:

            line = line.strip()

            match = Game.tag_re.match(line)

            if match is None:
                break

            tag_tokens = Game.tag_re.match(line).groups()

            if len(tag_tokens) >= 2:

                tag_name = tag_tokens[0].strip()
                tag_value = tag_tokens[1].strip('"')

                print(tag_name, tag_value)

                self.tags[tag_name] = tag_value

        if not len(self.tags):
            return False

        found_movetext = False

        mt = []

        #Read move text
        for line in pgn_file:

            line = line.strip()

            if not len(line) and found_movetext:

                break

            if len(line) > 0:

                found_movetext = True

                mt.append(line)

        self.movetext = " ".join(mt)

        if parse_movetext:
            self.parse_movetext()

        return True


    def export_pgn(self, file_pgn):

        for tag, value in self.tags.items():

            file_pgn.write('[%s "%s"]\n'%(tag, value))

        file_pgn.write('\n')

        MAX_LINE = 80

        board = self.initial_board()
        san_line = ""
        for moveno, move in enumerate(self.moves):

            san = move.san(board, decorate=False)
            board.do_move(move)

            movetext = ""
            if not (moveno & 1):
                half_move = 1 + (moveno / 2)
                movetext = '%i. %s'%(half_move, san)
            else:
                movetext = san

            decorate = ''

            is_check = board.is_check(board.get_turn())

            if is_check:
                decorate = '+'

            if is_check and moveno == len(self.moves)-1:
                if not board.any_legal_moves(board.get_turn()):
                    decorate = '#'

            movetext += decorate

            if len(san_line) + len(movetext) > MAX_LINE:
                file_pgn.write("%s\n"%san_line[:-1])
                san_line = movetext+' '
            else:
                san_line += movetext+' '

        if len(san_line):
            file_pgn.write("%s\n"%san_line[:-1])

        file_pgn.write( "\n" )


    def parse_movetext(self):

        self.board = Board()
        self.board.setup(INITIAL_BOARD)

        for token in self.movetext.split():

            num = None
            try:
                num = float(token)
            except:
                pass

            if num is None:

                move = None

                if token in Game.RESULTS:
                    break

                try:
                    move = self.board.parse_san(token)
                except ParseError as e:
                    break

                if move is not None:

                    self.board.do_move(move)
                    self.moves.append(move)


    def move(self, move):

        if isinstance(move, str):
            try:
                move = self.board.parse(movetext)
            except ParseError as error:
                return False

        if not self.board.check_legal(move):
            return False

        self.moves.append(move)
        self.board.do_move(move)

        return True



def Adjudicate():


    commands = "exit help reset board fen legal moves captures pgn".split()
    commands.sort()

    game = Game()
    game.setup()

    ongoing = True

    def show():
        print(game.board)
        #if game.board.get_turn() == WHITE:
        #    print "BLACK to move"
        #else:
        #    print "BLACK to move"

    show()

    while True:

        if game.board.get_turn() == WHITE:
            prompt = "%i. "%game.board.full_move_count()
        else:
            prompt = "%i. ... "%game.board.full_move_count()

        line = input(prompt)

        if not len(line):
            show()
            continue

        # Test for a command first
        param=None
        cmd = line.lower()
        if " " in cmd:
            cmd, param = cmd.split(" ",1)
        if cmd == "exit":
            break
        if cmd == "help":
            for word in commands:
                print(word)
            continue
        elif cmd == "reset":
            game.reset()
            ongoing = True
            print(game.board)
            continue
        elif cmd == "board":
            show()
            continue
        elif cmd == "fen":
            print(game.board.fen())
            continue
        elif cmd == "legal":
            for move in game.board.legal_moves():
                #print move
                print(move.san(game.board))
            continue
        elif cmd == "moves":
            for move in game.moves:
                print(move)
            continue
        elif cmd == "captures":
            for piece in game.board.captures:
                print(piece)
            continue
        elif cmd == "pgn":
            if not param:
                print("Filename required")
                continue
            else:
                try:
                    game.export_pgn(file(param, "w+"))
                except:
                    print("Unable to write", param)
                    continue
            print("Written", param)
            continue

        if not ongoing:
            print("Type reset for a new game.")
            continue

        # If its not a command we will assume its a move
        move = None
        try:
            move = game.board.parse(line)
        except ParseError as error:
            print(error)
            continue

        if not game.move(move):
            print("Illegal move")
            continue

        show()

        result = game.board.check_result()
        if result == MATE:
            print("Checkmate!")
            ongoing = False
        elif result == STALEMATE:
            print("Stalemate")
            ongoing = False

class echec():
    
    nom = "echec"
    max_joueur = 2
    
    def jouer(self, joueur, msg):
        print(joueur, msg)
    
"""
if __name__ == "__main__":

    Adjudicate()


    #file_pgn = file("john.pgn")
    #
    #while True:
    #    game = Game()
    #    if not game.import_pgn(file_pgn):
    #        break
    #    print game.board

"""
