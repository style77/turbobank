from bank.accounts.manage import get_accounts
from bank.simulation.simulate import simulate_transactions


def simulate_one_day(
    transaction_fee: float = 0.01,
    internal_transaction_fee: float = 0.00,
    max_transfer: float = 10000,
):
    accounts = get_accounts()
    simulate_transactions(
        accounts, transaction_fee, internal_transaction_fee, max_transfer, 0.01, 0
    )
