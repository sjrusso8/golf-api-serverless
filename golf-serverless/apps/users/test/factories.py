from typing import Optional

from apps.users.models import User

def create_app_user(
    email: str,
    password: str = 'secretpassword123',
) -> User: 
    user = User.create_user(
        email=email,
        password=password
    )
    return user