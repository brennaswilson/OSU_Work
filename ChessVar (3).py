# Author: Brenna Wilson
# GitHub username: brennaswilson
# Date: 3/13/24
# Description: chess game, follows basic rules, includes two extra "Fairy" pieces, does not include check or checkmate,
# and there is no castling, en passant, or pawn promotion

class ChessVar:
    """sets up rules and controls game"""

    def __init__(self):
        self._game_state = 'UNFINISHED'
        self._turn = 'w'
        self._board = [
            [Rook('w'), Knight('w'), Bishop('w'), Queen('w'), King('w'), Bishop('w'), Knight('w'), Rook('w')],
            [Pawn('w'), Pawn('w'), Pawn('w'), Pawn('w'), Pawn('w'), Pawn('w'), Pawn('w'), Pawn('w')],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [Pawn('b'), Pawn('b'), Pawn('b'), Pawn('b'), Pawn('b'), Pawn('b'), Pawn('b'), Pawn('b')],
            [Rook('b'), Knight('b'), Bishop('b'), Queen('b'), King('b'), Bishop('b'), Knight('b'), Rook('b')]
        ]
        self._white_player_lost_pieces = []
        self._black_player_lost_pieces = []
        self._fairy_pieces_white = ['Falcon', 'Hunter']
        self._fairy_pieces_black = ['Falcon', 'Hunter']

    def get_board(self):
        """returns current state of chess board"""
        return self._board

    def get_game_state(self):
        """returns 'UNFINISHED', 'WHITE_WON', or 'BLACK_WON' based on current state of game"""
        return self._game_state

    def get_turn(self):
        """returns which player's turn it is (white or black, game always starts with white)"""
        return self._turn

    def make_move(self, square_from, square_to):
        """takes in square moved from and to, returns False if: contains piece that is not players, move is not legal
        game was already won
        Else: indicate move, remove any captured piece, update game state as necessary, update turn, and return True
        Needs each Chess Piece subclass, valid_move function to execute as intended"""

        # convert squares from string to indices
        from_col = ord(square_from[0]) - 97     # convert letter to column number using ASCII nums, change to 1-8
        from_row = int(square_from[1:]) - 1
        to_col = ord(square_to[0]) - 97       # convert letter to column number using ASCII nums, change to 1-8
        to_row = int(square_to[1:]) - 1

        # return False if valid_move returns False, else, move piece and capture piece as necessary
        if not self.valid_move(from_col, from_row, to_col, to_row):
            return False
        else:
            from_chess_piece = self._board[from_row][from_col]
            to_chess_piece = self._board[to_row][to_col]
            if to_chess_piece is None:
                self._board[to_row][to_col] = self._board[from_row][from_col]
                self._board[from_row][from_col] = None
            else:
                captured_piece = self._board[to_row][to_col]
                self._board[to_row][to_col] = self._board[from_row][from_col]
                self._board[from_row][from_col] = None
                current_color = from_chess_piece.get_color()
                if current_color == 'b':
                    self._white_player_lost_pieces.append(captured_piece)
                else:
                    self._black_player_lost_pieces.append(captured_piece)

        # check if king was captured, if so, change game state to reflect who won
        for pieces in self._white_player_lost_pieces:
            if isinstance(pieces, King):
                self._game_state = "BLACK_WON"
        for pieces in self._black_player_lost_pieces:
            if isinstance(pieces, King):
                self._game_state = "WHITE_WON"

        # update player turn
        if self._turn == 'w':
            self._turn = 'b'
            return True
        else:
            self._turn = 'w'
            return True

    def enter_fairy_piece(self, piece, square_to):
        """takes in fairy piece to be entered and at which square. If position is not possible,
        or fairy piece is not playable, returns False
        Else: update board, update turn, and return True"""

        # to square is not empty
        to_col = ord(square_to[0]) - 97  # convert letter to column number using ASCII nums, change to 1-8
        to_row = int(square_to[1:]) - 1

        if self._board[to_row][to_col] is not None:
            return False

        # calls get_playable from FairyPiece subclass to see if player can use fairy piece yet

        needed_pieces_white = 0
        needed_pieces_black = 0

        for pieces in self._white_player_lost_pieces:
            if isinstance(pieces, (Queen, Knight, Bishop)):
                needed_pieces_white += 1
        for pieces in self._black_player_lost_pieces:
            if isinstance(pieces, (Queen, Knight, Bishop)):
                needed_pieces_black += 1

        # at least one fairy piece is available
        if self._turn == 'w':
            if needed_pieces_white == 0:
                return False
            else:
                pass
        else:
            if needed_pieces_black == 0:
                return False
            else:
                pass

        # at least one fairy piece can be played at this point

        # return False if fairy piece is already in play
        if self._turn == 'w':
            if piece == 'Falcon':
                if "Falcon" in self._fairy_pieces_white:
                    pass
                else:
                    return False
        if self._turn == 'w':
            if piece == 'Hunter':
                if "Hunter" in self._fairy_pieces_white:
                    pass
                else:
                    return False
        if self._turn == 'b':
            if piece == 'Falcon':
                if "Falcon" in self._fairy_pieces_black:
                    pass
                else:
                    return False

        if self._turn == 'b':
            if piece == 'Hunter':
                if "Hunter" in self._fairy_pieces_black:
                    pass
                else:
                    return False

        # return False if one Fairy piece is in and not qualified to enter second fairy piece yet
        # or no fairy pieces left, else continue on
        fairy_pieces_remaining = 0

        if self._turn == 'w':
            for pieces in self._fairy_pieces_white:
                fairy_pieces_remaining += 1
            if fairy_pieces_remaining == 0:
                return False  # no fairy pieces left to play
            if fairy_pieces_remaining == 1 and needed_pieces_white > 1:
                pass
            if fairy_pieces_remaining == 2 and needed_pieces_white >= 1:
                pass
            else:
                return False
        if self._turn == 'b':
            for pieces in self._fairy_pieces_black:
                fairy_pieces_remaining += 1
            if fairy_pieces_remaining == 0:
                return False            # no fairy pieces left to play
            if fairy_pieces_remaining == 1 and needed_pieces_black > 1:
                pass
            if fairy_pieces_remaining == 2 and needed_pieces_black >= 1:
                pass
            else:
                return False

        # call make_move if everything else has not returned False
        if self._turn == 'w':
            if piece == 'Falcon':
                self._board[to_row][to_col] = Falcon('w')
                self._fairy_pieces_white.remove('Falcon')

            if piece == 'Hunter':
                self._fairy_pieces_white.remove('Hunter')
                self._board[to_row][to_col] = Hunter('w')

        if self._turn == 'b':
            if piece == 'Falcon':
                self._fairy_pieces_black.remove('Falcon')
                self._board[to_row][to_col] = Falcon('b')
            if piece == 'Hunter':
                self._fairy_pieces_black.remove('Hunter')
                self._board[to_row][to_col] = Hunter('b')

        if self._turn == 'w':
            self._turn = 'b'
            return True
        else:
            self._turn = 'w'
            return True

    def valid_move(self, from_col, from_row, to_col, to_row):
        """takes in parameters from make_mov and returns True if move is valid, else returns False
        will be fed parameters from make_move function"""

        from_square = [from_row, from_col]
        to_square = [to_row, to_col]

        # return False if game is won
        if self._game_state != 'UNFINISHED':
            return False

        # return False if either square is out of bounds
        if from_col < 0 or from_col > 7:  # square_from col is out of bounds
            return False
        if from_row < 0 or from_row > 7:  # square_from row is out of bounds
            return False
        if to_col < 0 or to_col > 7:  # square_to col is out of bounds
            return False
        if to_row < 0 or to_row > 7:  # square_to row is out of bounds
            return False

        # chess_piece variable
        chess_piece = self._board[from_row][from_col]

        # return False if square_from is empty
        if chess_piece is None:
            return False

        # return False if square_from does not have current player's piece
        if chess_piece.get_color() != self._turn:
            return False

        # return False if square_to has current player's piece
        to_chess_piece = self._board[to_row][to_col]
        if to_chess_piece is not None:
            if to_chess_piece.get_color() == self._turn:
                return False

        # get list of all possible moves (includes spaces off board and w/ pieces on it)
        possible_squares = chess_piece.piece_move(from_col, from_row, self._board, self._turn)

        # if to_square not in possible_squares, return False
        if to_square not in possible_squares:
            return False

        # no False's, return to make_move
        return True


