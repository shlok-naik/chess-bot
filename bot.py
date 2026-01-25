import chess
import random

piece_values = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0
}

center = [chess.D4, chess.D5, chess.E4, chess.E5]
extended_center = [chess.C3, chess.C4, chess.C5, chess.C6, chess.D3,chess.D6, chess.E3,chess.E6, chess.F3, chess.F4, chess.F5, chess.F6]

def rules(board, move, botColor):
    score = 0

    moved_piece = board.piece_at(move.to_square)
    if not moved_piece or moved_piece.color != botColor:
        return -float('inf')

    if board.fullmove_number <= 10:
        if moved_piece.piece_type == chess.ROOK and not board.is_castling(move):
            score -= 20
        elif moved_piece.piece_type in [chess.KNIGHT, chess.BISHOP]:
            score += 15
        elif moved_piece.piece_type == chess.QUEEN:
            score -= 10
        if board.is_castling(move):
            score += 15
        if moved_piece.piece_type == chess.PAWN:
            if move.to_square in center:
                score += 5
            elif move.to_square in extended_center:
                score += 2

    #terminal
    if board.is_checkmate():
        return float('inf')
    elif board.is_stalemate() or board.is_repetition():
        return -50

    #capture
    if board.move_stack and len(board.move_stack) > 0:
        #undo to check
        board.pop()
        if board.is_capture(move):
            captured = board.piece_at(move.to_square)
            if captured:
                score += piece_values[captured.piece_type] * 10
                score += (piece_values[captured.piece_type] - piece_values[moved_piece.piece_type])
        board.push(move)

    #hanging all
    for square in chess.SQUARES:
        p = board.piece_at(square)
        if p and p.color == botColor:
            attackers = list(board.attackers(not botColor, square))
            defenders = list(board.attackers(botColor, square))
            if len(attackers) > len(defenders):
                score -= piece_values[p.piece_type] * 8
    
    #hanging moved
    if board.is_attacked_by(not botColor, move.to_square):
        defenders = len(board.attackers(botColor, move.to_square))
        attackers = len(board.attackers(not botColor, move.to_square))
        if attackers > defenders:
            score -= piece_values[moved_piece.piece_type] * 10

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

    #castling
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
    repeat_penalty = 0
    recent_moves = board.move_stack[-7:-1]
    for past_move in recent_moves:
        if past_move.from_square == move.to_square and past_move.to_square == move.from_square:
            repeat_penalty += 0.5
    score -= repeat_penalty

    return score


def evaluate(board, move, botColor):
    simBoard = board.copy()
    simBoard.push(move)

    #bot plays
    score = rules(simBoard, move, botColor)

    #opp responds
    opp_best = -float('inf')
    oppColor = not botColor
    opp_moves = list(simBoard.legal_moves)

    if not opp_moves:
        if simBoard.is_checkmate():
            opp_best = float('inf')  #bot wins
        else:
            opp_best = 0
    else:
        for opp_move in opp_moves:
            simBoard.push(opp_move)
            opp_score = rules(simBoard, opp_move, oppColor)
            simBoard.pop()
            if opp_score > opp_best:
                opp_best = opp_score

    if opp_best == -float('inf'):
        opp_best = 0

    return score - opp_best


def move(board, botColor):
    if board.turn != botColor:
        return

    best_move = None
    best_score = -float('inf')

    legal_moves = list(board.legal_moves)
    if not legal_moves:
        print("gg")
        return

    for m in legal_moves:
        score = evaluate(board, m, botColor)

        if score > best_score:
            best_score = score
            best_move = m

    if best_move is None:
        best_move = legal_moves[0]
        best_score = evaluate(board, best_move, botColor)

    board.push(best_move)
    print(f"Bot plays {best_move} (score {best_score})")


