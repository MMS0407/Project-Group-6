import unittest
from unittest.mock import call, mock_open, patch

from banking_system_components.account import Account

class TestAccount(unittest.TestCase):

    def setUp(self):
        """Set up test environment for each test method."""
        self.account = Account(
            "John", "Doe", 30, "California", "Employed", "Checking", 500.0)

    def test_account_initialization(self):
        """Test account initialization."""
        self.assertEqual(self.account.first_name, "John")
        self.assertEqual(self.account.last_name, "Doe")
        self.assertEqual(self.account.age, 30)
        self.assertEqual(self.account.state, "California")
        self.assertEqual(self.account.job, "Employed")
        self.assertEqual(self.account.account_type, "Checking")
        self.assertEqual(self.account.balance, 500.0)

    def test_deposit(self):
        """Test deposit functionality."""
        self.account.deposit(500.0)
        self.assertEqual(self.account.balance, 1000.0)

    def test_deposit_negative_amount(self):
        """Test deposit with negative amount raises error."""
        with self.assertRaises(ValueError):
            self.account.deposit(-100.0)

    def test_withdraw(self):
        """Test withdrawal functionality."""
        self.account.withdraw(200.0)
        self.assertEqual(self.account.balance, 300.0)

    def test_withdraw_insufficient_funds(self):
        """Test withdrawal more than balance raises error."""
        with self.assertRaises(ValueError):
            self.account.withdraw(600.0)

    def test_withdraw_negative_amount(self):
        """Test withdrawal of negative amount raises error."""
        with self.assertRaises(ValueError):
            self.account.withdraw(-100.0)

    def test_transfer_funds(self):
        """Test transferring funds between accounts."""
        target_account = Account(
            "Jane", "Doe", 28, "Nevada", "Unemployed", "Savings", 300.0)
        self.account.transfer(target_account, 200.0)
        self.assertEqual(self.account.balance, 300.0)
        self.assertEqual(target_account.balance, 500.0)

    def test_transfer_insufficient_funds(self):
        """Test transfer more than balance raises error."""
        target_account = Account(
            "Jane", "Doe", 28, "Nevada", "Unemployed", "Savings", 300.0)
        with self.assertRaises(ValueError):
            self.account.transfer(target_account, 600.0)

    def test_filter_transactions(self):
        """Test filtering transactions by type."""
        self.account.deposit(200.0)
        self.account.withdraw(100.0)
        deposits = self.account.filter_transactions("Deposit")
        self.assertEqual(len(deposits), 1)
        self.assertEqual(deposits[0].amount, 200.0)

    @patch('builtins.open', new_callable=mock_open)
    def test_export_balance_update(self, mock_file):
        """Test exporting balance updates after a deposit."""
        self.account.deposit(200.0)

        # Validate that open was called correctly during the export
        mock_file.assert_called_with("accounts.csv", "w", newline='')

        # Get the mock file handle and inspect what was written
        handle = mock_file()
        calls = handle.write.call_args_list

        # Check that the header and account update lines are written correctly
        header_call = call(
            "account_id,first_name,last_name,age,state,job,account_type,balance\r\n")
        self.assertIn(header_call, calls,
                      "The CSV header was not written correctly.")

        expected_balance_update_call = call(
            f"{self.account.account_id},{self.account.first_name},{self.account.last_name},{self.account.age},{self.account.state},{self.account.job},{self.account.account_type},{self.account.balance:.2f}\r\n")
        self.assertIn(expected_balance_update_call, calls,
                      "The account balance update was not written correctly.")

    def test_get_details(self):
        """Test getting account details."""
        details = self.account.get_details()
        expected_details = (
            f"Account ID: {self.account.account_id}\n"
            f"Account Holder: {self.account.first_name} {self.account.last_name}\n"
            f"Age: {self.account.age}\n"
            f"State: {self.account.state}\n"
            f"Job: {self.account.job}\n"
            f"Account Type: {self.account.account_type}\n"
            f"Balance: ${self.account.balance:.2f}"
        )
        self.assertEqual(details, expected_details)

    def test_zzz_delete_csv(self):
        """ Cleaning up the CSV file after all tests are run. As unittest runs tests in alphabetical order, the function is named that way to ensure it runs last."""
        self.account.delete_balance_csv()
        with self.assertRaises(FileNotFoundError):
            with open("accounts.csv", "r"):
                pass


if __name__ == '__main__':
    unittest.main()
