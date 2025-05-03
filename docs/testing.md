# Testing Document

## Unit Testing Coverage

### Core Components Tested
- **Board Initialization**: Verified starting positions, king locations, and castling rights.
- **Move Execution**: Pawn moves, captures, promotions, castling, and undo functionality.
- **Game State Checks**: Check detection, checkmate, stalemate, and valid move generation.
- **AI Logic**: Minimax algorithm, board evaluation (material/positional scores).
- **Special Moves**: Castling, pawn promotion, pinned pieces.

## Tested Scenarios & Methods

### 1. Board Setup & Basics
- `test_board_initialize`: Validates starting board configuration.
- `test_start_king_locations`: Confirms kings start at (7,4) and (0,4).

### 2. Move Execution
- `test_make_move`: Pawn advances (`a2a4`), updates board state, and switches turn.
- `test_capture`: Pawn captures opponent, updates score (material difference).
- `test_castling_kingside`: King and rook move, castling rights revoked.

### 3. Check & Endgame Logic
- `test_check_detection`: Detects queen attacking king.
- `test_checkmate_evaluation`: Returns `9999` for checkmate (black to move).
- `test_stalemate_evaluation`: Returns `0` for stalemate.

### 4. Special Moves
- `test_pawn_promotion`: Promotes pawn to queen, updates score (+8 for white).
- `test_undo_promotion`: Reverts promotion, restores original board state.

### 5. AI Decision-Making
- `test_make_best_move`: AI prioritizes capturing a queen with a pawn.

---

## Input Types
- **Valid UCI Moves**: `e2e4`, `a7a8q` (promotion), `e1g1` (castling).
- **Board Configurations**: Checkmate/stalemate setups, pinned pieces.
- **Edge Cases**: Pawns at promotion squares, kings in castling positions.

---

## Reproduction Steps
1. **Install Dependencies**:
   ```bash
   poetry run pytest