class ChessPiece:
    """chess piece class, initialize variables and functions needed for all chess pieces"""

    def __init__(self, color, piece_name):
        self._current_square = ''
        self._color = color
        self._piece_name = piece_name

    def get_name(self):
        """returns name of piece"""
        return self._piece_name

    def get_current_square(self):
        """returns square that piece is on"""
        return self._current_square

    def get_color(self):
        """returns color of piece"""
        return self._color

    def check_range(self, to_row, to_col):
        """helper function if a possible to_Square is out of range"""
        if to_row > 7 or to_row < 0:
            return False
        if to_col > 7 or to_col < 0:
            return False
        else:
            return True


class Pawn(ChessPiece):
    """represents pawn chess piece, inherits from ChessPiece class, color and name specific attributes"""

    def __init__(self, color):
        super().__init__(color, "Pawn")

    def piece_move(self, from_col, from_row, board, turn):
        """passed from_square from valid_move function, returns list of all possible squares piece could move to"""

        possible_squares = []           # list of all possible moves

        # determine if pawn is white (bottom of game board)
        if self._color == 'w':

            if not self.check_range(from_row + 1, from_col + 1):
                pass
            else:
                # if square in front is empty
                if board[from_row + 1][from_col] is None:
                    possible_squares.append([from_row + 1, from_col])

            if not self.check_range(from_row + 1, from_col + 1):
                pass
            else:
                # determine if enemy piece in upper right
                if board[from_row + 1][from_col + 1] is not None:
                    upper_right = board[from_row + 1][from_col + 1]
                    if upper_right.get_color() != self.get_color():
                        possible_squares.append([from_row + 1, from_col + 1])

            if not self.check_range(from_row + 1, from_col - 1):
                pass
            else:
                # determine if enemy piece upper left
                if board[from_row + 1][from_col - 1] is not None:
                    upper_left = board[from_row + 1][from_col - 1]
                    if upper_left.get_color() != self.get_color():
                        possible_squares.append([from_row + 1, from_col - 1])

            # determine if pawn is in starting position, thus gets to move up 2 spaces (if no piece there)
            if board[from_row + 2][from_col] is None:
                possible_squares.append([from_row + 2, from_col])
            else:
                pass

        # determine if pawn is black (top of game board)
        if self._color == 'b':

            # if square in front is empty, moves on if square is out of bounds
            if not self.check_range(from_row - 1, from_col):
                pass
            else:
                if board[from_row - 1][from_col] is None:
                    possible_squares.append([from_row - 1, from_col])

            # determine if enemy piece in upper right, moves on if square is out of bounds
            if not self.check_range(from_row - 1, from_col + 1):
                pass
            else:
                if (board[from_row - 1][from_col + 1]) is not None:
                    bottom_right = board[from_row - 1][from_col + 1]
                    if bottom_right.get_color() != self.get_color():
                        possible_squares.append([from_row - 1, from_col + 1])

            # determine if enemy piece upper left, moves on if square is out of bounds
            if not self.check_range(from_row - 1, from_col - 1):
                pass
            else:
                if board[from_row - 1][from_col - 1] is not None:
                    bottom_left = board[from_row - 1][from_col - 1]
                    if bottom_left.get_color() != self.get_color():
                        possible_squares.append([from_row - 1, from_col - 1])

            # determine if pawn is in starting position, thus gets to move down 2 spaces (and no piece there)
            if from_row == 6:
                if board[from_row - 2][from_col] is None:
                    possible_squares.append([from_row - 2, from_col])
                else:
                    pass

        # return list of all possible square moves
        return possible_squares


