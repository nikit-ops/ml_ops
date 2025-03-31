from dataclasses import dataclass, field
from typing import List
import re
import os
from enum import Enum
import random


@dataclass
class User:
    """
    Класс для представления пользователя в системе.

    Attributes:
        id (int): Уникальный идентификатор пользователя
        email (str): Email пользователя
        password (str): Пароль пользователя
        animal_predictions (List[animal_predictions]): Список предсказаний пользователя
        cat_count (int): Количество кошек
        dog_count (int): Количество собак
    """

    id: int
    email: str
    password: str
    animal_predictions: List["AnimalPrediction"] = field(default_factory=list)
    cat_count: int = 0
    dog_count: int = 0

    def __post_init__(self) -> None:
        self._validate_email()
        self._validate_password()

    def _validate_email(self) -> None:
        """Проверяет корректность email."""
        email_pattern = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
        if not email_pattern.match(self.email):
            raise ValueError("Invalid email format")

    def _validate_password(self) -> None:
        """Проверяет минимальную длину пароля."""
        if len(self.password) < 8:
            raise ValueError("Password must be at least 8 characters long")

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


class AnimalType(Enum):
    CAT = "cat"
    DOG = "dog"
    UNKNOWN = "unknown"


@dataclass
class AnimalPrediction:
    """
    Класс для представления определения животного.

    Attributes:
        id (int): Уникальный идентификатор события
        image (str): Путь к изображению
        creator (User): Создатель события
        animal_type (AnimalType): Определенный моделью тип животного
    """

    id: int
    image: str
    creator: User
    animal_type: AnimalType = field(init=False)

    def __post_init__(self):
        self._validate_image()
        self._detect_animal_type()

    def _validate_image(self) -> None:
        """Проверяет формат изображения"""
        valid_extensions = [".jpg", ".jpeg"]
        _, ext = os.path.splitext(self.image)
        if ext.lower() not in valid_extensions:
            raise ValueError("Image must be in JPG format")

    def _detect_animal_type(self) -> None:
        model = CatDogModel()
        self.animal_type = model.predict(self.image)
        if self.animal_type == AnimalType.CAT:
            self.creator.cat_count += 1
        elif self.animal_type == AnimalType.DOG:
            self.creator.dog_count += 1


class CatDogModel:
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


def main() -> None:
    try:
        user = User(id=1, email="test@mail.ru", password="secure_password123")

        for i in range(1, 11):
            pet = AnimalPrediction(id=i, image=f"my_animals/pet_{i}.jpg", creator=user)
            user.add_animal(pet)

        print(f"Created user: {user}")
        print(user.get_animal_stats())

    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
