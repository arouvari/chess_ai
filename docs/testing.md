Testing Document

[COVERAGE REPORT](https://arouvari.github.io/chess_ai/htmlcov/index.html)

What was tested and how:
    All tests are currently done by pytest testing important functions.
    Chessboard starting position is tested with checking that all pieces are in
    correct places, there are no kings in check, king starting locations are
    mapped correctly and starting turn is for white. Move making and
    move handling functions are tested. There is a test for the
    correct chess notation(UCI) generation. One position is tested for
    checking if king is in check. Testing for the evaluation function is
    provided.

What types of inputs were used for testing:
    Move generation tests use simple legal starting moves as test inputs.
    Also the UCI generation is done with a simple move.
    King checking function is tested with setting the pieces to a clear
    checking position for black and using isInCheck to check that it
    works correctly. Valid starting moves for white are validated by
    checking that there are exactly 20 possible moves. Evaluation function is
    tested using the starting, checkmate and stalemate positions.

How can the tests be reproduced:
    1. Go to the root directory in the terminal
    2. Paste command: poetry run pytest
