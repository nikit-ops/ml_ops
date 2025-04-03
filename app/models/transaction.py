from dataclasses import dataclass, field
from typing import List
from enum import Enum


class TransactionType(Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    PREDICTION_PAYMENT = "prediction_payment"


@dataclass
class Transaction:
    """
    Класс финансовой транзакции.

    Attributes:
        id (int): Уникальный идентификатор
        amount (float): Сумма операции
        type (TransactionType): Тип операции
        description (str): Описание операции
    """

    id: int
    amount: float
    type: TransactionType
    description: str = ""


@dataclass
class TransactionHistory:
    """История финансовых операций пользователя"""

    transactions: List[Transaction] = field(default_factory=list)

    def add_transaction(self, transaction: Transaction) -> None:
        """Добавляет новую транзакцию"""
        self.transactions.append(transaction)