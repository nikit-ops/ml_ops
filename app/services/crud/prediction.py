from models.mlmodel import MlModel
from models.mltask import AnimalType
import random

def get_prediction_from_model(model: MlModel, image_path: str) -> AnimalType:
    """Use a prediction model to generate a prediction for an image."""
    # print(f"Using model '{model.description}' to predict for image: {image_path}")
    return random.choice([AnimalType.CAT, AnimalType.DOG, AnimalType.UNKNOWN])
