from datetime import datetime, timedelta
import random
import time
import typing
import logging

from bank.accounts.manage import Account, update_account_balance, create_transaction


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
def simulate_transactions(accounts: typing.List[Account], transaction_fee: float, internal_transaction_fee: float, max_transfer: float, day_time: int | None, day: int):
    transactions_to_perform = random.randint(1, len(accounts) // 5)
    logging.info(f"Simulating {transactions_to_perform} transactions.")

    total_time_elapsed = 0
    
    # add a day to the current date
    tx_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=day)

    for i in range(transactions_to_perform):
        account = random.choice(accounts)
        
        transaction_type = random.choice(
            ['Deposit', 'Withdrawal', 'Transfer', 'Payment']
        )
        
        amount = round(random.uniform(0.01, max_transfer), 2)
        target_account = None

        if transaction_type == 'Withdrawal':
            if amount + transaction_fee > account.balance:
                continue
            net_amount = amount + transaction_fee
            new_balance = account.balance - net_amount

        elif transaction_type == 'Transfer':
            target_account = random.choice(accounts)
            while target_account.id == account.id:
                target_account = random.choice(accounts)
            
            transfer_amount = max(amount - internal_transaction_fee, 0.01)
            if transfer_amount + transaction_fee > account.balance:
                continue
            new_balance = account.balance - (transfer_amount + transaction_fee)

            update_account_balance(target_account.id, transfer_amount, True)
            create_transaction(target_account.id, 'Deposit', transfer_amount, tx_date, f'Transfer from account {account.account_number}')

        elif transaction_type == 'Payment':
            if amount + transaction_fee > account.balance:
                continue
            net_amount = amount + transaction_fee
            new_balance = account.balance - net_amount

        else:  # Deposit
            new_balance = account.balance + amount

        operator = '+' if new_balance > account.balance else '-'
        logging.info(f"{transaction_type} | {account.account_number} > {target_account.account_number if target_account else 'N/A'} | Balance={account.balance:.2f} > {new_balance:.2f} ({operator}{amount:.2f})")

        update_account_balance(account.id, new_balance)
        create_transaction(account.id, transaction_type, amount, tx_date, 'Auto-generated transaction')
        
        account.balance = new_balance

        if day_time is None:
            continue

        if i < transactions_to_perform - 1:
            remaining_time = day_time - total_time_elapsed
            max_sleep_time = remaining_time / (transactions_to_perform - i)
            sleep_time = random.uniform(0.01, max_sleep_time)
            total_time_elapsed += sleep_time

            if sleep_time > 0:
                time.sleep(sleep_time)