import chess

class MoveEncoder:
    ACTION_SIZE = 64 * 73

    KNIGHT_ORDER = [
        (-2, -1), (-2, 1),
        (-1, -2), (-1, 2),
        (1, -2), (1, 2),
        (2, -1), (2, 1),
    ]

    KNIGHT_TO_ID = {m: i for i, m in enumerate(KNIGHT_ORDER)}

    DIRS = [
        (-1, 0), (1, 0),
        (0, -1), (0, 1),
        (-1, -1), (-1, 1),
        (1, -1), (1, 1),
    ]

    DIR_TO_ID = {d: i for i, d in enumerate(DIRS)}

    # python-chess promotion constants
    PROMO_PIECE = {
        chess.KNIGHT: 0,
        chess.BISHOP: 1,
        chess.ROOK: 2,
    }

    PROMO_PIECES = [
        chess.KNIGHT,
        chess.BISHOP,
        chess.ROOK,
    ]

    # MOVE -> ACTION
    def encode(self, move: chess.Move):

        from_sq = move.from_square
        to_sq = move.to_square

        fr, ff = divmod(from_sq, 8)
        tr, tf = divmod(to_sq, 8)

        dr = tr - fr
        df = tf - ff

        promotion = move.promotion

        # QUEEN PROMOTION = normal move
        if promotion == chess.QUEEN:
            plane = self._encode_slide(dr, df)

        # UNDERPROMOTIONS
        elif promotion in self.PROMO_PIECE:

            # White promotion
            if dr > 0:

                if df == -1:
                    direction = 0
                elif df == 0:
                    direction = 1
                elif df == 1:
                    direction = 2
                else:
                    raise ValueError("Invalid promotion move")

            # Black promotion
            else:

                if df == 1:
                    direction = 0
                elif df == 0:
                    direction = 1
                elif df == -1:
                    direction = 2
                else:
                    raise ValueError("Invalid promotion move")

            plane = 64 + self.PROMO_PIECE[promotion] * 3 + direction

        # KNIGHTS
        elif (dr, df) in self.KNIGHT_TO_ID:

            plane = 56 + self.KNIGHT_TO_ID[(dr, df)]

        # SLIDING / QUEEN PROMO
        else:
            plane = self._encode_slide(dr, df)

        return from_sq * 73 + plane

    # ACTION -> MOVE
    def decode(self, action, board):

        for move in board.legal_moves:
            if self.encode(move) == action:
                return move

        raise ValueError(
            f"Action {action} is not legal in this position"
        )

    def _encode_slide(self, dr, df):

        if not (dr == 0 or df == 0 or abs(dr) == abs(df)):
            raise ValueError(f"Illegal sliding move ({dr},{df})")

        step_r = 0 if dr == 0 else (1 if dr > 0 else -1)
        step_f = 0 if df == 0 else (1 if df > 0 else -1)

        dir_id = self.DIR_TO_ID[(step_r, step_f)]

        distance = max(abs(dr), abs(df))

        if not (1 <= distance <= 7):
            raise ValueError("Invalid distance")

        return dir_id * 7 + (distance - 1)