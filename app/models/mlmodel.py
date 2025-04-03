
import os
from enum import Enum
import random
from abc import ABC, abstractmethod

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
