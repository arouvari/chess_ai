Weekly report 5

What did I do this week: I made an simple evaluator that evaluates the game state depending on the balance of material. 
                         I made an undo move function for the minimax algorithm to work correctly while going recursively.
                         I also implemented a simple minimax algorithm that looks for the best move based on the evaluation of
                         the pieces. Minimax algorithm looks in depth of three to check for three to look for the next continuation after the 
                         opponents response to upcoming move.

How has the program progressed: The program is at a point where the main functionality works and can now be improved with new features or
                                optimization. New tests have also been made for checking that the evaluation function works. Seeing what
                                moves the algorithm makes, conveys new possible improvements that would improve the intelligence of the
                                AI.

What did I learn this week/today: I learned how to program a working minimax algorithm that chooses moves by evaluating the chessboard. 
                                  For reference I used chess programming wiki and wikipedia to look at pseudocode and descriptions on how
                                  the algorithm works to construct it.

What remains unclear or has been challenging: A lot of the problems arrised from the minimax algorithm. Small indentation and typo errors
                                              made it work in weird ways like only producing moves for white pieces or moving one piece
                                              back and forth. With only material evaluation white and black pieces open the game in very
                                              different ways.
                                      
What will I do next: I will next try to optimize my code to make it faster. Some moves take a while for the AI to make. I will also try to
                     make an evaluation system that takes into the account the board position. Extra rules like pawn promotion, castling or en
                     passant could be added after. Pawn promotion being quite important for pawn board evaluation.
