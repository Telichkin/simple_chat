from functools import wraps

from application import active_users


def auth_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        active_user = active_users.get_current_user()
        if active_user:
            return fn(active_user, *args, **kwargs)
    return wrapper