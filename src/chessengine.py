import time
import random

class ChessEngine():
    def __init__(self):
        self.board = self.initialize()
        self.moves = []
        self.turn = "white"


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

    def make_move(self, move):
        self.board[move.startRow][move.startCol] = " "
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moves.append(move)
        self.turn = "black" if self.turn == "white" else "white"
        return move.getChessNotation()

    def handle_move(self, move):
        print(f"Received move: {move}")

    def set_board(self, board_state):
        print(f"Set board to: {board_state}")

    def reset_board(self):
        self.board = self.initialize()
        print("Board reset!")


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

    #Converting chessboard row and column numbers to chessnotation.
    def getChessNotation(self):
        nameConvert = {"r":"R", "R":"R", "b":"B", "B":"B", "n":"N",
        "N":"N", "q":"Q", "Q":"Q", "k":"K", "K":"K"}
        notation = ""
        if self.pieceCaptured == " ":
            if self.pieceMoved in ("P", "p"):
                notation = self.getRankFile(self.endRow, self.endCol)
            else:
                notation = nameConvert.get(self.pieceMoved, "") + self.getRankFile(self.endRow, self.endCol)
        else:
            if self.pieceMoved in ("P", "p"):
                start_file = self.colsToFiles[self.startCol]
                notation = f"{start_file}x{self.getRankFile(self.endRow, self.endCol)}"
            else:
                piece = nameConvert.get(self.pieceMoved, "")
                notation = f"{piece}x{self.getRankFile(self.endRow, self.endCol)}"
        return notation

    #Help function for getChessNotation function
    def getRankFile(self, r, c):
        return self.colsToFiles[c]+self.rowsToRanks[r]

#The main function is code mimiced from the example code from stupid-chess-ai.
def main():
    ai = ChessEngine()

    while True:
        command = input()
        time.sleep(random.randrange(1,10)/100)
        if command.startswith("BOARD:"):
            ai.set_board(command.removeprefix("BOARD:"))
        elif command.startswith("PLAY:"):
            dummy = Move((0, 0),(0, 0), ai.board)
            move = ai.make_move(dummy)
            print(f"MOVE:{move}")
        elif command.startswith("MOVE:"):
            move = command.removeprefix("MOVE:")
            ai.handle_move(move)
        elif command.startswith("RESET:"):
            ai.reset_board()
        else:
            print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
