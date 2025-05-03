# Implementation Document

## General Structure of the Program

### Key Components
1. **`ChessEngine` Class**:  
   - Manages game state (board, turn, castling rights, king locations).  
   - Implements move generation, validation, and execution.  
   - AI logic via minimax with alpha-beta pruning.  
   - Positional evaluation using piece-specific score tables.  

2. **`Move` Class**:  
   - Represents a chess move (start/end positions, promotions, castling).  
   - Converts moves to/from UCI notation.  

3. **Main Loop**:  
   - Handles commands (`BOARD:`, `PLAY:`, `MOVE:`, `RESET:`).  
   - Interfaces with the AI to generate moves.  

### Workflow
- **Initialization**: Board setup, turn assignment, castling rights.  
- **Move Generation**: Valid moves generated based on checks/pins.  
- **AI Decision**: Uses minimax to evaluate positions and select optimal moves.  
- **Execution**: Moves applied to the board, game state updated.  


## Achieved Time and Space Complexities

### Key Algorithms & Complexities
1. **Minimax with Alpha-Beta Pruning**:  
   - **Time**: **O(b^(d/2))**, where `b` = branching factor (~35 for chess), `d` = depth (default 3).  
   - **Space**: **O(d)** for recursion stack.  

2. **Move Generation**:  
   - **Time**: **O(n)** per piece, where `n` = number of squares a piece can attack.  
   - **Space**: **O(m)** to store valid moves, where `m` ≈ 20–40 in mid-game.  

3. **Board Evaluation**:  
   - **Time**: **O(64)** (constant) to scan all squares for material/positional scores.  

### Shortcomings
1. **Missing Features**:  
   - No en passant or threefold repetition.  
   - Limited castling checks (e.g., path safety not fully validated).  
2. **Performance**:  
   - Depth-limited AI (~3 ply) makes suboptimal decisions.  
   - No transposition tables or move ordering optimizations.  


## Use of Large Language Models (LLMs)

- **ChatGPT** was used to:  
  - Check for typos in the code.

## Sources

1. **Positional Score Tables**:  
   Adapted from [BlackWidow-Chess](https://github.com/amir650/BlackWidow-Chess).  
2. **Minimax & Alpha-Beta**:  
   [Chess Programming Wiki](https://www.chessprogramming.org).  

