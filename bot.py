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

def evaluate(board, move):

    score = 0

    boardCopy = board.copy()
    boardCopy.push(move)

    #capture
    if boardCopy.is_capture(move):
        captured_piece = board.piece_at(move.to_square)
        if captured_piece:
            score += piece_values[captured_piece.piece_type]

    #center
    to_square = move.to_square
    if to_square in [chess.D4, chess.D5, chess.E4, chess.E5]:
        score += 0.5

    #castling
    if board.is_castling(move):
        score += 0.5
    
    #promtotion
    if move.promotion:
        score += 10

    #not in check
    if not boardCopy.is_check():
        score += 0.5

    return score

def move(board, botColor):
    if board.turn != botColor:
        return

    best_move = None
    best_score = -float('inf')

    for m in board.legal_moves:
        score = evaluate(board, m)
        if score > best_score:
            best_score = score
            best_move = m

    board.push(best_move)
    print(f"Bot plays: {best_move} (score: {best_score})")

