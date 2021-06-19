import chess
import chess.engine
import chess.pgn
import collections
import asyncio
import io

CHESS_CPU = {"stockfish": "/usr/games/stockfish"}


class ChessPlayer:
    def __init__(self, playerName="stockfish", timeLimitms=100, level=1, timeout=None):
        self.playerName = playerName.lower()
        self.timeLimit = float(timeLimitms) / 1000
        self.level = int(level)
        self.timeout = timeout
        self.engine = False
        self.isEngine = False

        if self.playerName in CHESS_CPU:
            self.isEngine = True
            self.engine = chess.engine.SimpleEngine.popen_uci(
                CHESS_CPU[self.playerName], timeout=self.timeout
            )
            self.engine.configure({"Skill Level": self.level})

    def __del__(self):
        if self.isEngine:
            self.engine.quit()

    def configure(self, d):
        if self.playerName != "human":
            self.engine.configure(d)

    def play(self, chessBoard):
        return self.engine.play(chessBoard, chess.engine.Limit(time=self.timeLimit))

    def get_player(self):
        return self.playerName

    def get_level(self):
        return self.level

    def get_timeout(self):
        return self.timeout

    def get_time_limit(self):
        return self.timeLimit


def playOneCPU(player, level, limit):
    pass


class ChessGame:
    def __init__(self, p1, p2, whiteTurn=True, title="chessdynamics"):
        self.board = chess.Board()
        self.game = chess.pgn.Game()
        self.node = self.game
        self.white = p1
        self.black = p2
        self.white_turn = whiteTurn
        self.title = title

    def print_game(self):
        return str(board)

    def load_PGN(self, pgn):
        self.game = chess.pgn.read_game(io.StringIO(pgn))

    def is_game_over(self):
        return self.board.is_game_over()

    def play_turn(self):
        if not self.is_game_over():
            if self.white_turn:
                result = self.white.play(self.board)
            else:
                result = self.black.play(self.board)
            self.node = self.node.add_variation(result.move)
            self.white_turn = not self.white_turn
            self.board.push(result.move)
            return result.move
        else:
            return "gg"

    def play_continuous(self):
        while not self.is_game_over():
            self.play_turn()

    def get_PGN(self):
        self.set_headers()
        return str(self.game)

    def set_headers(self):
        self.game.headers["Event"] = self.title
        if self.white.get_player() not in CHESS_CPU:
            self.game.headers["White"] = self.white.get_player()
        else:
            self.game.headers["White"] = (
                self.white.get_player() + ":" + str(self.white.get_level())
            )
        if self.black.get_player() not in CHESS_CPU:
            self.game.headers["Black"] = self.black.get_player()
        else:
            self.game.headers["Black"] = (
                self.black.get_player() + ":" + str(self.black.get_level())
            )
        self.game.headers["Result"] = self.board.result()
        self.game.headers["Site"] = "ChessDynamics"

# class Game(models.Model):
#     title = models.CharField(max_length=200, default="untitled game")
#     description = models.CharField(max_length=500, default="test game")
#     PGN = models.CharField(max_length=20000, default="")
#     black = models.CharField(max_length=200, default="stockfish")
#     black_level = models.IntegerField(default=1)
#     white = models.CharField(max_length=200, default="stockfish")
#     white_level = models.IntegerField(default=1)
#     time_controls = models.IntegerField(default=100)
#     white_move = models.BooleanField(default=True)

#     def setup_white(self):
#         return ChessPlayer(self.white, self.time_controls, self.white_level)


#     def setup_black(self):
#         return ChessPlayer(self.black, self.time_controls, self.black_level)

#     def setup_game(self):
#         w = self.setup_white()
#         b = self.setup_black()
#         cg = ChessGame(w, b, self.white_move, self.title)
#         if len(self.PGN) > 0:
#             cg.load_PGN(self.PGN)
#         return cg

#     def __str__(self):
#         return self.setup_game().get_PGN()
    
#     def load_PGN(self, pgn):
#         self.PGN = pgn
    
#     def is_game_over(self):
#         return self.setup_game().is_game_over()
    
#     def play_turn(self):
#         g = self.setup_game()
#         move = g.play_turn()
#         self.PGN = g.get_PGN()
#         return move
    
#     def play_continuous(self):
#         moves = list()
#         g = self.setup_game()
#         moves.append(g.play_turn())
#         self.PGN = g.get_PGN()
#         return moves
    
#     def get_PGN(self):
#         return self.setup_game().get_PGN()
    
#     def print_game(self):
#         return self.setup_game().print_game()

#     def get_white_player(self):
#         return self.setup_white().get_player()
    
#     def get_black_player(self):
#         return self.setup_black().get_player()
    
#     def get_white_level(self):
#         return self.setup_white().get_level()
    
#     def get_black_level(self):
#         return self.setup_black().get_level()
