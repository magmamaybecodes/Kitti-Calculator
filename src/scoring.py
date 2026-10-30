
def create_session(players, bet, salami_amount, four_pairs_kitti):
    """
    Creates a new Kitti game session.
    """

    # Validate player count
    if len(players) < 2:
        raise ValueError("A game needs at least 2 players.")

    # Validate player names
    if len(set(players)) != len(players):
        raise ValueError("Player names must be unique.")

    if any(not name.strip() for name in players):
        raise ValueError("Player names cannot be empty.")

    # Validate amounts
    if bet <= 0 or salami_amount < 0:
        raise ValueError("Invalid bet or Salami amount.")

    # Calculate initial pool
    initial_pool = len(players) * bet

    # Create player balances
    balances = {}

    for player in players:
        balances[player] = -bet

    # Create session
    session = {
        "players": players,
        "bet": bet,
        "salami_amount": salami_amount,
        "four_pairs_kitti": four_pairs_kitti,
        "pool": initial_pool,
        "kitti_count": 0,
        "balances": balances,
        "active": True
    }

    return session


def add_kitti(session):
    """
    Adds one Kitti to the game.
    Every player contributes the initial bet again.
    """

    if not session["active"]:
        raise ValueError("This game session has ended.")

    bet = session["bet"]

    # Add another contribution from every player
    for player in session["players"]:
        session["balances"][player] -= bet

    # Increase the prize pool
    session["pool"] += len(session["players"]) * bet

    # Increase Kitti count
    session["kitti_count"] += 1

    return session


def normal_win(session, winner):
    """
    Ends the game and awards the entire pool to the winner.
    """

    if not session["active"]:
        raise ValueError("This game session has already ended.")

    if winner not in session["players"]:
        raise ValueError("Invalid winner.")

    # Award the entire pool to the winner
    session["balances"][winner] += session["pool"]

    # Empty the pool and end the game
    session["pool"] = 0
    session["active"] = False

    return session
