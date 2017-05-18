from functools import wraps

from application import active_users, message_history


def auth_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        active_user = active_users.get_current_user()
        if active_user:
            return fn(active_user, *args, **kwargs)
    return wrapper


def save_to_history(fn):
    @wraps(fn)
    def wrapper(message, to_user=None):
        if to_user:
            message_history.add_private(message, to_user.username)
            return fn(message, to_user)
        else:
            message_history.add_global(message)
            return fn(message)
    return wrapper
