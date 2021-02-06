from transfer.models import UserAgent


class UserAgentMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        current_user_agent = request.headers['User-Agent']
        user_agent_obj, created = UserAgent.objects.get_or_create(user=request.user)
        user_agent_obj.user_agent = current_user_agent
        user_agent_obj.save()
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response