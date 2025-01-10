from rich.console import Console

from banking_system_components.bank import Bank


class BankCLI:
    """CLI for the banking system."""

    def __init__(self) -> None:
        """Initialize the CLI with a Bank instance."""
        self.bank = Bank()
        self.bank.load_initial_accounts()
        self.console = Console()

    def menu(self) -> None:
        """Display the banking system menu and handle user input."""
        while True:
            self.console.print("\n[bold blue]Banking System Menu:[/bold blue]")

            self.console.print(
                "\n[bold green]Banking Transactions:[/bold green]")
            self.console.print("[bold green]1.[/bold green] Deposit Money")
            self.console.print("[bold green]2.[/bold green] Withdraw Money")
            self.console.print("[bold green]3.[/bold green] Transfer Money")
            self.console.print(
                "[bold green]4.[/bold green] View Transaction History")
            self.console.print(
                "[bold green]5.[/bold green] Filter Transactions by Type")

            self.console.print("\n[#e72a77]Account Operations:[/#e72a77]")
            self.console.print("[#e72a77]6.[/#e72a77] Create Account")
            self.console.print("[#e72a77]7.[/#e72a77] Delete Account")
            self.console.print("[#e72a77]8.[/#e72a77] View Account Details")
            self.console.print(
                "[#e72a77]9.[/#e72a77] Update Account Information")
            self.console.print(
                "[#e72a77]10.[/#e72a77] Export Transaction History")
            self.console.print("[#e72a77]11.[/#e72a77] List All Accounts")

            self.console.print("\n[bold red]12. Exit[/bold red]")

            choice = input("\n Choose an option (From 1 to 12): ")

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

    def create_account(self) -> None:
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
        self.bank.create_account(
            first_name, last_name, age, state, job, account_type, initial_balance)

    def delete_account(self) -> None:
        """Handle account deletion."""
        account_id = input("Enter account ID to delete: ")
        try:
            self.bank.delete_account(account_id)
        except ValueError as e:
            print(e)

    def deposit_money(self) -> None:
        """Handle money deposit."""
        account_id = input("Enter account ID: ")
        try:
            amount = float(input("Enter deposit amount: "))
            account = self.bank.get_account(account_id)
            account.deposit(amount)
            print(f"Deposited ${amount:.2f} into account {
                  account_id}. New balance: ${account.balance:.2f}")
        except ValueError as e:
            print(e)

    def withdraw_money(self) -> None:
        """Handle money withdrawal."""
        account_id = input("Enter account ID: ")
        try:
            amount = float(input("Enter withdrawal amount: "))
            account = self.bank.get_account(account_id)
            account.withdraw(amount)
            print(f"Withdrew ${amount:.2f} from account {account_id}. New balance: ${account.balance:.2f}")  # noqa
        except ValueError as e:
            print(e)

    def transfer_money(self) -> None:
        """Handle money transfer."""
        from_account_id = input("Enter your account ID: ")
        to_account_id = input("Enter the target account ID: ")
        try:
            amount = float(input("Enter transfer amount: "))
            from_account = self.bank.get_account(from_account_id)
            to_account = self.bank.get_account(to_account_id)
            from_account.transfer(to_account, amount)
            print(f"Transferred ${amount:.2f} from account {from_account_id} to {to_account_id}.")  # noqa
        except ValueError as e:
            print(e)

    def view_transaction_history(self) -> None:
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

    def filter_transactions(self) -> None:
        """Filter transactions by type."""
        account_id = input("Enter account ID: ")
        transaction_type = input(
            "Enter transaction type (Deposit, Withdrawal, Transfer In, Transfer Out): ")
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

    def export_transaction_history(self) -> None:
        """Export transaction history to a file."""
        account_id = input("Enter account ID: ")
        try:
            account = self.bank.get_account(account_id)
            transactions = account.get_transaction_history()
            if not transactions:
                print("No transactions to export.")
                return
            filename = input(
                "Enter filename to export to (e.g., transactions.csv): ")
            with open(filename, "w") as file:
                for transaction in transactions:
                    file.write(f"{transaction}\n")
            print(f"Transaction history exported to {filename}.")
        except ValueError as e:
            print(e)

    def view_account_details(self) -> None:
        """View details of an account."""
        account_id = input("Enter account ID: ")
        try:
            account = self.bank.get_account(account_id)
            print(f"Account Details for {account_id}:")
            print(account.get_details())
        except ValueError as e:
            print(e)
