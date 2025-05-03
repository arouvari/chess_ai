import time
import random

class ChessEngine:
    """
    A chess engine that manages the game state, evaluates positions, and computes moves using a minimax algorithm with alpha-beta pruning.
    The engine represents the chessboard as an 8x8 grid, with pieces denoted by letters, uppercase for white and lowercase for black.
    It supports move generation, validation, castling, pawn promotion, and basic AI move selection.
    No en passant implementation is in the code.
    """
    def __init__(self):
        """
        This function initializes the starting state of the game by setting the starting position, king locations, castling rights,
        initializing moves, pins and checks lists.
        """
        self.board = ChessEngine.initialize()
        #Tracks all moves made during a game for the undo function.
        self.moves = []
        #Current player turn, set as white for the start.
        self.turn = "white"
        #Using right get moves function depending on piece.
        self.pieceMoves = {
            "P": self.getPawnMoves, "R": self.getRookMoves, "N": self.getKnightMoves,
            "B": self.getBishopMoves, "Q": self.getQueenMoves, "K": self.getKingMoves
        }
        #Starting locations for white and black kings
        self.wKingLocation = (7, 4)
        self.bKingLocation = (0, 4)
        #Initial checkmate and stalemate states
        self.checkmate = False
        self.stalemate = False
        self.check = False
        #List of current pins
        self.pins = []
        #List of current checks
        self.checks = []
        #For calculating the current material difference between black and white
        self.score = self.calculateScore()
        #All castling rights are set True at the start.
        self.whiteCastleKingside = True
        self.whiteCastleQueenside = True
        self.blackCastleKingside = True
        self.blackCastleQueenside = True

        #Preferred board position mappings for different pieces eg. pawn is best on the penultimate row since on next move it can promote,
        # queen is best in the middle since it has more possible moves.
        # Source: https://github.com/amir650/BlackWidow-Chess/blob/master/src/com/chess/engine/classic/Alliance.java
        self.white_pawn_preferred_coordinates = [
            0, 0, 0, 0, 0, 0, 0, 0,
            0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9,
            0.3, 0.3, 0.4, 0.6, 0.6, 0.4, 0.3, 0.3,
            0.1, 0.1, 0.2, 0.4, 0.4, 0.2, 0.1, 0.1,
            0.05, 0.05, 0.1, 0.2, 0.2, 0.1, 0.05, 0.05,
            0, 0, 0,-0.1,-0.1, 0, 0, 0,
            0.05, -0.05,-0.1, 0, 0,-0.1, -0.05, 0.05,
            0, 0, 0, 0, 0, 0, 0, 0
        ]
        self.black_pawn_preferred_coordinates = [
            0, 0, 0, 0, 0, 0, 0, 0,
            0.05, -0.05,-0.1,0,0,-0.1,-0.05,0.05,
            0, 0, 0,-0.1,-0.1, 0, 0, 0,
            0.05, 0.05, 0.1, 0.2, 0.2, 0.1, 0.05, 0.05,
            0.1, 0.1, 0.2, 0.4, 0.4, 0.2, 0.1, 0.1,
            0.3, 0.3, 0.4, 0.6, 0.6, 0.4, 0.3, 0.3,
            0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9,
            0, 0, 0, 0, 0, 0, 0, 0
        ]
        self.white_knight_preferred_coordinates = [
            -0.5,-0.4,-0.3,-0.3,-0.3,-0.3,-0.4,-0.5,
            -0.4,-0.2, 0, 0.05, 0.05, 0,-0.2,-0.4,
            -0.3, 0.05, 0.1, 0.15, 0.15, 0.1, 0.05,-0.3,
            -0.3, 0.05, 0.15, 0.2, 0.2, 0.15, 0.05,-0.3,
            -0.3, 0.05, 0.15, 0.2, 0.2, 0.15, 0.05,-0.3,
            -0.3, 0.05, 0.1, 0.15, 0.15, 0.1, 0.05,-0.3,
            -0.4,-0.2, 0, 0, 0, 0,-0.2,-0.4,
            -0.5,-0.4,-0.3,-0.3,-0.3,-0.3,-0.4,-0.5
        ]
        self.black_knight_preferred_coordinates = [
            -0.5,-0.4,-0.3,-0.3,-0.3,-0.3,-0.4,-0.5,
            -0.4,-0.2, 0, 0, 0, 0,-0.2,-0.4,
            -0.3, 0.05, 0.1, 0.15, 0.15, 0.1, 0.05,-0.3,
            -0.3, 0.05, 0.15, 0.2, 0.2, 0.15, 0.05,-0.3,
            -0.3, 0.05, 0.15, 0.2, 0.2, 0.15, 0.05,-0.3,
            -0.3, 0.05, 0.1, 0.15, 0.15, 0.1, 0.05,-0.3,
            -0.4,-0.2, 0, 0.05, 0.05, 0,-0.2,-0.4,
            -0.5,-0.4,-0.3,-0.3,-0.3,-0.3,-0.4,-0.5
        ]
        self.white_bishop_preferred_coordinates = [
            -0.2,-0.1,-0.1,-0.1,-0.1,-0.1,-0.1,-0.2,
            -0.1, 0, 0, 0, 0, 0, 0,-0.1,
            -0.1, 0, 0.05, 0.1, 0.1, 0.05, 0,-0.1,
            -0.1, 0.05, 0.05, 0.1, 0.1, 0.05, 0.05,-0.1,
            -0.1, 0, 0.1, 0.15, 0.15, 0.1, 0,-0.1,
            -0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1,-0.1,
            -0.1, 0.05, 0, 0, 0, 0, 0.05,-0.1,
            -0.2,-0.1,-0.1,-0.1,-0.1,-0.1,-0.1,-0.2
        ]
        self.black_bishop_preferred_coordinates = [
            -0.2,-0.1,-0.1,-0.1,-0.1,-0.1,-0.1,-0.2,
            -0.1, 0.05, 0, 0, 0, 0, 0.05,-0.1,
            -0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1,-0.1,
            -0.1, 0, 0.1, 0.15, 0.15, 0.1, 0,-0.1,
            -0.1, 0.05, 0.1, 0.15, 0.15, 0.1, 0.05,-0.1,
            -0.1, 0, 0.1, 0.1, 0.1, 0.1, 0,-0.1,
            -0.1, 0, 0, 0, 0, 0, 0,-0.1,
            -0.2,-0.1,-0.1,-0.1,-0.1,-0.1,-0.1,-0.2
        ]
        self.white_rook_preferred_coordinates = [
            0,  0,  0,  0,  0,  0,  0,  0,
            0.05, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.05,
            -0.05, 0, 0, 0, 0, 0, 0, -0.05,
            -0.05, 0, 0, 0, 0, 0, 0, -0.05,
            -0.05, 0, 0, 0, 0, 0, 0, -0.05,
            -0.05, 0, 0, 0, 0, 0, 0, -0.05,
            -0.05, 0, 0, 0, 0, 0, 0, -0.05,
            0, 0, 0, 0.05, 0.05, 0, 0, 0
        ]
        self.black_rook_preferred_coordinates = [
            0, 0, 0, 0.05, 0.05, 0, 0, 0,
            -0.05, 0, 0, 0, 0, 0, 0, -0.05,
            -0.05, 0, 0, 0, 0, 0, 0, -0.05,
            -0.05, 0, 0, 0, 0, 0, 0, -0.05,
            -0.05, 0, 0, 0, 0, 0, 0, -0.05,
            -0.05, 0, 0, 0, 0, 0, 0, -0.05,
            0.05, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.05,
            0, 0, 0, 0, 0, 0, 0, 0
        ]
        self.white_queen_preferred_coordinates = [
            -0.2,-0.1,-0.1, -0.05, -0.05,-0.1,-0.1,-0.2,
            -0.1, 0, 0, 0, 0, 0, 0,-0.1,
            -0.1, 0, 0.05, 0.05, 0.05, 0.05, 0,-0.1,
            -0.05, 0, 0.05, 0.1, 0.1, 0.05, 0, -0.05,
            -0.05, 0, 0.05, 0.1, 0.1, 0.05, 0, -0.05,
            -0.1, 0, 0.05, 0.05, 0.05, 0.05, 0,-0.1,
            -0.1, 0, 0, 0, 0, 0, 0,-0.1,
            -0.2,-0.1,-0.1, -0.05, -0.05,-0.1,-0.1,-0.2
        ]
        self.black_queen_preferred_coordinates = [
            -0.2,-0.1,-0.1, -0.05, -0.05,-0.1,-0.1,-0.2,
            -0.1, 0, 0.05, 0, 0, 0, 0,-0.1,
            -0.1, 0.05, 0.05, 0.05, 0.05, 0.05, 0,-0.1,
            -0.05, 0, 0.05, 0.1, 0.1, 0.05, 0, -0.05,
            -0.05, 0, 0.05, 0.1, 0.1, 0.05, 0, -0.05,
            -0.1, 0, 0.05, 0.05, 0.05, 0.05, 0,-0.1,
            -0.1, 0, 0, 0, 0, 0, 0,-0.1,
            -0.2,-0.1,-0.1, -0.05, -0.05,-0.1,-0.1,-0.2
        ]
        self.white_king_preferred_coordinates = [
            -0.5,-0.3,-0.3,-0.3,-0.3,-0.3,-0.3,-0.5,
            -0.3,-0.3, 0, 0, 0, 0,-0.3,-0.3,
            -0.3,-0.1, 0.2, 0.3, 0.3, 0.2,-0.1,-0.3,
            -0.3,-0.1, 0.3, 0.4, 0.4, 0.3,-0.1,-0.3,
            -0.3,-0.1, 0.3, 0.4, 0.4, 0.3,-0.1,-0.3,
            -0.3,-0.1, 0.2, 0.3, 0.3, 0.2,-0.1,-0.3,
            -0.3,-0.2,-0.1, 0, 0,-0.1,-0.2,-0.3,
            -0.5,-0.4,-0.3,-0.2,-0.2,-0.3,-0.4,-0.5
        ]
        self.black_king_preferred_coordinates = [
            -0.5,-0.4,-0.3,-0.2,-0.2,-0.3,-0.4,-0.5,
            -0.3,-0.2,-0.1, 0, 0,-0.1,-0.2,-0.3,
            -0.3,-0.1, 0.2, 0.3, 0.3, 0.2,-0.1,-0.3,
            -0.3,-0.1, 0.3, 0.4, 0.4, 0.3,-0.1,-0.3,
            -0.3,-0.1, 0.3, 0.4, 0.4, 0.3,-0.1,-0.3,
            -0.3,-0.1, 0.2, 0.3, 0.3, 0.2,-0.1,-0.3,
            -0.3,-0.3, 0, 0, 0, 0,-0.3,-0.3,
            -0.5,-0.3,-0.3,-0.3,-0.3,-0.3,-0.3,-0.5
        ]


    @staticmethod
    def initialize():
        """
        This function initializes the chessboard as 8x8 mailbox with each letter representing a piece,
        white pieces are in uppercase and black pieces in lower case.
        Empty squares are represented as a space.
        """
        return [
            ["r", "n", "b", "q", "k", "b", "n", "r"],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            ["R", "N", "B", "Q", "K", "B", "N", "R"]
        ]
    def calculateScore(self):
        """
        Calculates the score by material. Assigning a value for each piece and adding them to get current
        evaluation of material.

        Returns:
            int: positive values represent an advantage for white in material and negative values an advantage for black.
        """
        piece_values = {
            "P":1, "p":1,
            "N":3, "n":3,
            "B":3, "b":3,
            "R":5, "r":5,
            "Q":9, "q":9,
            "K":0, "k":0
        }
        score = 0
        for row in self.board:
            for piece in row:
                if piece == " ":
                    continue
                if piece.isupper():
                    score += piece_values.get(piece, 0)
                else:
                    score -= piece_values.get(piece, 0)

        return score

    def makeMove(self, move): # pylint: disable=R0915
        """
        Executes a move, updates the game state including castling rights and material score based on the
        move received.

        Args:
            move (Move): The move to execute, containing start/end positions, piece moved, and optional promotion.

        Returns:
            str: The move in UCI notation (e.g., 'e2e4').
        """
        captured_value = 0
        move.whiteCastleKingside = self.whiteCastleKingside
        move.whiteCastleQueenside = self.whiteCastleQueenside
        move.blackCastleKingside = self.blackCastleKingside
        move.blackCastleQueenside = self.blackCastleQueenside
        if move.pieceCaptured != " ":
            captured_value = {"p": 1, "n": 3, "b": 3, "r": 5, "q": 9, "k": 0}.get(move.pieceCaptured.lower(), 0)
            self.score += captured_value if self.turn == "white" else -captured_value
            if move.pieceCaptured.lower() == 'r':
                if move.pieceCaptured == 'r':
                    if (move.endRow, move.endCol) == (0, 0):
                        self.blackCastleQueenside = False
                    elif (move.endRow, move.endCol) == (0, 7):
                        self.blackCastleKingside = False
                else:
                    if (move.endRow, move.endCol) == (7, 0):
                        self.whiteCastleQueenside = False
                    elif (move.endRow, move.endCol) == (7, 7):
                        self.whiteCastleKingside = False

        if move.promotionChoice:
            promotion_value = {"q": 9, "r": 5, "n": 3, "b": 3}.get(move.promotionChoice.lower(), 0)
            pawn_value = 1
            if self.turn == "white":
                self.score += (promotion_value - pawn_value)
            else:
                self.score -= (promotion_value - pawn_value)

        self.board[move.startRow][move.startCol] = " "
        self.board[move.endRow][move.endCol] = move.promotionChoice if move.promotionChoice else move.pieceMoved
        self.moves.append(move)
        self.turn = "black" if self.turn == "white" else "white"

        if move.isCastle:
            self.board[move.rookStart[0]][move.rookStart[1]] = " "
            self.board[move.rookEnd[0]][move.rookEnd[1]] = move.rookMoved
            if move.pieceMoved == "K":
                self.whiteCastleKingside = False
                self.whiteCastleQueenside = False
            else:
                self.blackCastleKingside = False
                self.blackCastleQueenside = False

        if move.pieceMoved.upper() == "K":
            if move.pieceMoved.isupper():
                self.wKingLocation = (move.endRow, move.endCol)
            else:
                self.bKingLocation = (move.endRow, move.endCol)

        if move.pieceMoved.upper() == "K":
            if move.pieceMoved == "K":
                self.whiteCastleKingside = False
                self.whiteCastleQueenside = False
            else:
                self.blackCastleKingside = False
                self.blackCastleQueenside = False
        elif move.pieceMoved.upper() == "R":
            if move.pieceMoved == "R":
                if (move.startRow, move.startCol) == (7, 0):
                    self.whiteCastleQueenside = False
                elif (move.startRow, move.startCol) == (7, 7):
                    self.whiteCastleKingside = False
            else:
                if (move.startRow, move.startCol) == (0, 0):
                    self.blackCastleQueenside = False
                elif (move.startRow, move.startCol) == (0, 7):
                    self.blackCastleKingside = False
        return move.getUCI()


    def handleMove(self, move_uci):
        """
        Handles a move it gets in UCI notation and makes changes to the board.

        Args:
            move_uci (str): The move in UCI notation.

        Raises:
            ValueError: If the UCI received is invalid.
        """
        if len(move_uci) not in (4, 5):
            raise ValueError(f"Invalid UCI move: {move_uci}")
        start_col = Move.filesToCols[move_uci[0]]
        start_row = Move.ranksToRows[move_uci[1]]
        end_col = Move.filesToCols[move_uci[2]]
        end_row = Move.ranksToRows[move_uci[3]]
        promotion = None
        if len(move_uci) == 5:
            if move_uci[4].upper() not in ["Q", "R", "N", "B"]:
                raise ValueError(f"Invalid promotion piece: {move_uci[4]}")
            promotion = move_uci[4].upper() if self.turn == "white" else move_uci[4].lower()
        move = Move((start_row, start_col), (end_row, end_col), self.board, promotionChoice=promotion)
        self.makeMove(move)
        print(f"Received move: {move}")

    def undoMove(self):
        """
        Undos the last made move, reverses the made changes in the board and game state.
        """
        if not self.moves:
            return
        move = self.moves.pop()
        self.whiteCastleKingside = move.whiteCastleKingside
        self.whiteCastleQueenside = move.whiteCastleQueenside
        self.blackCastleKingside = move.blackCastleKingside
        self.blackCastleQueenside = move.blackCastleQueenside

        if move.pieceCaptured != " ":
            captured_value = {"p": 1, "n": 3, "b": 3, "r": 5, "q": 9, "k": 0}.get(move.pieceCaptured.lower(), 0)
            if move.pieceMoved.isupper():
                self.score -= captured_value
            else:
                self.score += captured_value
        if move.promotionChoice:
            promotion_value = {"q": 9, "r": 5, "n": 3, "b": 3}.get(move.promotionChoice.lower(), 0)
            pawn_value = 1
            if move.pieceMoved.isupper():
                self.score -= (promotion_value - pawn_value)
            else:
                self.score += (promotion_value - pawn_value)

        self.board[move.startRow][move.startCol] = move.pieceMoved
        self.board[move.endRow][move.endCol] = move.pieceCaptured
        self.turn = "white" if self.turn == "black" else "black"
        if move.pieceMoved.upper() == "K":
            if move.pieceMoved.isupper():
                self.wKingLocation = (move.startRow, move.startCol)
            else:
                self.bKingLocation = (move.startRow, move.startCol)

        if move.isCastle:
            self.board[move.rookStart[0]][move.rookStart[1]] = move.rookMoved
            self.board[move.rookEnd[0]][move.rookEnd[1]] = move.rookCaptured



    def setBoard(self, fen):
        """
        Sets the board position based on the provided FEN string.

        Args:
            fen_str (str): The FEN string representing the board position.
        """
        fen_fields = fen.split()
        piece_placement = fen_fields[0]
        active_color = fen_fields[1]
        castling = fen_fields[2]


        ranks = piece_placement.split('/')

        self.board = []
        for rank in range(8):
            row = []
            rank_str = ranks[rank]
            col = 0
            for char in rank_str:
                if char.isalpha():
                    row.append(char)
                    if char == 'K':
                        self.wKingLocation = (rank, col)
                    elif char == 'k':
                        self.bKingLocation = (rank, col)
                    col += 1
                elif char.isdigit():
                    num = int(char)
                    row.extend([' '] * num)
                    col += num
                else:
                    raise ValueError(f"Invalid character in FEN: {char}")
            if col != 8:
                raise ValueError(f"Invalid FEN: rank {rank} does not have 8 squares")
            self.board.append(row)

        if active_color == 'w':
            self.turn = 'white'
        elif active_color == 'b':
            self.turn = 'black'
        else:
            raise ValueError(f"Invalid active color: {active_color}")

        if castling == '-':
            self.whiteCastleKingside = False
            self.whiteCastleQueenside = False
            self.blackCastleKingside = False
            self.blackCastleQueenside = False
        else:
            self.whiteCastleKingside = 'K' in castling
            self.whiteCastleQueenside = 'Q' in castling
            self.blackCastleKingside = 'k' in castling
            self.blackCastleQueenside = 'q' in castling

        self.score = self.calculateScore()

        self.moves = []

        print(f"Set board to FEN: {fen}")

    def resetBoard(self):
        """
        Resets board to the starting position.
        """
        self.board = ChessEngine.initialize()
        print("Board reset!")

    def bestMove(self, depth=3):
        """
        Calculates best move for the AI using minimax algorithm in depth of 3.

        Args:
            depth (int): The search depth for the minimax algorithm.

        Returns:
            Move: The best move or None if no valid moves exist.
        """
        _, best_move = self.minimax(depth, self.turn == "white")
        return best_move

    def minimax(self, depth, maximizingPlayer, alpha=float("-inf"), beta=float("inf")):
        """
        Implements the minimax algorithm with alpha-beta pruning to evaluate moves.

        Args:
            depth (int): The depth the algorithm searches.
            maximizingPlayer (bool): True if maximizing (White), False if minimizing (Black).
            alpha (float): Best score for the maximizer along the current path.
            beta (float): Best score for the minimizer along the current path.

        Returns:
            tuple: (best_score, best_move).
        """
        valid_moves = self.validMoves()
        if depth == 0 or not valid_moves:
            return self.evaluateBoard(), None
        if maximizingPlayer:
            max_value = float("-inf")
            best_move = None
            for move in valid_moves:
                self.makeMove(move)
                value, _ = self.minimax(depth-1, False, alpha, beta)
                self.undoMove()
                if value > max_value:
                    max_value = value
                    best_move = move
                alpha = max(alpha, max_value)
                if beta <= alpha:
                    break
            return max_value, best_move

        min_value = float("inf")
        best_move = None
        for move in valid_moves:
            self.makeMove(move)
            value, _ = self.minimax(depth-1, True, alpha, beta)
            self.undoMove()
            if value < min_value:
                min_value = value
                best_move = move
            beta = min(beta, min_value)
            if beta <= alpha:
                break
        return min_value, best_move

    def evaluateBoard(self):
        """
        Evaluates the board position based on material difference and position of the pieces.

        Returns:
            float: Positive scores are advantage for white, negative are advantage for Black.
        """
        valid_moves = self.validMoves()
        if not valid_moves:
            if self.isInCheck():
                #When the player in turn is in checkmate
                return -9999 if self.turn == "white" else 9999
            #When there is a stalemate
            return 0
        material_score = self.score

        positional_score = 0
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece == " ":
                    continue
                index = r * 8 + c
                if piece == "P":
                    positional_score += self.white_pawn_preferred_coordinates[index]
                elif piece == "p":
                    positional_score -= self.black_pawn_preferred_coordinates[index]
                elif piece == "N":
                    positional_score += self.white_knight_preferred_coordinates[index]
                elif piece == "n":
                    positional_score -= self.black_knight_preferred_coordinates[index]
                elif piece == "B":
                    positional_score += self.white_bishop_preferred_coordinates[index]
                elif piece == "b":
                    positional_score -= self.black_bishop_preferred_coordinates[index]
                elif piece == "R":
                    positional_score += self.white_rook_preferred_coordinates[index]
                elif piece == "r":
                    positional_score -= self.black_rook_preferred_coordinates[index]
                elif piece == "Q":
                    positional_score += self.white_queen_preferred_coordinates[index]
                elif piece == "q":
                    positional_score -= self.black_queen_preferred_coordinates[index]
                elif piece == "K":
                    positional_score += self.white_king_preferred_coordinates[index]
                elif piece == "k":
                    positional_score -= self.black_king_preferred_coordinates[index]

        total_score = material_score+positional_score

        return total_score if self.turn == "white" else -total_score


    def validMoves(self):
        """
        Generates all legal moves for the current player, accounting for checks and pins.

        Returns:
            list: A list of valid moves that are allowed by the rules.
        """
        moves = []
        self.check, self.pins, self.checks = self.pinsAndChecks()
        kingRow, kingCol = self.wKingLocation if self.turn == "white" else self.bKingLocation

        if self.check:
            if len(self.checks) == 1:
                moves = self.possibleMoves()
                check = self.checks[0]
                checkRow, checkCol = check[0], check[1]
                checkingPiece = self.board[checkRow][checkCol]
                validSquares = []
                if checkingPiece.upper() == "N":
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8):
                        validSquare = (kingRow + check[2] * i, kingCol + check[3] * i)
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break
                for i in range(len(moves) - 1, -1, -1):
                    if moves[i].pieceMoved.upper() != "K":
                        if (moves[i].endRow, moves[i].endCol) not in validSquares:
                            moves.remove(moves[i])
            else:
                moves = [move for move in self.possibleMoves() if move.pieceMoved.upper() == "K"]
        else:
            moves = self.possibleMoves()
        return moves


    def pinsAndChecks(self):
        """
        Identifies all pinned pieces and checks made against the current player's king.

        Returns:
            tuple: (is_in_check, pins, checks), where:
                is_in_check (bool): Is True if the king is in check.
                pins (list): List of all pinned pieces (row, col, direction).
                checks (list): List of all checking pieces (row, col, direction).
        """
        pins, checks = [], []
        check = False
        enemy, startRow, startCol = (
            ("b", self.wKingLocation[0], self.wKingLocation[1])
            if self.turn == "white"
            else ("w", self.bKingLocation[0], self.bKingLocation[1])
        )

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j, d in enumerate(directions):
            possiblePin = None
            for i in range(1, 8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    isAlly = (
                        endPiece.isupper() and self.turn == "white" and endPiece != "K" or
                        endPiece.islower() and self.turn == "black" and endPiece != "k"
                    )
                    if endPiece != " " and isAlly:
                        pieceType = endPiece.upper()
                        if pieceType == "N":
                            break
                        if not possiblePin:
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else:
                            break
                    elif endPiece != " " and (
                        endPiece.islower() and self.turn == "white" or
                        endPiece.isupper() and self.turn == "black"
                    ):
                        pieceType = endPiece.upper()
                        if (
                            (0 <= j <= 3 and pieceType == "R") or
                            (4 <= j <= 7 and pieceType == "B") or
                            (i == 1 and pieceType == "P" and (
                                enemy == "w" and 6 <= j <= 7 or
                                enemy == "b" and 4 <= j <= 5
                            )) or
                            pieceType == "Q" or
                            (i == 1 and pieceType == "K")
                        ):
                            if not possiblePin:
                                check = True
                                checks.append((endRow, endCol, d[0], d[1]))
                            else:
                                pins.append(possiblePin)
                            break
                        break
                else:
                    break

        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece != " " and (
                    endPiece.islower() and self.turn == "white" or
                    endPiece.isupper() and self.turn == "black"
                ):
                    if endPiece.upper() == "N":
                        check = True
                        checks.append((endRow, endCol, m[0], m[1]))
                        for i in range(len(self.pins) - 1, -1, -1):
                            if self.pins[i][0] == endRow and self.pins[i][1] == endCol:
                                self.pins.pop(i)
                                break
        return check, pins, checks


    def isInCheck(self):
        """
        Determines if the current player's king is in check.

        Returns:
            bool: Is True if the king is under attack.
        """
        r, c = self.wKingLocation if self.turn == "white" else self.bKingLocation
        return self.underAttack(r, c)


    def underAttack(self, r, c):
        """
        Determines if a square (r, c) is under attack by any of the opponent's pieces.
        """
        enemy_color = "black" if self.turn == "white" else "white"

        pawn_dir = -1 if enemy_color == "white" else 1
        attack_squares = [(r + pawn_dir, c - 1), (r + pawn_dir, c + 1)]
        for ar, ac in attack_squares:
            if 0 <= ar < 8 and 0 <= ac < 8:
                piece = self.board[ar][ac]
                if piece.lower() == 'p' and (piece.islower() == (enemy_color == "black")):
                    return True

        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for dr, dc in knight_moves:
            ar, ac = r + dr, c + dc
            if 0 <= ar < 8 and 0 <= ac < 8:
                piece = self.board[ar][ac]
                if piece.lower() == 'n' and (piece.islower() == (enemy_color == "black")):
                    return True

        king_moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dr, dc in king_moves:
            ar, ac = r + dr, c + dc
            if 0 <= ar < 8 and 0 <= ac < 8:
                piece = self.board[ar][ac]
                if piece.lower() == 'k' and (piece.islower() == (enemy_color == "black")):
                    return True

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                    (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for d in directions:
            dr, dc = d
            for step in range(1, 8):
                ar = r + dr * step
                ac = c + dc * step
                if not (0 <= ar < 8 and 0 <= ac < 8):
                    break
                piece = self.board[ar][ac]
                if piece == ' ':
                    continue
                if (piece.islower() == (enemy_color == "black")):
                    piece_type = piece.lower()
                    if step == 1 and piece_type == 'k':
                        return True
                    if piece_type == 'q':
                        return True
                    if (d in [(-1, 0), (1, 0), (0, -1), (0, 1)] and piece_type == 'r'):
                        return True
                    if (d in [(-1, -1), (-1, 1), (1, -1), (1, 1)] and piece_type == 'b'):
                        return True
                break

        return False

    def possibleMoves(self):
        """
        Generates all possible moves for the current player, ignoring checks.

        Returns:
            list: A list of possible moves.
        """
        moves = []
        for r, row in enumerate(self.board):
            for c, piece in enumerate(row):
                if self.turn == "white" and piece.isupper():
                    self.pieceMoves[piece](r, c, moves)
                elif self.turn == "black" and piece.islower():
                    self.pieceMoves[piece.upper()](r, c, moves)
        return moves


    def getPawnMoves(self, r, c, moves):
        """
        Generates all possible pawn moves, including promotions but not en passant.

        Args:
            r (int): Row of the pawn.
            c (int): Column of the pawn.
            moves (list): List to append valid moves for a pawn.
        """
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        promotion_pieces = ["Q", "R", "N", "B"] if self.turn == "white" else ["q", "r", "n", "b"]

        # White pawn moves
        if self.turn == "white":
            if self.board[r - 1][c] == " " and (not piecePinned or pinDirection == (-1, 0)):
                if r-1==0:
                    for piece in promotion_pieces:
                        moves.append(Move((r, c), (r-1, c), self.board, promotionChoice=piece))
                else:
                    moves.append(Move((r, c), (r - 1, c), self.board))
                    if r == 6 and self.board[r - 2][c] == " ":
                        moves.append(Move((r, c), (r - 2, c), self.board))

            if c - 1 >= 0 and self.board[r - 1][c - 1].islower() and (
                not piecePinned or pinDirection == (-1, -1)
            ):
                if r - 1 == 0:
                    for piece in promotion_pieces:
                        moves.append(Move((r, c), (r-1, c-1), self.board, promotionChoice=piece))
                else:
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if c + 1 <= 7 and self.board[r - 1][c + 1].islower() and (
                not piecePinned or pinDirection == (-1, 1)
            ):
                if r - 1 == 0:
                    for piece in promotion_pieces:
                        moves.append(Move((r, c), (r - 1, c + 1), self.board, promotionChoice=piece))
                else:
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))

        # Black pawn moves
        else:
            if self.board[r + 1][c] == " " and (not piecePinned or pinDirection == (1, 0)):
                if r + 1 == 7:
                    for piece in promotion_pieces:
                        moves.append(Move((r, c), (r + 1, c), self.board, promotionChoice=piece))
                else:
                    moves.append(Move((r, c), (r + 1, c), self.board))
                    if r == 1 and self.board[r + 2][c] == " ":
                        moves.append(Move((r, c), (r + 2, c), self.board))

            if c - 1 >= 0 and self.board[r + 1][c - 1].isupper() and (
                not piecePinned or pinDirection == (1, -1)
            ):
                if r + 1 == 7:
                    for piece in promotion_pieces:
                        moves.append(Move((r, c), (r + 1, c - 1), self.board, promotionChoice=piece))
                else:
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))

            if c + 1 <= 7 and self.board[r + 1][c + 1].isupper() and (
                not piecePinned or pinDirection == (1, 1)
            ):
                if r + 1 == 7:
                    for piece in promotion_pieces:
                        moves.append(Move((r, c), (r + 1, c + 1), self.board, promotionChoice=piece))
                else:
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))


    def getRookMoves(self, r, c, moves):
        """
        Generates all possible rook moves.

        Args:
            r (int): Row of the rook.
            c (int): Column of the rook.
            moves (list): List to append valid rook moves.
        """
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                break

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == " ":
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif (self.turn == "white" and endPiece.islower()) or (
                            self.turn == "black" and endPiece.isupper()
                        ):
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else:
                            break
                else:
                    break

    def getKnightMoves(self, r, c, moves):
        """
        Generates all possible knight moves.

        Args:
            r (int): Row of the knight.
            c (int): Column of the knight.
            moves (list): List to append valid knight moves.
        """
        piecePinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                break

        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if not piecePinned and (
                    endPiece == " " or
                    (self.turn == "white" and endPiece.islower()) or
                    (self.turn == "black" and endPiece.isupper())
                ):
                    moves.append(Move((r, c), (endRow, endCol), self.board))


    def getBishopMoves(self, r, c, moves):
        """
        Generates all possible bishop moves.

        Args:
            r (int): Row of the bishop.
            c (int): Column of the bishop.
            moves (list): List to append valid bishop moves.
        """
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                break
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == " ":
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif (self.turn == "white" and endPiece.islower()) or (
                            self.turn == "black" and endPiece.isupper()
                        ):
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else:
                            break
                else:
                    break


    def getQueenMoves(self, r, c, moves):
        """
        Generates all possible queen moves by combining rook and bishop moves.

        Args:
            r (int): Row of the queen.
            c (int): Column of the queen.
            moves (list): List to append valid queen moves.
        """
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)


    def getKingMoves(self, r, c, moves): # pylint: disable=R0915
        """
        Generates all possible king moves, including castling.

        Args:
            r (int): Row of the king.
            c (int): Column of the king.
            moves (list): List to append valid king moves.
        """
        rowMoves = (-1, -1, -1, 0, 0, 1, 1, 1)
        colMoves = (-1, 0, 1, -1, 1, -1, 0, 1)
        for i in range(8):
            endRow = r + rowMoves[i]
            endCol = c + colMoves[i]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece == " " or (
                    self.turn == "white" and endPiece.islower() or
                    self.turn == "black" and endPiece.isupper()
                ):
                    originalKingLoc = (
                        self.wKingLocation if self.turn == "white" else self.bKingLocation
                    )
                    if self.turn == "white":
                        self.wKingLocation = (endRow, endCol)
                    else:
                        self.bKingLocation = (endRow, endCol)
                    inCheck = self.pinsAndChecks()[0]
                    if not inCheck:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    if self.turn == "white":
                        self.wKingLocation = originalKingLoc
                    else:
                        self.bKingLocation = originalKingLoc
        if self.turn == "white" and not self.check:
            if self.whiteCastleKingside and self.board[7][7] == "R":
                if self.board[7][5] == " " and self.board[7][6] == " ":
                    if not self.underAttack(7, 4) and not self.underAttack(7, 5) and not self.underAttack(7, 6):
                        move = Move((7, 4), (7, 6), self.board)
                        move.isCastle = True
                        move.rookStart = (7, 7)
                        move.rookEnd = (7, 5)
                        move.rookMoved = "R"
                        move.rookCaptured = " "
                        moves.append(move)
            if self.whiteCastleQueenside and self.board[7][0] == "R":
                if self.board[7][1] == " " and self.board[7][2] == " " and self.board[7][3] == " ":
                    if not self.underAttack(7, 4) and not self.underAttack(7, 3) and not self.underAttack(7, 2):
                        move = Move((7, 4), (7, 2), self.board)
                        move.isCastle = True
                        move.rookStart = (7, 0)
                        move.rookEnd = (7, 3)
                        move.rookMoved = "R"
                        move.rookCaptured = " "
                        moves.append(move)

        elif self.turn == "black" and not self.check:
            if self.blackCastleKingside and self.board[0][7] == "r":
                if self.board[0][5] == " " and self.board[0][6] == " ":
                    if not self.underAttack(0, 4) and not self.underAttack(0, 5) and not self.underAttack(0, 6):
                        move = Move((0, 4), (0, 6), self.board)
                        move.isCastle = True
                        move.rookStart = (0, 7)
                        move.rookEnd = (0, 5)
                        move.rookMoved = "r"
                        move.rookCaptured = " "
                        moves.append(move)
            if self.blackCastleQueenside and self.board[0][0] == "r":
                if self.board[0][1] == " " and self.board[0][2] == " " and self.board[0][3] == " ":
                    if not self.underAttack(0, 4) and not self.underAttack(0, 3) and not self.underAttack(0, 2):
                        move = Move((0, 4), (0, 2), self.board)
                        move.isCastle = True
                        move.rookStart = (0, 0)
                        move.rookEnd = (0, 3)
                        move.rookMoved = "r"
                        move.rookCaptured = " "
                        moves.append(move)


