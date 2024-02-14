# Chess
Chess board with logic

A simple chessboard created in Python with all the logic necessary. Check, Checkmate, Promotion, Stalemate, Castling, Double Move, En Passant and Insufficient Material all work properly.
When a piece is clicked on all possible moves are calculated.
All moves are calculated by creating a second duplicate board. All moves are executed on this board to see if moving the piece does not reveal an attack on the king (in which case the piece is pinned)
If the king is in check, every move is calculated on the duplicate board aswell to see if it unchecks the king. If such a move exists it is only check (Check)
If there are no moves and the king is in check, the attacking player wins. (Checkmate)
If a pawn reaches the opposite side, it promotes to a knight, bishop, rook or queen. (Promotion)
If there are no moves and the king is not in check, the game ends in a draw (Stalemate)
If both the rook and the king have not moved, and the king is not in check, and the two squares the king wants to move does not result in the king being in check, the king can castle (Castling)
If a pawn hasn't move yet, it may move two squares instead of one (Double Move)
If a pawn hasn't move yet, and an opponent pawn is two squares in front of it and the unmoved pawn moves two squares so that both pawns are on the same rank, the attacking pawn may perform En Passant on the next move, but only on the next move. In En Passant the attacking pawn may attack the empty square behind the pawn that just moved two spaces, taking the defending pawn as if the pawn moved one space. (En Passant)
