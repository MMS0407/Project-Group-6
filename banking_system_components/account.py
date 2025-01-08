import csv
from typing import List, Dict
from banking_system_components.transaction import Transaction
import uuid

class Account:
    """Represents a bank account with balance and transaction history."""

    def __init__(self, first_name: str, last_name: str, age: int, state: str, job: str, account_type: str = "Checking", initial_balance: float = 0.0):
        """
        Initialize a bank account.

        Args:
            first_name (str): The first name of the account holder.
            last_name (str): The last name of the account holder.
            age (int): The age of the account holder.
            state (str): The state in the US where the account holder resides.
            job (str): The job title of the account holder.
            account_type (str): The type of account (Checking or Savings).
            initial_balance (float): The initial account balance (default: 0.0).
        """
        if account_type not in ["Checking", "Savings"]:
            raise ValueError("Invalid account type. Must be 'Checking' or 'Savings'.")
        self.account_id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.state = state
        self.job = job
        self.account_type = account_type
        self.balance = initial_balance
        self.transactions: List[Transaction] = []
    
    def update_info(self, first_name=None, last_name=None, age=None, state=None, job=None):
        """Update account information."""
        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name
        if age is not None:
            self.age = age
        if state:
            self.state = state
        if job:
            self.job = job

    def deposit(self, amount: float):
        """
        Deposit money into the account.

        Args:
            amount (float): The amount to deposit.
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be greater than zero.")
        self.balance += amount
        self.transactions.append(Transaction("Deposit", amount))
        self.export_balance_update()

    def withdraw(self, amount: float):
        """
        Withdraw money from the account.

        Args:
            amount (float): The amount to withdraw.

        Raises:
            ValueError: If the amount exceeds the balance or is non-positive.
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero.")
        if amount > self.balance:
            raise ValueError("Insufficient funds.")
        self.balance -= amount
        self.transactions.append(Transaction("Withdrawal", amount))
        self.export_balance_update()

    def transfer(self, target_account: 'Account', amount: float):
        """
        Transfer money to another account.

        Args:
            target_account (Account): The target account for the transfer.
            amount (float): The amount to transfer.

        Raises:
            ValueError: If the transfer amount exceeds the balance or is non-positive.
        """
        if amount <= 0:
            raise ValueError("Transfer amount must be greater than zero.")
        if amount > self.balance:
            raise ValueError("Insufficient funds for transfer.")
        self.balance -= amount
        target_account.balance += amount
        self.transactions.append(Transaction("Transfer Out", amount, target_account.account_id))
        target_account.transactions.append(Transaction("Transfer In", amount, self.account_id))
        self.export_balance_update()
        target_account.export_balance_update()
    
        
    def filter_transactions(self, transaction_type: str) -> List[Transaction]:
        """
        Filter transactions by type.

        Args:
            transaction_type (str): The type of transaction to filter.

        Returns:
            list: A list of transactions matching the given type.
        """
        return [t for t in self.transactions if t.transaction_type == transaction_type]

    def get_transaction_history(self) -> List[Dict]:
        """
        Retrieve all transactions in dictionary format.

        Returns:
            list: A list of dictionaries representing all transactions.
        """
        return [t.to_dict() for t in self.transactions]

    def export_balance_update(self):
        """
        Export the account balance to the CSV file after any balance update.
        """
        with open("accounts.csv", "r") as csvfile:
            reader = list(csv.DictReader(csvfile))

        with open("accounts.csv", "w", newline="") as csvfile:
            fieldnames = ["account_id", "first_name", "last_name", "age", "state", "job", "account_type", "balance"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            updated = False
            for row in reader:
                if row["account_id"] == self.account_id:
                    row["balance"] = f"{self.balance:.2f}"
                    updated = True
                writer.writerow(row)

            if not updated:
                writer.writerow({
                    "account_id": self.account_id,
                    "first_name": self.first_name,
                    "last_name": self.last_name,
                    "age": self.age,
                    "state": self.state,
                    "job": self.job,
                    "account_type": self.account_type,
                    "balance": f"{self.balance:.2f}",
                })

    def get_details(self):
        """Return a formatted string with account details."""
        return (
            f"Account ID: {self.account_id}\n"
            f"Account Holder: {self.first_name} {self.last_name}\n"
            f"Age: {self.age}\n"
            f"State: {self.state}\n"
            f"Job: {self.job}\n"
            f"Account Type: {self.account_type}\n"
            f"Balance: ${self.balance:.2f}"
        )

