
from scoring import create_session

players = ["Player 1", "Player 2", "Player 3", "Player 4", "Player 5"]

game = create_session(
    players=players,
    bet=10,
    salami_amount=10,
    four_pairs_kitti=True
)

print("Players:", game["players"])
print("Initial Pool: Rs.", game["pool"])
print("Kitti Count:", game["kitti_count"])
print("Player Balances:", game["balances"])
