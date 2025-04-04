import time
import random

class ChessEngine():
    def __init__(self):
        self.board = self.initialize()
        self.moves = []
        self.turn = "white"
        #Function for getting moves for different pieces
        self.pieceMoves = {"p": self.getPawnMoves, "R": self.getRookMoves, "N": self.getKnightMoves,
                         "B": self.getBishopMoves, "Q": self.getQueenMoves, "K":self.getKingMoves}

        #Starting locations for white and black kings
        self.wKingLocation = (7, 4)
        self.bKingLocation = (0, 4)
        #Initial checkmate and stalemate states
        self.checkmate = False
        self.stalemate = False
        self.check = False
        self.pins = []
        self.checks = []


    #This function initializes the chessboard as 8x8 mailbox with each letter representing a piece,
    #white pieces are in uppercase and black pieces in lower case.
    #Empty squares are represented as a space.
    def initialize(self):
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

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = " "
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moves.append(move)
        self.turn = "black" if self.turn == "white" else "white"
        if move.pieceMoved == "K":
            self.wKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "k":
            self.bKingLocation = (move.endRow, move.endCol)
        return move.getChessNotation()

    def handleMove(self, move):
        print(f"Received move: {move}")

    def setBoard(self, board_state):
        print(f"Set board to: {board_state}")

    def resetBoard(self):
        self.board = self.initialize()
        print("Board reset!")

    #Checking for checkmate, stalemate and removing own moves that put you in check
    def validMoves(self):
        moves = []
        self.check, self.pins, self.checks = self.pinsAndChecks()
        if self.turn == "white":
            kingRow = self.wKingLocation[0]
            kingCol = self.wKingLocation[1]
        else:
            kingRow = self.bKingLocation[0]
            kingCol = self.bKingLocation[1]
        if self.check:
            if len(self.checks) == 1:
                moves = self.possibleMoves()
                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                checkingPiece = self.board[checkRow][checkCol]
                validSquares = []
                if checkingPiece[1] == "N":
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8):
                        validSquare = (kingRow+check[2]*i, kingCol+check[3]*i)
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break
                for i in range(len(moves)-1, -1, -1):
                    if moves[i].pieceMoved[1] != "K":
                        if not (moves[i].endRow, moves[i].endCol) in validSquares:
                            moves.remove(moves[i])
            else:
                self.getKingMoves(kingRow, kingCol, moves)
        else:
            moves = self.possibleMoves()

        return moves

    def pinsAndChecks(self):
        pins = []
        checks = []
        check = False
        if self.turn == "white":
            enemy = "b"
            ally = "w"
            startRow = self.wKingLocation[0]
            startCol = self.wKingLocation[1]

        else:
            enemy = "w"
            ally = "b"
            startRow = self.bKingLocation[0]
            startCol = self.bKingLocation[1]

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = ()
            for i in range(1, 8):
                endRow = startRow+d[0]*i
                endCol = startCol+d[1]*i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == ally and endPiece[1] != "K":
                        if possiblePin == ():
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else:
                            break
                    elif endPiece[0] == enemy:
                        type = endPiece[1]
                        if (0 <= j <= 3 and type == "R") or \
                            (4 <= j <= 7 and type == "B") or \
                            (i == 1 and type == "p" and ((enemy == "w" and 6 <= j <= 7) or (enemy == "b" and 4 <= j <= 5))) or \
                            (type == "Q") or (i==1 and type == "K"):

                            if possiblePin == ():
                                check = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else:
                                pins.append(possiblePin)
                                break
                        else:
                            break
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knightMoves:
            endRow = startRow+m[0]
            endCol = startCol+m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemy and endPiece[1] == "N":
                    check = True
                    checks.append((endRow, endCol, m[0], m[1]))

        return check, pins, checks


    #Function for determining if king is in check
    def isInCheck(self):
        if self.turn == "white":
            return self.underAttack(self.wKingLocation[0], self.wKingLocation[1])
        else:
            return self.underAttack(self.bKingLocation[0], self.bKingLocation[1])

    #Help function for check function
    def underAttack(self, r, c):
        self.turn = "black"
        enemyMoves = self.possibleMoves()
        self.turn = "white"
        for move in enemyMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False

    #Finding all possible moves for white and black
    def possibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == "w" and self.turn == "white") or (turn == "b" and self.turn == "black"):
                    piece = self.board[r][c][1]
                    self.pieceMoves[piece](r, c, moves)
        return moves

    #Rules for all possible pawn moves
    def getPawnMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.turn == "white":
            if self.board[r-1][c] == " ":
                if not piecePinned or pinDirection == (-1, 0):
                    moves.append(Move((r, c), (r-1, c), self.board))
                    if r == 6 and self.board[r-2][c] == " ":
                        moves.append(Move((r, c), (r-2, c), self.board))
            if c-1 >= 0:
                if self.board[r-1][c-1][0] == "b":
                    if not piecePinned or pinDirection == (-1, -1):
                        moves.append(Move((r, c), (r-1, c-1), self.board))
            if c+1 <= 7:
                if self.board[r-1][c+1][0] == "b":
                    if not piecePinned or pinDirection == (-1, 1):
                        moves.append(Move((r, c), (r-1, c+1), self.board))
        else:
            if self.board[r+1][c] == " ":
                if not piecePinned or pinDirection == (1, 0):
                    moves.append(Move((r, c), (r+1, c), self.board))
                    if r == 1 and self.board[r+2][c] == " ":
                        moves.append(Move((r,c), (r+2, c), self.board))

            if c-1 >= 0:
                if self.board[r+1][c-1][0] == "w":
                    if not piecePinned or pinDirection == (1, -1):
                        moves.append(Move((r, c), (r+1, c-1), self.board))
            if c+1 <= 7:
                if self.board[r+1][c+1][0] == "w":
                    if not piecePinned or pinDirection == (1, 1):
                        moves.append(Move((r, c), (r+1, c+1), self.board))
    #No en passant or pawn promotion


    #Rules for all possible rook moves
    def getRookMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != "Q":
                    self.pins.remove(self.pins[i])
                break

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemy = "b" if self.turn == "white" else "w"

        for d in directions:
            for i in range(1, 8):
                endRow = r+d[0]*i
                endCol = c+d[1]*i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                    if endPiece == " ":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemy:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break
    #No castling possiblity as of yet

    #Rules for all possible knight moves
    def getKnightMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        ally = "w" if self.turn == "white" else "b"
        for m in knightMoves:
            endRow = r+m[0]
            endCol = c+m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                if not piecePinned:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != ally:
                        moves.append(Move((r, c), (endRow, endCol), self.board))

    #Rules for all possible bishop moves
    def getBishopMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemy = "b" if self.turn == "white" else "w"

        for d in directions:
            for i in range(1, 8):
                endRow = r+d[0]*i
                endCol = c+d[1]*i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == " ":
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemy:
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
        ally = "w" if self.turn == "white" else "b"
        for i in range(8):
            endRow = r+rowMoves[i]
            endCol = c+colMoves[i]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != ally:
                    if ally == "w":
                        self.wKingLocation = (endRow, endCol)
                    else:
                        self.bKingLocation = (endRow, endCol)
                    check, pins, checks = self.pinsAndChecks()
                    if not check:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    if ally == "w":
                        self.wKingLocation = (r, c)
                    else:
                        self.bKingLocation = (r, c)


class Move():
    #Mapping list values to chessboard row names
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow*1000+self.startCol*100+self.endRow*10

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    #Converting chessboard row and column numbers to chessnotation.
    def getUCI(self):
        return self.getRankFile(self.startRow, self.startCol)+self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c]+self.rowsToRanks[r]


#The main function is code mimiced from the example code from stupid-chess-ai.
def main():
    ai = ChessEngine()

    while True:
        command = input()
        time.sleep(random.randrange(1,10)/100)
        if command.startswith("BOARD:"):
            ai.setBoard(command.removeprefix("BOARD:"))
        elif command.startswith("PLAY:"):
            dummy = Move((0, 0),(0, 0), ai.board)
            move = ai.makeMove(dummy)
            print(f"MOVE:{move.getUCI}")
        elif command.startswith("MOVE:"):
            move = command.removeprefix("MOVE:")
            ai.handleMove(move)
        elif command.startswith("RESET:"):
            ai.resetBoard()
        else:
            print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
