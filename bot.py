import rules

def evaluate(board, move, botColor):
    simBoard = board.copy()
    
    #bot plays
    score = rules.rules(simBoard, move, botColor)
    
    #push bots best move
    simBoard.push(move)
    
    #opp responds
    opp_best = -float('inf')
    oppColor = not botColor
    opp_moves = list(simBoard.legal_moves)

    if not opp_moves:
        if simBoard.is_checkmate():
            opp_best = float('inf')  # bot wins
        else:
            opp_best = 0
    else:
        for opp_move in opp_moves:
            opp_score = rules.rules(simBoard, opp_move, oppColor)
            if opp_score > opp_best:
                opp_best = opp_score

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

