import uuid
import csv
from typing import List, Dict, Optional
import random
from rich.console import Console

class Transaction:
    """Represents a transaction in a banking account."""

    def __init__(self, transaction_type: str, amount: float, target_account: Optional[str] = None):
        """
        Initialize a transaction.
                                                                 
        Args:
            transaction_type (str): The type of transaction (e.g., Deposit, Withdrawal, Transfer In).
            amount (float): The transaction amount.
            target_account (Optional[str]): The ID of the target account for transfers (default: None).
        """
        self.transaction_type = transaction_type
        self.amount = amount
        self.target_account = target_account
        self.transaction_id = uuid.uuid4().hex  # Unique transaction ID

    def to_dict(self) -> Dict:
        """
        Convert the transaction to a dictionary format.

        Returns:
            dict: A dictionary representing the transaction.
        """
        return {
            "type": self.transaction_type,
            "amount": self.amount,
            "target_account": self.target_account,
            "transaction_id": self.transaction_id,
        }


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


class BankCLI:
    """CLI for the banking system."""

    def __init__(self):
        """Initialize the CLI with a Bank instance."""
        self.bank = Bank()
        self.console = Console()

    def menu(self):
        """Display the banking system menu and handle user input."""
        while True:
            self.console.print("\n[bold blue]Banking System Menu:[/bold blue]")
            
            # Grouping Banking Transactions
            self.console.print("\n[bold green]Banking Transactions:[/bold green]")
            self.console.print("[bold green]1.[/bold green] Deposit Money")
            self.console.print("[bold green]2.[/bold green] Withdraw Money")
            self.console.print("[bold green]3.[/bold green] Transfer Money")
            self.console.print("[bold green]4.[/bold green] View Transaction History")
            self.console.print("[bold green]5.[/bold green] Filter Transactions by Type")
            
            # Grouping Account Operations
            self.console.print("\n[#e72a77]Account Operations:[/#e72a77]")
            self.console.print("[#e72a77]6.[/#e72a77] Create Account")
            self.console.print("[#e72a77]7.[/#e72a77] Delete Account")
            self.console.print("[#e72a77]8.[/#e72a77] View Account Details")
            self.console.print("[#e72a77]9.[/#e72a77] Update Account Information")
            self.console.print("[#e72a77]10.[/#e72a77] Export Transaction History")
            self.console.print("[#e72a77]11.[/#e72a77] List All Accounts")
            
            # Exit Option
            self.console.print("\n[bold red]12. Exit[/bold red]")
            
            choice = input("\n Choose an option (From 1 to 12): ")

            # Handling user choices (same logic as before)
            if choice == "1":
                self.deposit_money()
            elif choice == "2":
                self.withdraw_money()
            elif choice == "3":
                self.transfer_money()
            elif choice == "4":
                self.view_transaction_history()
            elif choice == "5":
                self.filter_transactions()
            elif choice == "6":
                self.create_account()
            elif choice == "7":
                self.delete_account()
            elif choice == "8":
                self.view_account_details()
            elif choice == "9":
                self.bank.update_account_info()
            elif choice == "10":
                self.export_transaction_history()
            elif choice == "11":
                self.bank.list_accounts()
            elif choice == "12":
                print("Exiting the banking system. Goodbye!")
                break
            else:
                print("Invalid option. Please try again.")

    def create_account(self):
        """Handle account creation."""
        first_name = input("Enter account holder's first name: ")
        last_name = input("Enter account holder's last name: ")
        try:
            age = int(input("Enter account holder's age: "))
        except ValueError:
            print("Invalid input. Age must be a number.")
            return
        state = input("Enter account holder's state: ")
        job = input("Enter account holder's job: ")
        account_type = input("Enter account type (Checking/Savings): ")
        try:
            initial_balance = float(input("Enter initial balance: "))
        except ValueError:
            print("Invalid input. Initial balance must be a number.")
            return
        self.bank.create_account(first_name, last_name, age, state, job, account_type, initial_balance)

    def delete_account(self):
        """Handle account deletion."""
        account_id = input("Enter account ID to delete: ")
        try:
            self.bank.delete_account(account_id)
        except ValueError as e:
            print(e)

    def deposit_money(self):
        """Handle money deposit."""
        account_id = input("Enter account ID: ")
        try:
            amount = float(input("Enter deposit amount: "))
            account = self.bank.get_account(account_id)
            account.deposit(amount)
            print(f"Deposited ${amount:.2f} into account {account_id}. New balance: ${account.balance:.2f}")
        except ValueError as e:
            print(e)

    def withdraw_money(self):
        """Handle money withdrawal."""
        account_id = input("Enter account ID: ")
        try:
            amount = float(input("Enter withdrawal amount: "))
            account = self.bank.get_account(account_id)
            account.withdraw(amount)
            print(f"Withdrew ${amount:.2f} from account {account_id}. New balance: ${account.balance:.2f}")
        except ValueError as e:
            print(e)

    def transfer_money(self):
        """Handle money transfer."""
        from_account_id = input("Enter your account ID: ")
        to_account_id = input("Enter the target account ID: ")
        try:
            amount = float(input("Enter transfer amount: "))
            from_account = self.bank.get_account(from_account_id)
            to_account = self.bank.get_account(to_account_id)
            from_account.transfer(to_account, amount)
            print(f"Transferred ${amount:.2f} from account {from_account_id} to {to_account_id}.")
        except ValueError as e:
            print(e)

    def view_transaction_history(self):
        """View transaction history for an account."""
        account_id = input("Enter account ID: ")
        try:
            account = self.bank.get_account(account_id)
            transactions = account.get_transaction_history()
            if not transactions:
                print("No transactions found.")
                return
            print("Transaction History:")
            for transaction in transactions:
                print(transaction)
        except ValueError as e:
            print(e)

    def filter_transactions(self):
        """Filter transactions by type."""
        account_id = input("Enter account ID: ")
        transaction_type = input("Enter transaction type (Deposit, Withdrawal, Transfer In, Transfer Out): ")
        try:
            account = self.bank.get_account(account_id)
            filtered = account.filter_transactions(transaction_type)
            if not filtered:
                print(f"No transactions of type '{transaction_type}' found.")
                return
            print(f"Filtered Transactions ({transaction_type}):")
            for transaction in filtered:
                print(transaction.to_dict())
        except ValueError as e:
            print(e)

    def export_transaction_history(self):
        """Export transaction history to a file."""
        account_id = input("Enter account ID: ")
        try:
            account = self.bank.get_account(account_id)
            transactions = account.get_transaction_history()
            if not transactions:
                print("No transactions to export.")
                return
            filename = input("Enter filename to export to (e.g., transactions.csv): ")
            with open(filename, "w") as file:
                for transaction in transactions:
                    file.write(f"{transaction}\n") 
            print(f"Transaction history exported to {filename}.")
        except ValueError as e:
            print(e)

    def view_account_details(self):
        """View details of an account."""
        account_id = input("Enter account ID: ")
        try:
            account = self.bank.get_account(account_id)
            print(f"Account Details for {account_id}:")
            print(account.get_details()) 
        except ValueError as e:
            print(e)

if __name__ == "__main__":
    cli = BankCLI()
    cli.menu()
