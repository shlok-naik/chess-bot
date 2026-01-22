import chess

def get_move():
    move = input("move:  ").strip()
    try:
        return chess.Move.from_uci(move)
    except:
        print("a proper move please")
        return None

def validation(board, move, playerColor):
    if move is None:
        return False
    piece = board.piece_at(move.from_square)
    if piece is None:
        print("theres no piece on that square idiot")
        return False
    if piece.color != playerColor:
        print("wrong color dumbo")
        return False
    if move not in board.legal_moves:
        print("illegal, read the rules before playing")
        return False
    return True

def move(board, playerColor):
    while True:
        move = get_move()
        if validation(board, move, playerColor):
            board.push(move)
            break