import csv
import random
from typing import Dict
from account import Account

class Bank:
    """Represents a bank with multiple accounts."""

    def __init__(self):
        """Initialize the bank with an empty account database."""
        self.accounts: Dict[str, Account] = {}
        self.load_initial_accounts()

    def load_initial_accounts(self):
        first_names = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", "William", "Elizabeth"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
        states = [
            "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware",
            "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana",
            "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota"
        ]

        for i in range(20):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            age = random.randint(18, 80)
            state = random.choice(states)
            job = "Retired" if age > 67 else random.choice(["Employed", "Unemployed"])
            account_type = "Checking" if i % 2 == 0 else "Savings"
            balance = round(random.uniform(100.0, 10000.0), 2)

            self.create_account(first_name, last_name, age, state, job, account_type, balance)

        self.export_accounts_to_csv()

    def create_account(self, first_name: str, last_name: str, age: int, state: str, job: str, account_type: str = "Checking", initial_balance: float = 0.0) -> str:
        """
        Create a new account.

        Args:
            first_name (str): The first name of the account holder.
            last_name (str): The last name of the account holder.
            age (int): The age of the account holder.
            state (str): The state where the account holder resides.
            job (str): The job title of the account holder.
            account_type (str): The type of account (Checking or Savings).
            initial_balance (float): The initial balance for the account.

        Returns:
            str: The ID of the created account.
        """
        account = Account(first_name, last_name, age, state, job, account_type, initial_balance)
        self.accounts[account.account_id] = account
        self.export_accounts_to_csv()
        print(f"Account created for {first_name} {last_name}. Account ID: {account.account_id}")
        return account.account_id

    def delete_account(self, account_id: str):
        """
        Delete an account by ID.

        Args:
            account_id (str): The ID of the account to delete.

        Raises:
            ValueError: If the account ID is not found.
        """
        if account_id not in self.accounts:
            raise ValueError("Account not found.")
        del self.accounts[account_id]
        self.export_accounts_to_csv()
        print(f"Account {account_id} has been deleted.")

    def get_account(self, account_id: str) -> Account:
        """
        Retrieve an account by ID.

        Args:
            account_id (str): The ID of the account.

        Raises:
            ValueError: If the account ID is not found.
        """
        if account_id not in self.accounts:
            raise ValueError("Account not found.")
        return self.accounts[account_id]

    def update_account_info(self):
        """Update account holder's information."""
        account_id = input("Enter account ID: ")
        try:
            account = self.get_account(account_id)
            print("What would you like to change?")
            print("1. First Name")
            print("2. Last Name")
            print("3. Age")
            print("4. State")
            choice = input("Choose an option (1/2/3/4): ")

            if choice == "1":
                new_first_name = input("Enter new first name: ")
                account.update_info(first_name=new_first_name)
            elif choice == "2":
                new_last_name = input("Enter new last name: ")
                account.update_info(last_name=new_last_name)
            elif choice == "3":
                try:
                    new_age = int(input("Enter new age: "))
                    account.update_info(age=new_age)
                except ValueError:
                    print("Invalid input. Age must be a number.")
                    return
            elif choice == "4":
                new_state = input("Enter new state: ")
                account.update_info(state=new_state)
            else:
                print("Invalid option. Please try again.")
                return
            
            print("Account information updated successfully.")
        except ValueError as e:
            print(e)

        self.export_accounts_to_csv()

    def list_accounts(self):
        """List all accounts in the bank."""
        if not self.accounts:
            print("No accounts in the bank.")
        for account_id, account in self.accounts.items():
            print(f"ID: {account_id} | Name: {account.first_name} {account.last_name} | Age: {account.age} | State: {account.state} | Job: {account.job} | Type: {account.account_type} | Balance: ${account.balance:.2f}")

    def export_accounts_to_csv(self):
        """Export all account data to a CSV file."""
        with open("accounts.csv", "w", newline="") as csvfile:
            fieldnames = ["account_id", "first_name", "last_name", "age", "state", "job", "account_type", "balance"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for account in self.accounts.values():
                writer.writerow({
                    "account_id": account.account_id,
                    "first_name": account.first_name,
                    "last_name": account.last_name,
                    "age": account.age,
                    "state": account.state,
                    "job": account.job,
                    "account_type": account.account_type,
                    "balance": account.balance,
                })

