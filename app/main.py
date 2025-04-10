from database.config import get_settings
from database.database import get_session, init_db, engine
from services.crud.user import get_all_users, create_user
from services.crud.balance import (
    get_balance_by_user_id,
    deposit,
    withdraw,
)
from services.crud.transaction import get_transaction_history_by_user_id
from services.crud.mltask import create_task_for_user_with_prediction
from sqlmodel import Session
from models.user import User
from models.balance import Balance
from models.mlmodel import MlModel


if __name__ == "__main__":

    init_db()
    print("Init db has been success")

    with Session(engine) as session:
        try:
            test_user = User(email="test@mail.ru", password="password123")
            test_user_2 = User(email="test@mail2.ru", password="password123")
            test_user_3 = User(email="admin@mail.ru", password="adminpassword", is_admin=True)

            create_user(test_user, session)
            create_user(test_user_2, session)
            create_user(test_user_3, session)
        except Exception as e:
            print(f"User operation failed: {e}")

        try:
            test_user = User(email="test4324r23@mail.ru", password="123")
            create_user(test_user, session)
        except Exception as e:
            print(f"User operation (bad_password) failed: {e}")

        users = get_all_users(session)
        for user in users:
            print(f"id: {user.id} - {user.email}")

    with Session(engine) as session:
        try:
            balance = get_balance_by_user_id(session, user_id=3)
            print(f"Initial balance: ID={balance.id}, Amount={balance.amount}")

            updated_balance = deposit(session, balance_id=balance.id, amount=70.0)
            print(
                f"Deposited funds: ID={updated_balance.id}, Amount={updated_balance.amount}"
            )

            current_balance = get_balance_by_user_id(session, user_id=3)
            print(
                f"Current balance after deposit: ID={current_balance.id}, Amount={current_balance.amount}"
            )

            updated_balance = withdraw(session, balance_id=balance.id, amount=30.0)
            print(
                f"Withdrew funds: ID={updated_balance.id}, Amount={updated_balance.amount}"
            )

            current_balance = get_balance_by_user_id(session, user_id=3)
            print(
                f"Current balance after withdrawal: ID={current_balance.id}, Amount={current_balance.amount}"
            )

        except Exception as e:
            print(f"Balance operation failed: {e}")

    with Session(engine) as session:
        try:
            transaction_history = get_transaction_history_by_user_id(session, user_id=3)
            print("Transaction History:")
            for transaction in transaction_history:
                print(
                    f"Transaction ID: {transaction.id}, Type: {transaction.type}, Amount: {transaction.amount}, Timestamp: {transaction.timestamp}"
                )
        except Exception as e:
            print(f"Transaction history retrieval failed: {e}")

    with Session(engine) as session:
        for i in range(5):
            try:
                model = MlModel(description="Cat-Dog Classifier")
                session.add(model)
                session.commit()
                session.refresh(model)
            
                user_id = 3
                image_path = "/path/to/image.jpg"
                cost = 10.0
                task = create_task_for_user_with_prediction(session, user_id, image_path, cost, model)
                print(f"Task created: ID={task.id}, Status={task.status}, Prediction={task.result}")
            except Exception as e:
                print(f"Task or prediction operation failed: {e}")