class Knight(ChessPiece):
    """represents Knight chess piece, inherits from ChessPiece class, color and name specific attributes"""
    
    def __init__(self, color):
        super().__init__(color, "Knight")

    def piece_move(self, from_col, from_row, board, turn):
        """passed from_square from valid_move function, returns list of all possible squares piece could move to"""

        possible_squares = []

        # square 2 up and 1 right
        if not self.check_range(from_row + 2, from_col + 1):
            pass
        else:
            if board[from_row + 2][from_col + 1] is None or board[from_row + 2][from_col + 1].get_color() != turn:
                possible_squares.append([from_row + 2, from_col + 1])

        # square 2 right 1 up
        if not self.check_range(from_row + 1, from_col + 2):
            pass
        else:
            if board[from_row + 1][from_col + 2] is None or board[from_row + 1][from_col + 2].get_color() != turn:
                possible_squares.append([from_row + 1, from_col + 2])

        # square 2 right 1 down
        if not self.check_range(from_row - 1, from_col + 2):
            pass
        else:
            if board[from_row - 1][from_col + 2] is None or board[from_row - 1][from_col + 2].get_color() != turn:
                possible_squares.append([from_row - 1, from_col + 2])

        # square 2 down one right
        if not self.check_range(from_row - 2, from_col + 1):
            pass
        else:
            if board[from_row - 2][from_col + 1] is None or board[from_row - 2][from_col + 1].get_color() != turn:
                possible_squares.append([from_row - 2, from_col + 1])

        # square 2 down one left
        if not self.check_range(from_row -2, from_col - 1):
            pass
        else:
            if board[from_row - 2][from_col - 1] is None or board[from_row - 2][from_col - 1].get_color() != turn:
                possible_squares.append([from_row - 2, from_col - 1])

        # square 2 left one down
        if not self.check_range(from_row - 1, from_col - 2):
            pass
        else:
            if board[from_row - 1][from_col - 2] is None or board[from_row - 1][from_col - 2].get_color() != turn:
                possible_squares.append([from_row - 1, from_col - 2])

        # square 2 left one up
        if not self.check_range(from_row + 1, from_col - 2):
            pass
        else:
            if board[from_row + 1][from_col - 2] is None or board[from_row + 1][from_col - 2].get_color() != turn:
                possible_squares.append([from_row + 1, from_col - 2])

        # square 2 up 1 left
        if not self.check_range(from_row + 2, from_col - 1):
            pass
        else:
            if board[from_row + 2][from_col - 1] is None or board[from_row + 2][from_col - 1].get_color() != turn:
                possible_squares.append([from_row + 2, from_col - 1])

        return possible_squares


