
from scoring import create_session, four_pairs

players = ["Player 1", "Player 2", "Player 3", "Player 4", "Player 5"]

game = create_session(players, 10, 10, False)

print("Before Four Pairs:", game["pool"])

four_pairs(game)

print("After Four Pairs:", game["pool"])
print("Kitti Count:", game["kitti_count"])
print("Balances:", game["balances"])
