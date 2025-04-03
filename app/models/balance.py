from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.user import User
    from models.transaction import Transaction, TransactionType

@dataclass
class Balance:
    """
    Класс для управления балансом пользователя.

    Attributes:
        user (User): Владелец баланса
        amount (float): Текущий баланс
    """

    user: "User"
    amount: float = 0.0

    def deposit(self, amount: float) -> None:
        """Пополнение баланса"""
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self.amount += amount
        self.user.transaction_history.add_transaction(
            Transaction(
                id=len(self.user.transaction_history.transactions) + 1,
                amount=amount,
                type=TransactionType.DEPOSIT,
            )
        )

    def withdraw(self, amount: float) -> None:
        """Списание средств"""
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if self.amount < amount:
            raise ValueError("Insufficient funds")
        self.amount -= amount
        self.user.transaction_history.add_transaction(
            Transaction(
                id=len(self.user.transaction_history.transactions) + 1,
                amount=-amount,
                type=TransactionType.WITHDRAWAL,
            )
        )