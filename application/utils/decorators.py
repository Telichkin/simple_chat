from functools import wraps

from flask_socketio import send

from application.chat_users import active_users


def auth_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        active_user = active_users.get_current()
        if active_user:
            return fn(*args, **kwargs)
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
