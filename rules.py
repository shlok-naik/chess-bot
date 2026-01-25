import chess

piece_values = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0
}

center = [chess.D4, chess.D5, chess.E4, chess.E5]
extended_center = [
    chess.C3, chess.C4, chess.C5, chess.C6, chess.D3, chess.D6,
    chess.E3, chess.E6, chess.F3, chess.F4, chess.F5, chess.F6
]

def rules(board, move, botColor):
    score = 0

    moved_piece = board.piece_at(move.from_square)
    if not moved_piece or moved_piece.color != botColor:
        return -float('inf')

    #opening
    if board.fullmove_number <= 10:
        if moved_piece.piece_type == chess.ROOK and not board.is_castling(move):
            score -= 20
        elif moved_piece.piece_type in [chess.KNIGHT, chess.BISHOP]:
            score += 5
        elif moved_piece.piece_type == chess.QUEEN:
            score -= 10
        if board.is_castling(move):
            score += 15
        if moved_piece.piece_type == chess.PAWN:
            if move.to_square in center:
                score += 10
            elif move.to_square in extended_center:
                score += 2

    #terminal
    if board.is_checkmate():
        return float('inf')
    elif board.is_stalemate() or board.is_repetition():
        return -50

    #capture
    if board.is_capture(move):
        captured = board.piece_at(move.to_square)
        if captured:
            score += piece_values[captured.piece_type] * 10
            score += (piece_values[captured.piece_type] - piece_values[moved_piece.piece_type])

    #dont let piece be captured
    if board.is_attacked_by(not botColor, move.to_square):
        attackers = len(board.attackers(not botColor, move.to_square))
        defenders = len(board.attackers(botColor, move.to_square))
        if attackers > defenders:
            score -= piece_values[moved_piece.piece_type] * 10

    #hanging
    for square in chess.SQUARES:
        p = board.piece_at(square)
        if p and p.color == botColor:
            attackers = len(board.attackers(not botColor, square))
            defenders = len(board.attackers(botColor, square))
            if attackers > defenders:
                score -= piece_values[p.piece_type] * 8

    #check
    if board.is_check():
        score += 5

    #open up pieces
    score += 0.05 * len(list(board.legal_moves))

    #center
    if move.to_square in center:
        score += 0.5
    elif move.to_square in extended_center:
        score += 0.2

    #castle
    if board.is_castling(move):
        score += 5 if board.fullmove_number <= 10 else 2

    #promotion
    if move.promotion == chess.QUEEN:
        score += 8
    elif move.promotion is not None:
        score += 5

    #push pawns
    if moved_piece.piece_type == chess.PAWN:
        score += 0.3 if move.to_square in center else 0.1

    #penalise repeated
    recent_moves = board.move_stack[-7:-1]
    for past_move in recent_moves:
        if past_move.from_square == move.to_square and past_move.to_square == move.from_square:
            score -= 0.5

    #king safe
    king_sq = board.king(botColor)
    attackers_on_king = len(board.attackers(not botColor, king_sq))
    if attackers_on_king > 0:
        score -= attackers_on_king * 3

    #dont let opp pin
    if board.is_pinned(botColor, move.to_square):
        score -= piece_values[moved_piece.piece_type] * 4

    #dont let opp develop
    opp_dev = 0
    for sq in chess.SQUARES:
        p = board.piece_at(sq)
        if p and p.color != botColor and p.piece_type in [chess.KNIGHT, chess.BISHOP]:
            if sq not in [chess.B1, chess.G1, chess.C1, chess.F1,
                          chess.B8, chess.G8, chess.C8, chess.F8]:
                opp_dev += 1
    score -= opp_dev * 1.5

    return score
