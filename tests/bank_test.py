import unittest
from unittest.mock import mock_open, patch

from banking_system_components.bank import Bank

class TestBank(unittest.TestCase):

    def setUp(self):
        self.bank = Bank()

    def test_create_account(self):
        account_id = self.bank.create_account(
            "John", "Doe", 30, "California", "Employed", "Checking", 500.0)
        self.assertIn(account_id, self.bank.accounts)
        account = self.bank.accounts[account_id]
        self.assertEqual(account.first_name, "John")
        self.assertEqual(account.last_name, "Doe")
        self.assertEqual(account.age, 30)
        self.assertEqual(account.state, "California")
        self.assertEqual(account.job, "Employed")
        self.assertEqual(account.account_type, "Checking")
        self.assertEqual(account.balance, 500.0)

    def test_delete_account(self):
        account_id = self.bank.create_account(
            "Jane", "Doe", 25, "New York", "Unemployed", "Savings", 1000.0)
        self.bank.delete_account(account_id)
        self.assertNotIn(account_id, self.bank.accounts)

    def test_get_account(self):
        account_id = self.bank.create_account(
            "Alice", "Smith", 40, "Texas", "Employed", "Checking", 2000.0)
        account = self.bank.get_account(account_id)
        self.assertEqual(account.first_name, "Alice")
        self.assertEqual(account.last_name, "Smith")
        self.assertEqual(account.age, 40)
        self.assertEqual(account.state, "Texas")
        self.assertEqual(account.job, "Employed")
        self.assertEqual(account.account_type, "Checking")
        self.assertEqual(account.balance, 2000.0)

    def test_update_account_info(self):
        account_id = self.bank.create_account(
            "Bob", "Brown", 50, "Florida", "Employed", "Savings", 3000.0)
        account = self.bank.get_account(account_id)
        account.update_info(first_name="Robert",
                            last_name="Brownie", age=55, state="Georgia")
        updated_account = self.bank.get_account(account_id)
        self.assertEqual(updated_account.first_name, "Robert")
        self.assertEqual(updated_account.last_name, "Brownie")
        self.assertEqual(updated_account.age, 55)
        self.assertEqual(updated_account.state, "Georgia")

    def test_delete_nonexistent_account(self):
        with self.assertRaises(ValueError):
            self.bank.delete_account("nonexistent_id")

    def test_get_nonexistent_account(self):
        with self.assertRaises(ValueError):
            self.bank.get_account("nonexistent_id")

    def test_list_accounts(self):
        self.bank.create_account("Charlie", "Johnson",
                                 60, "Nevada", "Retired", "Checking", 4000.0)
        self.bank.create_account(
            "Diana", "Williams", 35, "Ohio", "Employed", "Savings", 1500.0)
        self.assertEqual(len(self.bank.accounts), 2)

    @patch('builtins.open', new_callable=mock_open)
    def test_export_accounts_to_csv(self, mock_file):
        self.bank.create_account(
            "Eve", "Davis", 45, "Washington", "Employed", "Checking", 2500.0)
        self.bank.export_accounts_to_csv()
        mock_file.assert_called_with("accounts.csv", "w", newline='')
        handle = mock_file()
        handle.write.assert_called()
        rows = handle.write.call_args_list
        self.assertIn('Eve', str(rows))
        self.assertIn('Davis', str(rows))
        self.assertIn('45', str(rows))

    def test_load_initial_accounts(self):
        with patch('banking_system_components.bank.Bank.create_account') as mocked_create_account:
            self.bank.load_initial_accounts()
            self.assertEqual(mocked_create_account.call_count, 20)

    def test_zzz_delete_csv(self):
        """ Cleaning up the CSV file after all tests are run. As unittest runs tests in alphabetical order, the function is named that way to ensure it runs last."""
        self.bank.delete_account_csv()
        with self.assertRaises(FileNotFoundError):
            with open("accounts.csv", "r"):
                pass


if __name__ == '__main__':
    unittest.main()
