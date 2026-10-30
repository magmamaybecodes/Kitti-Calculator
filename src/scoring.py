from history import record_transaction

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
        "history": [],
        "active": True
    }

    return session



def add_kitti(session):
    """
    Adds one Kitti and records the transaction.
    """

    if not session["active"]:
        raise ValueError("This game session has ended.")

    bet = session["bet"]
    total_contribution = len(session["players"]) * bet

    for player in session["players"]:
        session["balances"][player] -= bet

    session["pool"] += total_contribution
    session["kitti_count"] += 1

    record_transaction(
        session,
        "Kitti",
        total_contribution,
        f"All {len(session['players'])} players contributed Rs. {bet}"
    )

    return session



def normal_win(session, winner):
    """
    Ends the game and records a normal win.
    """

    if not session["active"]:
        raise ValueError("This game session has already ended.")

    if winner not in session["players"]:
        raise ValueError("Invalid winner.")

    prize = session["pool"]

    session["balances"][winner] += prize
    session["pool"] = 0
    session["active"] = False

    record_transaction(
        session,
        "Normal Win",
        prize,
        f"{winner} won the game and received Rs. {prize}"
    )

    return session


    
def salami_win(session, winner):
    """
    Ends the game and awards the pool plus Salami to the winner.
    """

    if not session["active"]:
        raise ValueError("This game session has already ended.")

    if winner not in session["players"]:
        raise ValueError("Invalid winner.")

    # Calculate additional Salami
    salami = (len(session["players"]) - 1) * session["salami_amount"]

    # Deduct Salami from every other player
    for player in session["players"]:
        if player != winner:
            session["balances"][player] -= session["salami_amount"]

    # Award pool and Salami to the winner
    session["balances"][winner] += session["pool"] + salami

    # End the game
    session["pool"] = 0
    session["active"] = False

    return session

def four_of_a_kind_win(session, winner, rank):
    """
    Handles four of a kind and records the result.
    """

    if not session["active"]:
        raise ValueError("This game session has already ended.")

    if winner not in session["players"]:
        raise ValueError("Invalid winner.")

    valid_ranks = [
        "Ace", "King", "Queen", "Jack",
        "10", "9", "8", "7", "6", "5", "4", "3", "2"
    ]

    if rank not in valid_ranks:
        raise ValueError("Invalid card rank.")

    salami = 0

    if rank == "Ace":
        salami = (len(session["players"]) - 1) * session["salami_amount"]

        for player in session["players"]:
            if player != winner:
                session["balances"][player] -= session["salami_amount"]

    prize = session["pool"] + salami

    session["balances"][winner] += prize

    session["pool"] = 0
    session["active"] = False

    transaction_type = "Four Aces Win" if rank == "Ace" else "Four of a Kind Win"

    record_transaction(
        session,
        transaction_type,
        prize,
        f"{winner} won with four {rank}s"
    )

    return session


def four_pairs(session):
    """
    Handles a cancelled game caused by four pairs.
    """

    if not session["active"]:
        raise ValueError("This game session has ended.")

    if session["four_pairs_kitti"]:
        add_kitti(session)

        record_transaction(
            session,
            "Four Pairs",
            0,
            "Game cancelled. Kitti added according to session settings."
        )
    else:
        record_transaction(
            session,
            "Four Pairs",
            0,
            "Game cancelled. No additional Kitti added."
        )

    return session
    
def check_balances(session):
    """
    Checks whether all player balances add up to zero.
    """

    total_balance = sum(session["balances"].values())

    if total_balance == 0:
        return True

    return False




