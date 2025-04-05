Weekly report 4

What did I do this week:
    I completed basic move generation for all pieces. Pawn promotion, en passant and
    castling have not been made but maybe later on. Checks and pins are validated
    correctly. There is a random move generating algorithm that chooses randomly one
    move for the AI from valid moves. Simple unittests are provided that mainly
    check that the starting position and rules are correct and making moves works.

How has the program progressed:
    Program has moved to the phase that it is connected to the AI platform and
    bugs are much easier to see when playing against the engine or the engine
    playing against itself. Chess rules that are implemented  at the moment should
    work.

What did I learn this week/today:
    I learned about how to connect chess logic to the mailbox and how to represent
    chess moves with list inputs. I learned how to implement sliding moves for rooks
    and bishops, making pawn attack for black and white work in the right direction.

What remains unclear or has been challenging:
    Most challenging part was making the checks and pins work having to take in account
    for every piece if moving it affects whether something is pinned or puts the king in check.
    Also getting my program to work with the AI platform had some challenges. I had to change the
    way it was checked if moved piece is white or black for many functions to get it to work and
    the AI was making non valid moves frequently before fixing bugs.


What will I do next:
    Next I will start by making an evaluation system that evaluates the position based on material
    and based on where the pieces are. After that I can remove the random move AI and implement
    minmax algorithm. Maybe also try to add pawn promotion, en passant and castling.
