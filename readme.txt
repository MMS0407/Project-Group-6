This project implements a Banking System with features like account creation, transactions, and detailed reporting. 
The application is written in Python and includes a Command-Line Interface (CLI) for user interaction. 
The system uses a CSV file for data storage of accounts and transaction histories.

Files in the Project
	•	account.py: Defines the `Account` class for managing bank accounts, including attributes like holder details, 
        balance, and transactions, with methods for deposits, withdrawals, transfers, updates, and exporting data to CSV.
    •	bank.py: Defines the `Bank` class, which manages multiple accounts with methods for creating, deleting, retrieving, updating, 
        listing, and exporting account data, while also initializing sample accounts on startup.
    •	command_line_interface.py: Defines the `BankCLI` class, providing a command-line interface for interacting with the banking system, 
        including options for account and transaction management, exporting data, and displaying account details.
    •	accounts.csv: CSV file for persistent storage of account data.

CSV Integration
The application uses accounts.csv to store account data persistently:
	•	Each row represents an account with fields like account ID, holder name, age, state, job, account type, and balance.
	•	Data is automatically updated when accounts are created, deleted, or modified.

Menu Options
Banking Transactions
	1.	Deposit Money: Add funds to an account.
	2.	Withdraw Money: Deduct funds from an account.
	3.	Transfer Money: Transfer funds to another account.
	4.	View Transaction History: Display all transactions of an account.
	5.	Filter Transactions: Show transactions by type.
Account Operations
	6.	Create Account: Add a new account to the system.
	7.	Delete Account: Remove an account permanently.
	8.	View Account Details: Show detailed information about an account.
	9.	Update Account Information: Modify account holder details.
	10.	Export Transaction History: Save transaction logs to a CSV file.
	11.	List All Accounts: Display all accounts in the bank.
Exit
	12.	Exit: Quit the application.
