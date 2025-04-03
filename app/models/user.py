from dataclasses import dataclass, field
from typing import List, TYPE_CHECKING
import re
import bcrypt


if TYPE_CHECKING:
    from models.balance import Balance
    from models.transaction import TransactionHistory
    from models.prediction import PredictionHistory, AnimalPrediction

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
