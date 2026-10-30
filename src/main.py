
from scoring import create_session, add_kitti, normal_win

players = ["Player 1", "Player 2", "Player 3", "Player 4", "Player 5"]

game = create_session(players, 10, 10, True)

add_kitti(game)
add_kitti(game)

normal_win(game, "Player 1")

print("Final Pool:", game["pool"])
print("Game Active:", game["active"])
print("Final Balances:", game["balances"])