class Bishop(ChessPiece):
    """represents Bishop chess piece, inherits from ChessPiece class, color and name specific attributes"""
    
    def __init__(self, color):
        super().__init__(color, "Bishop")

    def piece_move(self, from_col, from_row, board, turn):
        """"passed from_square from valid_move function, returns list of all possible squares piece could move to"""
        possible_squares = []

        # diagonal going up and right
        new_row = from_row
        new_col = from_col
        for col in range(from_col, 8):
            new_row += 1
            new_col += 1
            if not self.check_range(new_row, new_col):
                break
            else:
                if board[new_row][new_col] is None:
                    possible_squares.append([new_row, new_col])
                elif board[new_row][new_col].get_color() != turn:
                    possible_squares.append([new_row, new_col])
                    break
                else:
                    break

        # diagonal going down and right
        new_row = from_row
        new_col = from_col
        for col in range(from_col, 8):
            new_row -= 1
            new_col += 1
            if not self.check_range(new_row, new_col):
                break
            else:
                if board[new_row][new_col] is None:
                    possible_squares.append([new_row, new_col])
                elif board[new_row][new_col].get_color() != turn:
                    possible_squares.append([new_row, new_col])
                    break
                else:
                    break

        # diagonal going left and up
        new_row = from_row
        new_col = from_col
        for col in range(from_col, -1, -1):
            new_row += 1
            new_col -= 1
            if not self.check_range(new_row, new_col):
                break
            else:
                if board[new_row][new_col] is None:
                    possible_squares.append([new_row, new_col])
                elif board[new_row][new_col].get_color() != turn:
                    possible_squares.append([new_row, new_col])
                    break
                else:
                    break

        # diagonal going left and down
        new_row = from_row
        new_col = from_col
        for col in range(from_col, -1, -1):
            new_row -= 1
            new_col -= 1
            if not self.check_range(new_row, new_col):
                break
            else:
                if board[new_row][new_col] is None:
                    possible_squares.append([new_row, new_col])
                elif board[new_row][new_col].get_color() != turn:
                    possible_squares.append([new_row, new_col])
                    break
                else:
                    break

        return possible_squares


