import pytest
from chessengine import ChessEngine, Move

@pytest.fixture
def engine():
    return ChessEngine()

#Test that the board is setup correctly.
def test_board_initialize(engine):
    correct_board = [
            ["r", "n", "b", "q", "k", "b", "n", "r"],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            ["R", "N", "B", "Q", "K", "B", "N", "R"]
        ]
    assert engine.board == correct_board

#Test that white starts the game.
def test_starting_turn(engine):
    assert engine.turn == "white"

#Test king starting locations
def test_start_king_locations(engine):
    assert engine.wKingLocation == (7, 4)
    assert engine.bKingLocation == (0, 4)

#Test that UCI chessnotation is generated correctly.
def test_uci_generation():
    board = ChessEngine().board
    move = Move((6, 0), (4, 0), board)
    assert move.getUCI() == "a2a4"

#Test that makeMove function works.
def test_make_move(engine):
    move = Move((6, 0), (4, 0), engine.board)
    uci = engine.makeMove(move)
    assert uci == "a2a4"
    assert engine.board[6][0] == " "
    assert engine.board[4][0] == "P"
    assert engine.turn == "black"

#Testing handleMove function.
def test_handle_move(engine):
    engine.handleMove("e2e4")
    assert engine.board[6][4] == " "
    assert engine.board[4][4] == "P"
    assert engine.turn == "black"

#Checking that validMoves has all 20 possible moves in the starting position for white.
#2 possible moves for 8 pawns and 2 possible moves
def test_valid_moves_(engine):
    moves = engine.validMoves()
    assert len(moves) == 20
    assert all(isinstance(move, Move) for move in moves)
