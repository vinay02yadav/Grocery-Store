from functools import wraps
from app.models import Login
from flask_jwt_extended import get_jwt_identity, jwt_required

def role_required(allowed_roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            identity = get_jwt_identity()
            user = Login.query.filter_by(email=identity).first()

            if user and (isinstance(allowed_roles, list) and user.role in allowed_roles) or (isinstance(allowed_roles, str) and user.role == allowed_roles):
                return func(*args, **kwargs)
            else:
                return False

        return wrapper

    return decorator