class King(ChessPiece):
    """represents King chess piece, inherits from ChessPiece class, color and name specific attributes"""
    
    def __init__(self, color):
        super().__init__(color, "King")

    def piece_move(self, from_col, from_row, board, turn):
        """passed from_square from valid_move function, returns list of all possible squares piece could move to"""

        possible_squares = []

        # square above
        if not self.check_range(from_row + 1, from_col):
            pass
        else:
            if board[from_row + 1][from_col] is None or board[from_row + 1][from_col].get_color() != turn:
                possible_squares.append([from_row + 1, from_col])

        # square below
        if not self.check_range(from_row - 1, from_col):
            pass
        else:
            if board[from_row - 1][from_col] is None or board[from_row - 1][from_col].get_color() != turn:
                possible_squares.append([from_row - 1, from_col])

        # square to right
        if not self.check_range(from_row, from_col + 1):
            pass
        else:
            if board[from_row][from_col + 1] is None or board[from_row][from_col + 1].get_color() != turn:
                possible_squares.append([from_row, from_col + 1])

        # square to left
        if not self.check_range(from_row, from_col - 1):
            pass
        else:
            if board[from_row][from_col - 1] is None or board[from_row][from_col - 1].get_color() != turn:
                possible_squares.append([from_row, from_col - 1])

        # square diagonal top right
        if not self.check_range(from_row + 1, from_col + 1):
            pass
        else:
            if board[from_row + 1][from_col + 1] is None or board[from_row + 1][from_col + 1].get_color() != turn:
                possible_squares.append([from_row + 1, from_col + 1])

        # square diagonal top left
        if not self.check_range(from_row + 1, from_col - 1):
            pass
        else:
            if board[from_row + 1][from_col - 1] is None or board[from_row + 1][from_col - 1].get_color() != turn:
                possible_squares.append([from_row + 1, from_col - 1])

        # square diagonal bottom right
        if not self.check_range(from_row - 1, from_col + 1):
            pass
        else:
            if board[from_row - 1][from_col + 1] is None or board[from_row - 1][from_col + 1].get_color() != turn:
                possible_squares.append([from_row - 1, from_col + 1])

        # square diagonal bottom left
        if not self.check_range(from_row - 1, from_col - 1):
            pass
        else:
            if board[from_row - 1][from_col - 1] is None or board[from_row - 1][from_col - 1].get_color() != turn:
                possible_squares.append([from_row - 1, from_col - 1])

        return possible_squares


