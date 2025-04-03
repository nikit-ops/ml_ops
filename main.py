from dataclasses import dataclass, field
from typing import List, Optional
import re
import os
from enum import Enum
import random
import bcrypt
from abc import ABC, abstractmethod


@dataclass
class User:
    """
    Класс для представления пользователя в системе.

    Attributes:
        id (int): Уникальный идентификатор пользователя
        email (str): Email пользователя
        password (str): Хэшированный пароль пользователя
        animal_predictions (List[animal_predictions]): Список предсказаний пользователя
        cat_count (int): Количество кошек
        dog_count (int): Количество собак
    """

    id: int
    email: str
    password: str
    animal_predictions: List["AnimalPrediction"] = field(default_factory=list)
    balance: "Balance" = field(init=False)
    transaction_history: "TransactionHistory" = field(init=False)
    prediction_history: "PredictionHistory" = field(init=False)

    def __post_init__(self) -> None:
        self._validate_email()
        if self._validate_password():
            self.password = bcrypt.hashpw(
                self.password.encode("utf-8"), bcrypt.gensalt()
            )
        self.balance = Balance(user=self)
        self.transaction_history = TransactionHistory()
        self.prediction_history = PredictionHistory(user=self)

    def _validate_email(self) -> None:
        """Проверяет корректность email."""
        email_pattern = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
        if not email_pattern.match(self.email):
            raise ValueError("Invalid email format")

    def _validate_password(self) -> None:
        """Проверяет минимальную длину пароля."""
        if len(self.password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        else:
            return True

    def check_password(self, password: str) -> bool:
        """Проверяет соответствие пароля хэшу."""
        return bcrypt.checkpw(password.encode("utf-8"), self.password)

    def add_animal(self, animal_prediction: "AnimalPrediction") -> None:
        """Добавляет событие в список событий пользователя."""
        self.animal_predictions.append(animal_prediction)

    def get_animal_stats(self) -> dict:
        """Возвращает статистику по животным."""
        return {
            "user_id": self.id,
            "cats": self.cat_count,
            "dogs": self.dog_count,
            "total_animals": self.cat_count + self.dog_count,
        }


class Model(ABC):
    """Абстрактный базовый класс для моделей ML"""

    @abstractmethod
    def predict(self, image_path: str):
        pass

    def _validate_image(self) -> None:
        """Проверяет формат изображения"""
        valid_extensions = [".jpg", ".jpeg"]
        _, ext = os.path.splitext(self.image)
        if ext.lower() not in valid_extensions:
            raise ValueError("Image must be in JPG format")


class AnimalType(Enum):
    CAT = "cat"
    DOG = "dog"
    UNKNOWN = "unknown"


class CatDogModel(Model):
    """ML модель для классификации кошек и собак"""

    def predict(self, image_path: str) -> AnimalType:
        # Для примера возвращаем случайный результат

        chance = random.random()
        if chance > 0.90:
            return AnimalType.UNKNOWN
        elif chance > 0.45:
            return AnimalType.DOG
        else:
            return AnimalType.CAT


@dataclass
class Balance:
    """
    Класс для управления балансом пользователя.

    Attributes:
        user (User): Владелец баланса
        amount (float): Текущий баланс
    """

    user: User
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


@dataclass
class PredictionHistory:
    """История предсказаний пользователя"""

    user: User
    predictions: List["AnimalPrediction"] = field(default_factory=list)

    def add_prediction(self, prediction: "AnimalPrediction") -> None:
        """Добавляет новое предсказание"""
        self.predictions.append(prediction)

    def get_stats(self) -> dict:
        """Возвращает статистику предсказаний"""
        stats = {"cats": 0, "dogs": 0, "unknown": 0, "total": len(self.predictions)}
        for prediction in self.predictions:
            if prediction.animal_type == AnimalType.CAT:
                stats["cats"] += 1
            elif prediction.animal_type == AnimalType.DOG:
                stats["dogs"] += 1
            else:
                stats["unknown"] += 1
        return stats


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
    user: User
    model: Model
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


@dataclass
class AnimalPrediction:
    """
    Класс результата предсказания.

    Attributes:
        id (int): Уникальный идентификатор
        image (str): Путь к изображению
        animal_type (AnimalType): Результат предсказания
        task (MLTask): Связанная задача
    """

    id: int
    image: str
    animal_type: AnimalType
    task: MLTask


def main() -> None:
    try:
        user = User(id=1, email="test@mail.ru", password="secure_password123")
        print(f"Created user: {user}\n")

        print("Check password: ", user.check_password("secure_password123"), "\n")

        print(f"Balance: {user.balance.amount}\n")
        print('Add balance...')
        user.balance.deposit(150.0)
        print(f"Balance: {user.balance.amount}\n")

        for i in range(1, 11):
            task = MLTask(
                id=i,
                image_path=f"pets/pet_{i}.jpg",
                user=user,
                model=CatDogModel(),
            )

            try:
                task.process()
                print(f"Prediction #{i} completed: {task.result.value}")
            except Exception as e:
                print(f"Prediction #{i} failed: {str(e)}")

        print("\nUser Stats:")
        print(f"Balance: {user.balance.amount}\n")
        print("Prediction History:", user.prediction_history.get_stats())

    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
