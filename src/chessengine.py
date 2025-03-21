import time
import random

class ChessEngine():
    def __init__(self):
        self.board = self.initialize()

    #This function initializes the chessboard as 8x8 mailbox with each letter representing a piece, white pieces are in uppercase and black pieces in lower case.
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

    def make_move(self):
        return "e2e4"

    def handle_move(self, move):
        print(f"Received move: {move}")

    def set_board(self, board_state):
        print(f"Set board to: {board_state}")

    def reset_board(self):
        self.board = self.initialize()
        print("Board reset!")

#The main function is code mimiced from the example code from stupid-chess-ai.
def main():
    ai = ChessEngine()

    while True:
        command = input()
        time.sleep(random.randrange(1,10)/100)
        if command.startswith("BOARD:"):
            ai.set_board(ai, command.removeprefix("BOARD:"))
        elif command.startswith("PLAY:"):
            move = ai.make_move()
            print(f"MOVE:{move}")
        elif command.startswith("MOVE:"):
            move = command.removeprefix("MOVE:")
            ai.handle_move(move)
        elif command.startswith("BOARD:"):
            board_state = command.removeprefix("BOARD:")
            ai.set_board(board_state)
        elif command.startswith("RESET:"):
            ai.reset_board()
        else:
            print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