class Rook(ChessPiece):
    """represents rook chess piece, inherits from ChessPiece class, color and name specific attributes"""
    
    def __init__(self, color):
        super().__init__(color, "Rook")

    def piece_move(self, from_col, from_row, board, turn):
        """passed from_square from valid_move function, returns list of all possible squares piece could move to"""
        
        possible_squares = []

        #go right
        new_row = from_row
        new_col = from_col
        for col in range(from_col, 8):
            new_col += 1
            if not self.check_range(new_row, new_col):
                pass
            else:
                if board[new_row][new_col] is None:
                    possible_squares.append([new_row, new_col])
                elif board[new_row][new_col].get_color() != turn:
                    possible_squares.append([new_row, new_col])
                    break
                else:
                    break

        # go left
        new_row = from_row
        new_col = from_col
        for col in range(from_col, -1, -1):
            new_col -= 1
            if not self.check_range(new_row, new_col):
                pass
            else:
                if board[new_row][new_col] is None:
                    possible_squares.append([new_row, new_col])
                elif board[new_row][new_col].get_color() != turn:
                    possible_squares.append([new_row, new_col])
                    break
                else:
                    break

        # go up
        new_row = from_row
        new_col = from_col
        for row in range(from_row, 8):
            new_row += 1
            if not self.check_range(new_row, new_col):
                pass
            else:
                if board[new_row][new_col] is None:
                    possible_squares.append([new_row, new_col])
                elif board[new_row][new_col].get_color() != turn:
                    possible_squares.append([new_row, new_col])
                    break
                else:
                    break

        # go down
        new_row = from_row
        new_col = from_col
        for row in range(from_row, -1, -1):
            new_row -= 1
            if not self.check_range(new_row, new_col):
                pass
            else:
                if board[new_row][new_col] is None:
                    possible_squares.append([new_row, new_col])
                elif board[new_row][new_col].get_color() != turn:
                    possible_squares.append([new_row, new_col])
                    break
                else:
                    break

        return possible_squares


class Queen(ChessPiece):
    """represents Queen chess piece, inherits from ChessPiece class, color and name specific attributes"""

    def __init__(self, color):
        super().__init__(color, "Queen")

    def piece_move(self, from_col, from_row, board, turn):
        """passed from_square from valid_move function, returns list of all possible squares piece could move to"""

        possible_squares = []

        # go right
        new_row = from_row
        new_col = from_col
        for col in range(from_col, 8):
            new_col += 1
            if not self.check_range(new_row, new_col):
                pass
            else:
                if board[new_row][new_col] is None:
                    possible_squares.append([new_row, new_col])
                elif board[new_row][new_col].get_color() != turn:
                    possible_squares.append([new_row, new_col])
                    break
                else:
                    break

        # go left
        new_row = from_row
        new_col = from_col
        for col in range(from_col, -1, -1):
            new_col -= 1
            if not self.check_range(new_row, new_col):
                pass
            else:
                if board[new_row][new_col] is None:
                    possible_squares.append([new_row, new_col])
                elif board[new_row][new_col].get_color() != turn:
                    possible_squares.append([new_row, new_col])
                    break
                else:
                    break

        # go up
        new_row = from_row
        new_col = from_col
        for row in range(from_row, 8):
            new_row += 1
            if not self.check_range(new_row, new_col):
                pass
            else:
                if board[new_row][new_col] is None:
                    possible_squares.append([new_row, new_col])
                elif board[new_row][new_col].get_color() != turn:
                    possible_squares.append([new_row, new_col])
                    break
                else:
                    break

        # go down
        new_row = from_row
        new_col = from_col
        for row in range(from_row, -1, -1):
            new_row -= 1
            if not self.check_range(new_row, new_col):
                pass
            else:
                if board[new_row][new_col] is None:
                    possible_squares.append([new_row, new_col])
                elif board[new_row][new_col].get_color() != turn:
                    possible_squares.append([new_row, new_col])
                    break
                else:
                    break

        # diagonal going up and right
        new_row = from_row
        new_col = from_col
        for col in range(from_col, 8):
            new_row += 1
            new_col += 1
            if not self.check_range(new_row, new_col):
                break
            else:
                if board[new_row][new_col] is None:
                    possible_squares.append([new_row, new_col])
                elif board[new_row][new_col].get_color() != turn:
                    possible_squares.append([new_row, new_col])
                    break
                else:
                    break

        # diagonal going down and right
        new_row = from_row
        new_col = from_col
        for col in range(from_col, 8):
            new_row -= 1
            new_col += 1
            if not self.check_range(new_row, new_col):
                break
            else:
                if board[new_row][new_col] is None:
                    possible_squares.append([new_row, new_col])
                elif board[new_row][new_col].get_color() != turn:
                    possible_squares.append([new_row, new_col])
                    break
                else:
                    break

        # diagonal going left and up
        new_row = from_row
        new_col = from_col
        for col in range(from_col, -1, -1):
            new_row += 1
            new_col -= 1
            if not self.check_range(new_row, new_col):
                break
            else:
                if board[new_row][new_col] is None:
                    possible_squares.append([new_row, new_col])
                elif board[new_row][new_col].get_color() != turn:
                    possible_squares.append([new_row, new_col])
                    break
                else:
                    break

        # diagonal going left and down
        new_row = from_row
        new_col = from_col
        for col in range(from_col, -1, -1):
            new_row -= 1
            new_col -= 1
            if not self.check_range(new_row, new_col):
                break
            else:
                if board[new_row][new_col] is None:
                    possible_squares.append([new_row, new_col])
                elif board[new_row][new_col].get_color() != turn:
                    possible_squares.append([new_row, new_col])
                    break
                else:
                    break

        return possible_squares


