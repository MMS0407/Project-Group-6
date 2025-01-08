import uuid
from typing import Dict, Optional

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
