Weekly report 2:

Most of this weeks work was on starting the development of the engine. I used the example code provided to connect my
code to the AI platform and started writing basic functions. For implementing the chessboard I used and 8x8 mailbox
representation. I made a class for representing the engine and a class for configuring the moves and translating
the chessboard to chess notation.

I have begun writing the code for the engine but there is no functionality yet that can be seen other than the
notation when moving pieces in the AI plaform. There are some placeholder functions made for code that I will write
later.

While researching I learned about different approaches to representing the board. I chose to pick an 8x8 mailbox
for it's simplicity since I don't need the highest performance for the project that could be had with bitboards.
I also learned how to connect my code with the AI platform.

This weeks work was not hard. It provided challenges first on how I should start coding my approach but the code
written is not that complex.

Next step is starting to code the legal moves for every piece. First just doing simple moves for all pieces while
keeping in mind checks and not worrying about harder moves like pawn promotion, castling or en passant.
