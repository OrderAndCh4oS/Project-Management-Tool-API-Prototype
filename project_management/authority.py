from rest_framework import serializers


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


def hyperlinkedRelatedFieldByAuthority(model, view_name, authority, many=True):
    return serializers.HyperlinkedRelatedField(
        many=many,
        view_name=view_name,
        queryset=model.objects.filter(authority=authority)
    )


def slugRelatedFieldByAuthority(model, slug, authority):
    return serializers.SlugRelatedField(
        slug_field=slug,
        queryset=model.objects.filter(authority=authority)
    )
