
from scoring import create_session, add_kitti, salami_win, check_balances

players = ["Player 1", "Player 2", "Player 3", "Player 4", "Player 5"]

game = create_session(players, 10, 10, True)

add_kitti(game)
add_kitti(game)

salami_win(game, "Player 1")

print("Final Pool:", game["pool"])
print("Final Balances:", game["balances"])

if check_balances(game):
    print("Balance Check: PASSED")
else:
    print("Balance Check: FAILED")
