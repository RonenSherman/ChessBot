import chess
import random

from encoding.encoder_decoder import MoveEncoder

encoder = MoveEncoder()

for _ in range(1000):

    board = chess.Board()

    for _ in range(random.randint(0, 50)):

        if board.is_game_over():
            break

        board.push(random.choice(list(board.legal_moves)))

    for move in board.legal_moves:

        action = encoder.encode(move)

        decoded = encoder.decode(action)

        assert move == decoded, (
            f"{move} -> {action} -> {decoded}"
        )

print("Passed")