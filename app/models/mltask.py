from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING
from enum import Enum

if TYPE_CHECKING:
    from models.user import User
    from models.prediction import AnimalPrediction
    from models.mlmodel import Model, AnimalType
    from models.transaction import Transaction, TransactionType


class MLTaskStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class MLTask:
    """
    Класс задачи машинного обучения.

    Attributes:
        id (int): Уникальный идентификатор
        image_path (str): Путь к изображению
        user (User): Инициатор задачи
        model (Model): Используемая модель
        cost (float): Стоимость предсказания
        status (MLTaskStatus): Статус выполнения
        result (Optional[AnimalType]: Результат предсказания
    """

    id: int
    image_path: str
    user: "User"
    model: "Model"
    cost: float = 10.0
    status: MLTaskStatus = MLTaskStatus.PENDING
    result: Optional[AnimalType] = None

    def process(self) -> None:
        """Выполняет предсказание и обновляет статус"""
        try:
            # Проверяем баланс
            if self.user.balance.amount < self.cost:
                raise ValueError("Insufficient funds to process prediction")

            # Выполняем предсказание
            self.result = self.model.predict(self.image_path)

            # Списание средств
            self.user.balance.withdraw(self.cost)

            # Создаем запись о предсказании
            prediction = AnimalPrediction(
                id=self.id, image=self.image_path, animal_type=self.result, task=self
            )
            self.user.prediction_history.add_prediction(prediction)

            # Обновляем статус
            self.status = MLTaskStatus.COMPLETED

            # Добавляем транзакцию
            self.user.transaction_history.add_transaction(
                Transaction(
                    id=len(self.user.transaction_history.transactions) + 1,
                    amount=-self.cost,
                    type=TransactionType.PREDICTION_PAYMENT,
                    description=f"Prediction #{self.id}",
                )
            )

        except Exception as e:
            self.status = MLTaskStatus.FAILED
            raise e
