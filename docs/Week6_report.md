Weekly report 6

What did I do this week: I made changes to the evaluation to take in account the positioning on the board. The placing of a piece affects
                        the score of that piece, eg. Pawns are better on the penultimate rank where they are close to promotion.
                        I added pawn promotion and castling to the engine to make positional evaluation more logical. I also added alpha-beta pruning to
                        the minmax algorithm to prune trees that leave you in a worse position. Also refined the code logic in pinning to
                        fix a bug.

How has the program progressed: The program is now mostly complete. Engine makes logical moves based on piece score difference and positional
                                advantage and there are no bugs in the logic. Code has also been optimized to work faster in times where there
                                is needed longer searching through the three. En passant is emitted for now.

What did I learn this week/today: I learned how to make evaluation based on the positioning of the pieces. I learned about alpha-beta pruning for
                                  the minmax algorithm, how it works and how it is implemented. I learned how to make pawn promotion work.

What remains unclear or has been challenging: Most challengin part was finding a bug in pinning pieces, where the AI tried to move pinned pieces that
                                              resulted in the game being halted since the engine thought the move was legal and made but the platform
                                              waited for a valid move.
                                      
What will I do next: Next I will improve the testing and documentation of the code. I will also improve the code quality and structure. I will complete
                          the all the documentation of the project.
