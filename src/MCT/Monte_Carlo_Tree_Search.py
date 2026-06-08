import chess
import random
import math


class Node:
    def __init__(self, board, parent=None, move=None):
        self.parent = parent
        self.move = move

        self.wins = 0.0
        self.visits = 0

        self.children = []
        self.untried_moves = list(board.legal_moves)

        # player who made the move leading to this node
        self.player = not board.turn

    def select_child(self):
        return max(
            self.children,
            key=lambda c: c.wins / c.visits
            + math.sqrt(2 * math.log(self.visits) / c.visits)
        )

    def expand(self, move, board):
        child = Node(board, parent=self, move=move)

        self.untried_moves.remove(move)
        self.children.append(child)

        return child

    def update(self, result):
        self.visits += 1
        self.wins += result


def game_result(board):
    """
    Returns:
        1.0 = White win
        0.0 = Black win
        0.5 = Draw
    """

    outcome = board.outcome()

    if outcome.winner is None:
        return 0.5

    return 1.0 if outcome.winner else 0.0


def mcts(root_board, iterations):
    root = Node(root_board)

    for _ in range(iterations):

        node = root
        board = root_board.copy()

        # Selection
        while not node.untried_moves and node.children:
            node = node.select_child()
            board.push(node.move)

        # Expansion
        if node.untried_moves:
            move = random.choice(node.untried_moves)

            board.push(move)
            node = node.expand(move, board)

        # Rollout
        while not board.is_game_over():
            board.push(random.choice(list(board.legal_moves)))

        result = game_result(board)

        # Backpropagation
        while node is not None:

            if node.player == chess.WHITE:
                node.update(result)
            else:
                node.update(1.0 - result)

            node = node.parent

    return max(root.children, key=lambda c: c.visits).move