class Falcon(ChessPiece):
    """represents Falcon Fairy piece, inherits from ChessPiece, color and name specific attributes"""

    def __init__(self, color):
        super().__init__(color, "Falcon")

    def piece_move(self, from_col, from_row, board, turn):
        """"passed from_square from valid_move function, returns list of all possible squares piece could move to"""
        possible_squares = []

        if self._color == 'w':
            # diagonal going up and right
            new_row = from_row
            new_col = from_col
            for col in range(from_col, 8):
                new_row += 1
                new_col += 1
                if not self.check_range(new_row, new_col):
                    break
                else:
                    if board[new_row][new_col] is None:
                        possible_squares.append([new_row, new_col])
                    elif board[new_row][new_col].get_color() != turn:
                        possible_squares.append([new_row, new_col])
                        break
                    else:
                        break

            # diagonal going left and up
            new_row = from_row
            new_col = from_col
            for col in range(from_col, -1, -1):
                new_row += 1
                new_col -= 1
                if not self.check_range(new_row, new_col):
                    break
                else:
                    if board[new_row][new_col] is None:
                        possible_squares.append([new_row, new_col])
                    elif board[new_row][new_col].get_color() != turn:
                        possible_squares.append([new_row, new_col])
                        break
                    else:
                        break
            # go down
            new_row = from_row
            new_col = from_col
            for row in range(from_row, -1, -1):
                new_row -= 1
                if not self.check_range(new_row, new_col):
                    pass
                else:
                    if board[new_row][new_col] is None:
                        possible_squares.append([new_row, new_col])
                    elif board[new_row][new_col].get_color() != turn:
                        possible_squares.append([new_row, new_col])
                        break
                    else:
                        break

            return possible_squares

        if self._color == 'b':

            # diagonal going down and right
            new_row = from_row
            new_col = from_col
            for col in range(from_col, 8):
                new_row -= 1
                new_col += 1
                if not self.check_range(new_row, new_col):
                    break
                else:
                    if board[new_row][new_col] is None:
                        possible_squares.append([new_row, new_col])
                    elif board[new_row][new_col].get_color() != turn:
                        possible_squares.append([new_row, new_col])
                        break
                    else:
                        break

            # diagonal going left and down
            new_row = from_row
            new_col = from_col
            for col in range(from_col, -1, -1):
                new_row -= 1
                new_col -= 1
                if not self.check_range(new_row, new_col):
                    break
                else:
                    if board[new_row][new_col] is None:
                        possible_squares.append([new_row, new_col])
                    elif board[new_row][new_col].get_color() != turn:
                        possible_squares.append([new_row, new_col])
                        break
                    else:
                        break

            # go up
            new_row = from_row
            new_col = from_col
            for row in range(from_row, 8):
                new_row += 1
                if not self.check_range(new_row, new_col):
                    pass
                else:
                    if board[new_row][new_col] is None:
                        possible_squares.append([new_row, new_col])
                    elif board[new_row][new_col].get_color() != turn:
                        possible_squares.append([new_row, new_col])
                        break
                    else:
                        break

            return possible_squares


