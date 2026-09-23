from .models import staff


def generate_staff_username():

    last_staff = staff.objects.order_by("-id").first()

    if last_staff is None:

        return "SM0001"

    last_number = int(last_staff.username[2:])

    next_number = last_number + 1

    return f"SM{next_number:04d}"