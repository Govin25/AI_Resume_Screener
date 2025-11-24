from uuid import uuid4
from models.user import User

token_json = {"user_id": str(uuid4())}
    
# Mock `get_all_users` to return a predefined list of users
mock_users = [
    User(user_id=uuid4(), full_name="Govind", email="govind@gmail.com"),
    User(user_id=uuid4(), full_name="Narendra", email="Narendra@gmail.com"),
    User(user_id=uuid4(), full_name="Ravi", email="Ravi@gmail.com"),
    User(user_id=uuid4(), full_name="rahul", email="rahul@gmail.com")
]