# -*- coding:utf-8 -*-
from functools import wraps
from flask import abort
from flask_login import current_user, login_required
from putidms.models.user import Permission


def permission_required(permission):
    def decorate(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)

        return decorated_function

    return decorate


def admin_required(f):
    return permission_required(Permission.ADMIN)(f)
