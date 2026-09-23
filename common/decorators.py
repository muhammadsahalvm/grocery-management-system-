from functools import wraps
from django.shortcuts import redirect


def owner_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if "owner_id" not in request.session:

            return redirect("owner_login")

        return view_func(request, *args, **kwargs)

    return wrapper


def staff_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if "staff_id" not in request.session:

            return redirect("staff_login")

        return view_func(request, *args, **kwargs)

    return wrapper