class Hunter(ChessPiece):
    """represents Hunter Fairy piece, inherits from ChessPiece , color and name specific attributes"""
    
    def __init__(self, color):
        super().__init__(color, "Hunter")

    def piece_move(self, from_col, from_row, board, turn):
        """passed from_square from valid_move function, returns list of all possible squares piece could move to"""
        possible_squares = []

        if self._color == 'w':

            # diagonal going down and right
            new_row = from_row
            new_col = from_col
            for col in range(from_col, 8):
                new_row -= 1
                new_col += 1
                if not self.check_range(new_row, new_col):
                    break
                else:
                    if board[new_row][new_col] is None:
                        possible_squares.append([new_row, new_col])
                    elif board[new_row][new_col].get_color() != turn:
                        possible_squares.append([new_row, new_col])
                        break
                    else:
                        break

            # diagonal going left and down
            new_row = from_row
            new_col = from_col
            for col in range(from_col, -1, -1):
                new_row -= 1
                new_col -= 1
                if not self.check_range(new_row, new_col):
                    break
                else:
                    if board[new_row][new_col] is None:
                        possible_squares.append([new_row, new_col])
                    elif board[new_row][new_col].get_color() != turn:
                        possible_squares.append([new_row, new_col])
                        break
                    else:
                        break

            # go up
            new_row = from_row
            new_col = from_col
            for row in range(from_row, 8):
                new_row += 1
                if not self.check_range(new_row, new_col):
                    pass
                else:
                    if board[new_row][new_col] is None:
                        possible_squares.append([new_row, new_col])
                    elif board[new_row][new_col].get_color() != turn:
                        possible_squares.append([new_row, new_col])
                        break
                    else:
                        break

            return possible_squares

        if self._color == 'b':

            # diagonal going up and right
            new_row = from_row
            new_col = from_col
            for col in range(from_col, 8):
                new_row += 1
                new_col += 1
                if not self.check_range(new_row, new_col):
                    break
                else:
                    if board[new_row][new_col] is None:
                        possible_squares.append([new_row, new_col])
                    elif board[new_row][new_col].get_color() != turn:
                        possible_squares.append([new_row, new_col])
                        break
                    else:
                        break

            # diagonal going left and up
            new_row = from_row
            new_col = from_col
            for col in range(from_col, -1, -1):
                new_row += 1
                new_col -= 1
                if not self.check_range(new_row, new_col):
                    break
                else:
                    if board[new_row][new_col] is None:
                        possible_squares.append([new_row, new_col])
                    elif board[new_row][new_col].get_color() != turn:
                        possible_squares.append([new_row, new_col])
                        break
                    else:
                        break
            # go down
            new_row = from_row
            new_col = from_col
            for row in range(from_row, -1, -1):
                new_row -= 1
                if not self.check_range(new_row, new_col):
                    pass
                else:
                    if board[new_row][new_col] is None:
                        possible_squares.append([new_row, new_col])
                    elif board[new_row][new_col].get_color() != turn:
                        possible_squares.append([new_row, new_col])
                        break
                    else:
                        break

            return possible_squares
