import chess
import player
import bot

#setup
colorPick = input("Please pick your color (black/white): ").strip().lower()
if colorPick == "white":
    playerColor = True
    botColor = False
elif colorPick == "black":
    playerColor = False
    botColor = True
else:
    print(f"its black or white not '{colorPick}'")
    exit()

board = chess.Board()
print(f"\nYou are {'white' if playerColor else 'black'}, the bot is {'white' if botColor else 'black'}.\n")

#main
while not board.is_game_over():
    print("")
    print(board)
    print("")

    if board.turn == playerColor:
        player.move(board, playerColor)
    else:
        bot.move(board, botColor)

#game over
print("\nGame over!")
print(f"Result: {board.result()}")
