import random
import click
import logging

from faker import Faker

from bank.accounts.manage import create_account, create_customer, get_accounts, setup_db
from bank.simulation.simulate import simulate_transactions

faker = Faker("pl_PL")
logging.basicConfig(level=logging.INFO)


@click.group()
def cli():
    pass


@click.command(help="Create customers and accounts")
@click.option(
    "--accounts", type=int, help="Accounts number", default=random.randint(30, 150)
)
def create_accounts(accounts: int):
    setup_db()
    
    if accounts < 1:
        logging.error(
            "Invalid number of accounts or subaccounts. Value can't be negative."
        )
        return

    logging.info(f"Creating {accounts} accounts...")

    for i in range(accounts+1):

        first_name = faker.first_name()
        last_name = faker.last_name()

        customer_id = create_customer(
            first_name,
            last_name,
            faker.date_of_birth(),
            faker.address(),
            faker.city(),
            faker.region(),
            faker.zipcode(),
            faker.phone_number(),
            faker.email(),
        )
        account = create_account(customer_id, 'Checking')

        logging.info(f"#{i}/{accounts} Created account for {first_name} {last_name} with account number {account.account_number}")


@click.command()
@click.option("--days", type=int, help="Days to simulate", default=30)
@click.option("--day-time", type=int, help="Day time in seconds", default=86400)
@click.option("--transaction-fee", type=float, help="Transaction fee", default=0.01)
@click.option(
    "--internal-transaction-fee",
    type=float,
    help="Internal transaction fee between customer owned accounts",
    default=0.00,
)
@click.option("--max-transfer", type=int, help="Max transfer", default=1000)
def simulate(days: int, day_time: int, transaction_fee: float, internal_transaction_fee: float, max_transfer: int):
    logging.info(f"Simulating bank transactions for {days} days...")
    logging.info(f"Day time: {day_time} seconds")

    accounts = get_accounts()

    for day in range(days+1):
        logging.info(f"Day {day}/{days}")

        simulate_transactions(accounts, transaction_fee, internal_transaction_fee, max_transfer, day_time, day)
        
cli.add_command(create_accounts)
cli.add_command(simulate)

if __name__ == "__main__":
    cli()