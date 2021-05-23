import chess
import chess.engine
import chess.pgn
import collections
import asyncio



def board_to_game(board):
    # from https://github.com/niklasf/python-chess/issues/63
    game = chess.pgn.Game()

    # Undo all moves.
    switchyard = collections.deque()
    while board.move_stack:
        switchyard.append(board.pop())

    game.setup(board)
    node = game

    # Replay all moves.
    while switchyard:
        move = switchyard.pop()
        node = node.add_variation(move)
        board.push(move)

    game.headers["Result"] = board.result()
    return game

def main():
    engine = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish", timeout=None)
    game = chess.pgn.Game()
    game.headers["Event"] = "Example"
    turn = True
    board = chess.Board()
    while not board.is_game_over():
        if turn:
            engine.configure({"Skill Level": 8})
        else:
            engine.configure({"Skill Level": 1})
        turn = not turn
        result = engine.play(board, chess.engine.Limit(time=0.1))
        board.push(result.move)

    print(board)
    print(board_to_game(board))
    engine.quit()
    return board

if __name__ == "__main__":
    # execute only if run as a script
    main()
