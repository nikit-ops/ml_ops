from dataclasses import dataclass, field
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from models.user import User
    from models.mlmodel import AnimalType
    from models.mltask import MLTask

@dataclass
class PredictionHistory:
    """История предсказаний пользователя"""

    user: "User"
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
    task: "MLTask"