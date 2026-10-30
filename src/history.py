
def record_transaction(session, transaction_type, amount, description):
    """
    Records a financial transaction in the game history.
    """

    transaction = {
        "type": transaction_type,
        "amount": amount,
        "description": description
    }

    session["history"].append(transaction)

    return transaction
