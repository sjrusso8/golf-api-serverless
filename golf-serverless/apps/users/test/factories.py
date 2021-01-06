from typing import Optional

from apps.users.models import User

def create_app_user(
    email: str,
    password: str = 'secretpassword123',
    first_name: Optional[str] = 'John',
    last_name: Optional[str] = 'Doe',
    is_staff: Optional[str] = False,
    is_superuser: Optional[str] = False
) -> User: 
    user = User.objects._create_user(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        is_staff=is_staff,
        is_superuser=is_superuser
    )
    return user