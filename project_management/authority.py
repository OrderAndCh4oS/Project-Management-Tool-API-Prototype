def get_the_authority(user):
    try:
        return user.staff.authority.get_uuid()
    except:
        return None


def has_access(request, object):
    try:
        return request.session.get('authority') == object.authority.get_uuid()
    except:
        return False
