from sqlmodel import SQLModel, Session, create_engine
from contextlib import contextmanager
from .config import get_settings
from models.user import User
from models.mlmodel import MlModel
from services.crud.user import create_user
from services.crud.balance import get_balance_by_user_id, deposit, withdraw
from services.crud.mltask import create_task_for_user_with_prediction

settings = get_settings()

engine = create_engine(url=settings.DATABASE_URL_psycopg, echo=settings.IS_DEBUG)


def get_session():
    with Session(engine) as session:
        yield session


def init_db():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        try:
            test_user = User(email="test@mail.test", password="password123")
            test_user_2 = User(email="test2@mail.test", password="password123")
            create_user(test_user, session)
            create_user(test_user_2, session)

            # Deposit sufficient funds into user balances
            balance_user_1 = get_balance_by_user_id(session, user_id=test_user.id)
            deposit(session, balance_id=balance_user_1.id, amount=100.0)

            balance_user_2 = get_balance_by_user_id(session, user_id=test_user_2.id)
            deposit(session, balance_id=balance_user_2.id, amount=100.0)

            withdraw(session, balance_id=balance_user_1.id, amount=30.0)

            model = MlModel(description="Cat-Dog Classifier")
            session.add(model)
            session.commit()
            session.refresh(model)

            image_path = "/path/to/image.jpg"
            cost = 10.0
            create_task_for_user_with_prediction(
                session,
                user_id=test_user.id,
                image_path=image_path,
                cost=cost,
                model=model,
            )
            create_task_for_user_with_prediction(
                session,
                user_id=test_user_2.id,
                image_path=image_path,
                cost=cost,
                model=model,
            )

        except Exception as e:
            print(f"Database population failed: {e}")
