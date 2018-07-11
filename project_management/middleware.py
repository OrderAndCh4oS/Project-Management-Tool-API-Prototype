from project_management.authority import get_the_authority


class UserAuthorities:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.session.get('authority'):
            request.session['authority'] = get_the_authority(request.user)

        response = self.get_response(request)

        return response
