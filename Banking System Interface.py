import uuid
from typing import List, Dict, Optional


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
        self.timestamp = uuid.uuid4().hex  # Unique transaction ID

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
            "timestamp": self.timestamp,
        }


class Account:
    """Represents a bank account with balance and transaction history."""

    def __init__(self, name: str, account_type: str = "Checking", initial_balance: float = 0.0):
        """
        Initialize a bank account.

        Args:
            name (str): The name of the account holder.
            account_type (str): The type of account (Checking or Savings).
            initial_balance (float): The initial account balance (default: 0.0).
        """
        if account_type not in ["Checking", "Savings"]:
            raise ValueError("Invalid account type. Must be 'Checking' or 'Savings'.")
        self.account_id = str(uuid.uuid4())
        self.name = name
        self.account_type = account_type
        self.balance = initial_balance
        self.transactions: List[Transaction] = []

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

    def calculate_interest(self, annual_rate: float, months: int = 1):
        """
        Calculate interest for savings accounts.

        Args:
            annual_rate (float): The annual interest rate (e.g., 0.05 for 5%).
            months (int): The number of months for which to calculate interest.

        Raises:
            ValueError: If the account type is not 'Savings' or invalid interest rate.
        """
        if self.account_type != "Savings":
            raise ValueError("Interest calculation is only applicable to savings accounts.")
        if annual_rate <= 0 or months <= 0:
            raise ValueError("Interest rate and duration must be positive values.")
        monthly_rate = annual_rate / 12
        interest = self.balance * monthly_rate * months
        self.deposit(interest)
        print(f"Interest of ${interest:.2f} added to account {self.account_id}.")

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


class Bank:
    """Represents a bank with multiple accounts."""

    def __init__(self):
        """Initialize the bank with an empty account database."""
        self.accounts: Dict[str, Account] = {}

    def create_account(self, name: str, account_type: str = "Checking", initial_balance: float = 0.0) -> str:
        """
        Create a new account.

        Args:
            name (str): The name of the account holder.
            account_type (str): The type of account (Checking or Savings).
            initial_balance (float): The initial balance for the account.

        Returns:
            str: The ID of the created account.
        """
        account = Account(name, account_type, initial_balance)
        self.accounts[account.account_id] = account
        print(f"Account created for {name}. Account ID: {account.account_id}")
        return account.account_id

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

    def list_accounts(self):
        """List all accounts in the bank."""
        if not self.accounts:
            print("No accounts in the bank.")
        for account_id, account in self.accounts.items():
            print(f"ID: {account_id} | Name: {account.name} | Type: {account.account_type} | Balance: ${account.balance:.2f}")


class BankCLI:
    """CLI for the banking system."""

    def __init__(self):
        """Initialize the CLI with a Bank instance."""
        self.bank = Bank()

    def menu(self):
        """Display the banking system menu and handle user input."""
        while True:
            print("\nBanking System Menu:")
            print("1. Create Account")
            print("2. Deposit Money")
            print("3. Withdraw Money")
            print("4. Transfer Money")
            print("5. View Transaction History")
            print("6. Filter Transactions by Type")
            print("7. Calculate Interest (Savings Accounts)")
            print("8. List All Accounts")
            print("9. Exit")
            choice = input("Choose an option: ")

            if choice == "1":
                self.create_account()
            elif choice == "2":
                self.deposit_money()
            elif choice == "3":
                self.withdraw_money()
            elif choice == "4":
                self.transfer_money()
            elif choice == "5":
                self.view_transaction_history()
            elif choice == "6":
                self.filter_transactions()
            elif choice == "7":
                self.calculate_interest()
            elif choice == "8":
                self.bank.list_accounts()
            elif choice == "9":
                print("Exiting the banking system. Goodbye!")
                break
            else:
                print("Invalid option. Please try again.")

    def create_account(self):
        """Handle account creation."""
        name = input("Enter account holder's name: ")
        account_type = input("Enter account type (Checking/Savings): ")
        try:
            initial_balance = float(input("Enter initial balance: "))
        except ValueError:
            print("Invalid input. Initial balance must be a number.")
            return
        self.bank.create_account(name, account_type, initial_balance)

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

    def calculate_interest(self):
        """Calculate interest for a savings account."""
        account_id = input("Enter account ID: ")
        try:
            annual_rate = float(input("Enter annual interest rate (e.g., 0.05 for 5%): "))
            months = int(input("Enter number of months: "))
            account = self.bank.get_account(account_id)
            account.calculate_interest(annual_rate, months)
        except ValueError as e:
            print(e)


if __name__ == "__main__":
    cli = BankCLI()
    cli.menu()
