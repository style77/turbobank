from dataclasses import dataclass
from datetime import date, datetime
import os
import random
import typing
import psycopg2
import numpy as np

def check_connection(database: str):
    try:
        conn = psycopg2.connect(database)
        conn.close()
        return True
    except psycopg2.OperationalError:
        return False

def get_connection():
    database = os.environ.get("POSTGRES_CONN_ID")
    if check_connection(database):
        return psycopg2.connect(database)
    
    hook = "postgres://postgres:postgres@postgres:5432/turbobank"
    if not check_connection(hook):
        raise Exception("Could not connect to the database.")
    return psycopg2.connect(hook)

@dataclass
class Account:
    id: int
    account_number: str
    customer_id: int
    account_type: typing.Literal["Checking", "Savings", "Credit"]
    balance: float


def setup_db():
    with open("bank/schema.sql", "r") as schema_file:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(schema_file.read())
        conn.commit()
        cursor.close()
        conn.close()


def create_customer(
    first_name: str,
    last_name: str,
    dob: date,
    address: str,
    city: str,
    state: str,
    zip_code: str,
    phone: str,
    email: str,
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO customers (first_name, last_name, date_of_birth, address, city, state, zip_code, phone, email)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
        """,
        (
            first_name,
            last_name,
            dob,
            address,
            city,
            state,
            zip_code,
            phone,
            email,
        ),
    )

    customer_id = cursor.fetchone()[0]

    cursor.close()  # Close the cursor before committing
    conn.commit()  # Commit after cursor is closed
    conn.close()

    return customer_id


def generate_account_balance(lambda_param=0.1, max_balance=10000):
    balance = np.random.exponential(scale=1 / lambda_param)
    return min(balance, max_balance)


def create_account(
    customer_id: int, account_type: typing.Literal["Checking", "Savings", "Credit"]
):
    # 20 characters acc number
    account_number = "".join(str(random.randint(0, 9)) for _ in range(20))

    # random balance with higher probability of lower values
    balance = generate_account_balance()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO accounts (account_number, customer_id, account_type, balance)
        VALUES (%s, %s, %s, %s)
        RETURNING id
        """,
        (account_number, customer_id, account_type, balance),
    )

    account_id = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT id, account_number, customer_id, account_type, balance FROM accounts WHERE id = %s
        """,
        (account_id,),
    )

    account = cursor.fetchone()

    cursor.close()  # Close the cursor before committing
    conn.commit()  # Commit after cursor is closed
    conn.close()

    return Account(*account)


def get_accounts():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, account_number, customer_id, account_type, balance FROM accounts
        """
    )

    accounts = cursor.fetchall()

    cursor.close()
    conn.close()

    return [Account(*account) for account in accounts]


def update_account_balance(account_id: int, new_balance: float, add: bool = False):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        (
            """
        UPDATE accounts SET balance = %s WHERE id = %s
        """
            if not sum
            else """
        UPDATE accounts SET balance = balance + %s WHERE id = %s
        """
        ),
        (new_balance, account_id),
    )

    cursor.close()
    conn.commit()
    conn.close()


def create_transaction(
    account_id: int,
    transaction_type: str,
    amount: float,
    created_at: datetime,
    description: str,
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO transactions (account_id, transaction_type, amount, created_at, description)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (account_id, transaction_type, amount, created_at, description),
    )

    cursor.close()
    conn.commit()
    conn.close()
