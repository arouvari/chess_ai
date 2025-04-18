import time
import random

class ChessEngine:
    def __init__(self):
        self.board = ChessEngine.initialize()
        self.moves = []
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
        self.pins = []
        self.checks = []
        #For calculating the current material difference between black and white
        self.score = self.calculateScore()

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

    #This function initializes the chessboard as 8x8 mailbox with each letter representing a piece,
    #white pieces are in uppercase and black pieces in lower case.
    #Empty squares are represented as a space.
    @staticmethod
    def initialize():
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


    def makeMove(self, move):
        captured_value = 0
        if move.pieceCaptured != " ":
            captured_value = {"p": 1, "n": 3, "b": 3, "r": 5, "q": 9, "k": 0}.get(move.pieceCaptured.lower(), 0)
            self.score += captured_value if self.turn == "white" else -captured_value
        if move.promotionChoice:
            promotion_value = {"q": 9, "r": 5, "n": 3, "b": 3}.get(move.promotionChoice.lower(), 0)
            pawn_value = 1
            if self.turn == "white":
                self.score += (promotion_value-pawn_value)
            else:
                self.score -= (promotion_value-pawn_value)
        self.board[move.startRow][move.startCol] = " "
        self.board[move.endRow][move.endCol] = move.promotionChoice if move.promotionChoice else move.pieceMoved
        self.moves.append(move)
        self.turn = "black" if self.turn == "white" else "white"
        if move.pieceMoved.upper() == "K":
            if move.pieceMoved.isupper():
                self.wKingLocation = (move.endRow, move.endCol)
            else:
                self.bKingLocation = (move.endRow, move.endCol)
        return move.getUCI()

    #This function get's the move from the engine and translates the UCI notation to the move
    def handleMove(self, move_uci):
        if len(move_uci) not in (4, 5):
            raise ValueError(f"Invalid UCI move: {move_uci}")
        start_col = Move.filesToCols[move_uci[0]]
        start_row = Move.ranksToRows[move_uci[1]]
        end_col = Move.filesToCols[move_uci[2]]
        end_row = Move.ranksToRows[move_uci[3]]
        promotion = None
        if len(move_uci) == 5:
            if move_uci[4].upper() not in ['Q', 'R', 'N', 'B']:
                raise ValueError(f"Invalid promotion piece: {move_uci[4]}")
            promotion = move_uci[4].upper() if self.turn == "white" else move_uci[4].lower()
        move = Move((start_row, start_col), (end_row, end_col), self.board, promotionChoice=promotion)
        self.makeMove(move)
        print(f"Received move: {move}")

    def undoMove(self):
        if not self.moves:
            return
        move = self.moves.pop()
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

    @staticmethod
    def setBoard(board_state):
        print(f"Set board to: {board_state}")

    def resetBoard(self):
        self.board = ChessEngine.initialize()
        print("Board reset!")

    def bestMove(self, depth=3):
        _, best_move = self.minimax(depth, self.turn == "white")
        return best_move

    def minimax(self, depth, MaximizingPlayer, alpha=float("-inf"), beta=float("inf")):
        valid_moves = self.validMoves()
        if depth == 0 or not valid_moves:
            return self.evaluateBoard(), None
        if MaximizingPlayer:
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


    #Checking for checkmate, stalemate and removing own moves that put you in check
    def validMoves(self):
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
                moves = []
                self.getKingMoves(kingRow, kingCol, moves)
        else:
            moves = self.possibleMoves()
        return moves

    #Finds all possible pins and checks based on the locations of the pieces.
    def pinsAndChecks(self):
        pins, checks = [], []
        check = False
        enemy, startRow, startCol = (
            ("b", self.wKingLocation[0], self.wKingLocation[1])
            if self.turn == "white"
            else ("w", self.bKingLocation[0], self.bKingLocation[1])
        )

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j, d in enumerate(directions):
            possiblePin = ()
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
                        if not possiblePin:
                            possiblePin = (endRow, endCol, d[0], d[1])
                        break
                    if endPiece != " " and (
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
        return check, pins, checks

    #Function for determining if king is in check
    def isInCheck(self):
        r, c = self.wKingLocation if self.turn == "white" else self.bKingLocation
        return self.underAttack(r, c)

    #Helper function for check detection
    def underAttack(self, r, c):
        self.turn = "black" if self.turn == "white" else "white"
        enemyMoves = self.validMoves()
        self.turn = "black" if self.turn == "white" else "white"
        return any(move.endRow == r and move.endCol == c for move in enemyMoves)

    #Finding all possible moves for white and black.
    def possibleMoves(self):
        moves = []
        for r, row in enumerate(self.board):
            for c, piece in enumerate(row):
                if self.turn == "white" and piece.isupper():
                    self.pieceMoves[piece](r, c, moves)
                elif self.turn == "black" and piece.islower():
                    self.pieceMoves[piece.upper()](r, c, moves)
        return moves

    #Rules for all possible pawn moves, no en passant.
    def getPawnMoves(self, r, c, moves):
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


    #Rules for all possible rook moves.
    def getRookMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c].upper() != "Q":
                    self.pins.remove(self.pins[i])
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
    #No castling possibility as of yet.

    #Rules for all possible knight moves.
    def getKnightMoves(self, r, c, moves):
        piecePinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                self.pins.remove(self.pins[i])
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

    #Rules for all possible bishop moves
    def getBishopMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c].upper() != "Q":
                    self.pins.remove(self.pins[i])
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

    #Rules for all possible queen moves, combines rook and bishop moves in one to get all queen moves.
    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    #Rules for all possible king moves
    def getKingMoves(self, r, c, moves):
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

class Move:
    #Mapping list values to chessboard row names
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, promotionChoice=None):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.promotionChoice = promotionChoice
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    #Converting chessboard row and column numbers to chessnotation.
    def getUCI(self):
        uci = self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
        if self.promotionChoice:
            uci += self.promotionChoice.lower()
        return uci

    #Helper function for translating to UCI.
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

    #For correct chess notation print in AI platform console#
    def __repr__(self):
        return self.getUCI()

#The main function is code mimiced from the example code from stupid-chess-ai.
def main():
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
