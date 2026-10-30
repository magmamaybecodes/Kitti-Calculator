
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
