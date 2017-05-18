from functools import wraps

from flask_socketio import send

from application import active_users, message_history


def auth_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        active_user = active_users.get_current()
        if active_user:
            return fn(*args, **kwargs)
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


def fields_required(field_names):
    def wrapper_factory(fn):
        @wraps(fn)
        def wrapper(json, *args, **kwargs):
            missed_fields = [field_name for field_name in field_names
                             if field_name not in json]
            if missed_fields:
                send(f"Missed required fields: {missed_fields}")
                return
            else:
                kwargs.update({field_name: json[field_name]
                               for field_name in field_names})
            return fn(*args, **kwargs)
        return wrapper
    return wrapper_factory