class Move:
    """Represents a chess move with start and end positions, capturing, and special move flags."""
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, promotionChoice=None):
        """
        Initializes a move with start and end squares, and optional promotion.

        Args:
            startSq (tuple): (row, col) of the starting square.
            endSq (tuple): (row, col) of the ending square.
            board (list): The current board state.
            promotionChoice (str, optional): The piece to promote to.
        """
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.promotionChoice = promotionChoice
        self.isCastle = False
        self.rookStart = None
        self.rookEnd = None
        self.rookMoved = None
        self.rookCaptured = None
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

        if self.pieceMoved.upper() == "K" and abs(self.startCol - self.endCol) == 2:
            self.isCastle = True
            if self.endCol > self.startCol:
                self.rookStart = (self.startRow, 7)
                self.rookEnd = (self.startRow, self.endCol - 1)
            else:
                self.rookStart = (self.startRow, 0)
                self.rookEnd = (self.startRow, self.endCol + 1)
            self.rookMoved = board[self.rookStart[0]][self.rookStart[1]]
            self.rookCaptured = board[self.rookEnd[0]][self.rookEnd[1]]

    def __eq__(self, other):
        """
        Checks if two moves are equal based on their moveID.

        Args:
            other (Move): The move to compare with.

        Returns:
            bool: True if the moves are equal.
        """
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getUCI(self):
        """
        Converts the move to UCI notation.

        Returns:
            str: The move in UCI format.
        """
        uci = self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
        if self.promotionChoice:
            uci += self.promotionChoice.lower()
        return uci

    def getRankFile(self, r, c):
        """Helper function that translates row and column to UCI notation.

        Args:
            r (int): Row index.
            c (int): Column index.

        Returns:
            str: UCI notation for the square.
        """
        return self.colsToFiles[c] + self.rowsToRanks[r]

    def __repr__(self):
        """Returns the move in UCI notation for console output.

        Returns:
            str: The move in UCI format.
        """
        return self.getUCI()


def main():
    """
    The main function is used for interaction between the AI platform.
    Code is copied from the example code from stupid-chess-ai: https://github.com/game-ai-platform-team/stupid-chess-ai/tree/main.
    """
    ai = ChessEngine()

    while True:
        command = input()
        time.sleep(random.randrange(1, 10) / 100)
        if command.startswith("BOARD:"):
            ai.setBoard(command.removeprefix("BOARD:"))
        elif command.startswith("PLAY:"):
            best_move = ai.bestMove(depth=3)
            if best_move is not None:
                ai.makeMove(best_move)
                print(f"MOVE:{best_move.getUCI()}")
            else:
                print("No valid moves!")
        elif command.startswith("MOVE:"):
            move = command.removeprefix("MOVE:")
            ai.handleMove(move)
        elif command.startswith("RESET:"):
            ai.resetBoard()
        else:
            print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
