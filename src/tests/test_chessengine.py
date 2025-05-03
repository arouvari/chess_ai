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
#2 possible moves for 8 pawns and 2 possible moves for 2 knights.
def test_valid_moves_(engine):
    moves = engine.validMoves()
    assert len(moves) == 20
    assert all(isinstance(move, Move) for move in moves)

#Checking that there are no checks at the start of the game.
def test_in_check_start(engine):
    assert not engine.isInCheck()

#Putting pieces in a position where black queen is checking the white king and using isInCheck function
#for validating that there is a check.
def test_check_detection(engine):
    engine.board[7][4] = " "
    engine.board[4][4] = "K"
    engine.board[0][4] = " "
    engine.board[3][4] = "k"
    engine.board[1][4] = " "
    engine.board[4][5] = "q"
    engine.wKingLocation = (4, 4)
    engine.bKingLocation = (3, 4)
    print(engine.board)
    assert engine.isInCheck()

#Test that checks that checkmate is evaluated correctly
def test_checkmate_evaluation(engine):
    test_board = [
            [" ", " ", " ", " ", " ", " ", " ", "k"],
            [" ", " ", " ", " ", " ", " ", " ", "Q"],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", "K", " ", " ", "R"]
        ]
    engine.board = test_board
    engine.turn = "black"
    engine.bKingLocation = (0, 7)
    engine.wKingLocation = (7, 4)
    assert engine.evaluateBoard() == 9999

#Testing correct stalemate evaluation
def test_stalemate_evaluation(engine):
    test_board = [
            [" ", " ", " ", " ", "k", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", "K", " ", " ", " "]
        ]
    engine.board = test_board
    assert engine.evaluateBoard() == 0

#Testing that captures work correctly using a pawn capture, seeing if score is updated.
def test_capture(engine):
    engine.board[4][4] = "P"
    engine.board[3][4] = "p"
    move = Move((4, 4), (3, 4), engine.board)
    uci = engine.makeMove(move)
    assert uci == "e4e5"
    assert engine.board[4][4] == " "
    assert engine.board[3][4] == "P"
    assert engine.score == 1
    assert engine.turn == "black"

#Testing that pawn promotion to a queen works.
def test_pawn_promotion(engine):
    engine.board[1][0] = "P"
    engine.board[0][0] = " "
    move = Move((1, 0), (0, 0), engine.board, promotionChoice="Q")
    uci = engine.makeMove(move)
    assert uci == "a7a8q"
    assert engine.board[1][0] == " "
    assert engine.board[0][0] == "Q"
    assert engine.score == 8
    assert engine.turn == "black"

#Test for castling. Checking that king and rook move to correct squares and castling rights are updated.
def test_castling_kingside(engine):
    engine.board[7][5] = " "
    engine.board[7][6] = " "
    move = Move((7, 4), (7, 6), engine.board)
    move.isCastle = True
    move.rookStart = (7, 7)
    move.rookEnd = (7, 5)
    move.rookMoved = "R"
    move.rookCaptured = " "
    uci = engine.makeMove(move)
    assert uci == "e1g1"
    assert engine.board[7][4] == " "
    assert engine.board[7][6] == "K"
    assert engine.board[7][7] == " "
    assert engine.board[7][5] == "R"
    assert engine.wKingLocation == (7, 6)
    assert not engine.whiteCastleKingside
    assert not engine.whiteCastleQueenside

#Testing that undo button works by capturing and undoing.
def test_undo_capture(engine):
    engine.board[4][4] = "P"
    engine.board[3][4] = "p"
    move = Move((4, 4), (3, 4), engine.board)
    engine.makeMove(move)
    engine.undoMove()
    assert engine.board[4][4] == "P"
    assert engine.board[3][4] == "p"
    assert engine.score == 0
    assert engine.turn == "white"

#Testing undo correctness after promoting a pawn.
def test_undo_promotion(engine):
    engine.board[1][0] = "P"
    engine.board[0][0] = " "
    move = Move((1, 0), (0, 0), engine.board, promotionChoice="Q")
    engine.makeMove(move)
    engine.undoMove()
    assert engine.board[1][0] == "P"
    assert engine.board[0][0] == " "
    assert engine.score == 0
    assert engine.turn == "white"

#Testing that all moves while king is in check are correct.
def test_valid_moves_in_check(engine):
    engine.board = [
        ["r", " ", " ", " ", "k", " ", " ", " "],
        ["p", "p", "p", "p", " ", "p", "p", "p"],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", "Q", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        ["P", "P", "P", "P", "P", "P", "P", "P"],
        ["R", "N", "B", " ", "K", "B", "N", "R"]
    ]
    engine.wKingLocation = (7, 4)
    engine.bKingLocation = (0, 4)
    engine.turn = "black"
    moves = engine.validMoves()
    assert len(moves) == 2
    uci_moves = [move.getUCI() for move in moves]
    assert set(uci_moves) == {"e8d8", "e8f8"}

#Testing all possible moves for a pawn.
def test_possible_pawn_moves(engine):
    engine.board[6][4] = "P"
    engine.board[5][4] = " "
    engine.board[4][4] = " "
    engine.board[5][5] = "p"
    moves = []
    engine.getPawnMoves(6, 4, moves)
    uci_moves = [move.getUCI() for move in moves]
    assert set(uci_moves) == {"e2e3", "e2e4", "e2f3"}

#Testing that checking with a knight works correctly.
def test_is_in_check_knight(engine):
    engine.board[7][4] = " "
    engine.board[5][5] = "K"
    engine.board[0][4] = " "
    engine.board[3][4] = "k"
    engine.board[4][3] = "n"
    engine.wKingLocation = (5, 5)
    engine.bKingLocation = (3, 4)
    assert engine.isInCheck()

#Testing pins_and_checks function correction.
def test_pins_and_checks(engine):
    engine.board = [
        [" ", " ", " ", " ", "k", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", "b", " ", " ", " ", " ", " ", " "],
        [" ", " ", "P", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", "K", " ", " ", " "]
    ]
    engine.wKingLocation = (7, 4)
    engine.bKingLocation = (0, 4)
    check, pins, checks = engine.pinsAndChecks()
    assert not check
    assert len(pins) == 1
    assert len(checks) == 0

#Testing board evaluation based on material.
def test_evaluate_board_material(engine):
    engine.board[6][0] = " "
    score = engine.calculateScore()
    assert score == -1

#Testing that the UCI notation for promition of a pawn to a queen works.
def test_handle_move_promotion(engine):
    engine.board[1][0] = "P"
    engine.board[0][0] = " "
    engine.handleMove("a7a8q")
    assert engine.board[1][0] == " "
    assert engine.board[0][0] == "Q"
    assert engine.turn == "black"

#Testing that the best move is chosen by the AI, eg. pawn takes the queen.
def test_make_best_move(engine):
    engine.board[4][4] = "P"
    engine.board[3][5] = "q"
    move = engine.bestMove(depth=2)
    assert move in engine.validMoves()
    engine.makeMove(move)
    assert engine.board[3][5] == "P"
