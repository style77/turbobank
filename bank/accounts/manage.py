from dataclasses import dataclass
import random
import typing
import sqlite3
from datetime import date

import numpy as np


@dataclass
class Account:
    id: int
    account_number: str
    customer_id: int
    account_type: typing.Literal["Checking", "Savings", "Credit"]
    balance: float


def setup_db():
    with open('bank/schema.sql', 'r') as schema_file:
        conn = sqlite3.connect('turbobank.db')
        cursor = conn.cursor()
        cursor.executescript(schema_file.read())
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
    conn = sqlite3.connect('turbobank.db')
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO customers (first_name, last_name, date_of_birth, address, city, state, zip_code, phone, email)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
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
    
    customer_id = cursor.lastrowid

    cursor.close()  # Close the cursor before committing
    conn.commit()   # Commit after cursor is closed
    conn.close()

    return customer_id

def generate_account_balance(lambda_param=0.1, max_balance=10000):
    balance = np.random.exponential(scale=1/lambda_param)
    return min(balance, max_balance)

def create_account(customer_id: int, account_type: typing.Literal["Checking", "Savings", "Credit"]):
    # 20 characters acc number
    account_number = "".join(str(random.randint(0, 9)) for _ in range(20))

    # random balance with higher probability of lower values
    balance = generate_account_balance()

    conn = sqlite3.connect('turbobank.db')
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO accounts (account_number, customer_id, account_type, balance)
        VALUES (?, ?, ?, ?)
        """,
        (account_number, customer_id, account_type, balance),
    )
    
    account_id = cursor.lastrowid

    cursor.execute(
        """
        SELECT id, account_number, customer_id, account_type, balance FROM accounts WHERE id = ?
        """,
        (account_id,)
    )

    account = cursor.fetchone()

    cursor.close()  # Close the cursor before committing
    conn.commit()   # Commit after cursor is closed
    conn.close()

    return Account(*account)
    

def get_accounts():
    conn = sqlite3.connect('turbobank.db')
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
