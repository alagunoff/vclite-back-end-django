def check_if_requester_authenticated(requester) -> bool:
    return requester and requester.is_authenticated


def check_if_requester_admin(requester) -> bool:
    return check_if_requester_authenticated(requester) and requester.is_staff
