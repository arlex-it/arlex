from Tasker.API.v1 import AbstractView


class APIV1ProductGetInfo(AbstractView):
    def dispatch_request(self, **kwargs):
        return True