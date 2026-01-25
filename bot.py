import rules

def evaluate(board, move, botColor):
    simBoard = board.copy()

    #bot moves
    move_score = rules.rules(simBoard, move, botColor)

    #play bots move
    simBoard.push(move)

    #opp response
    oppColor = not botColor
    opp_best = -float('inf')
    for opp_move in simBoard.legal_moves:
        opp_score = rules.rules(simBoard, opp_move, oppColor)
        if opp_score > opp_best:
            opp_best = opp_score

    if opp_best == -float('inf'):
        opp_best = 0

    return move_score - opp_best



def move(board, botColor):
    if board.turn != botColor:
        return

    legal_moves = list(board.legal_moves)
    if not legal_moves:
        print("gg")
        return

    best_move = max(legal_moves, key=lambda m: evaluate(board, m, botColor))
    best_score = evaluate(board, best_move, botColor)

    board.push(best_move)
    print(f"Bot plays {best_move} (score {best_score})")

