from encoder_decoder import MoveEncoder

from chess import Move

encoder = MoveEncoder()

for action in range(encoder.ACTION_SIZE):

    move = encoder.decode(action)

    new_action = encoder.encode(move)

    assert action == new_action

print("Passed!")