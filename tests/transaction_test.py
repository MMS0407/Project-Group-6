import unittest
from banking_system_components.transaction import Transaction


class TestTransaction(unittest.TestCase):
    def test_transaction_initialization(self):
        """Test that a Transaction object initializes correctly."""
        transaction = Transaction(transaction_type="Deposit", amount=150.0)
        self.assertEqual(transaction.transaction_type, "Deposit")
        self.assertEqual(transaction.amount, 150.0)
        self.assertIsNone(transaction.target_account)
        self.assertTrue(isinstance(transaction.transaction_id, str))
        self.assertEqual(len(transaction.transaction_id),
                         32)  # UUID hex is 32 chars long

    def test_transaction_initialization_with_target_account(self):
        """Test initializing with a target account."""
        transaction = Transaction(
            transaction_type="Transfer In", amount=200.0, target_account='123abc')
        self.assertEqual(transaction.transaction_type, "Transfer In")
        self.assertEqual(transaction.amount, 200.0)
        self.assertEqual(transaction.target_account, '123abc')

    def test_to_dict(self):
        """Test the to_dict method for accurate dictionary representation."""
        transaction = Transaction(transaction_type="Withdrawal", amount=100.0)
        transaction_dict = transaction.to_dict()
        expected_dict = {
            "type": "Withdrawal",
            "amount": 100.0,
            "target_account": None,
            "transaction_id": transaction.transaction_id
        }
        self.assertEqual(transaction_dict, expected_dict)


if __name__ == '__main__':
    unittest.main()
