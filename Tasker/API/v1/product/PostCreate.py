from Tasker.API.v1 import AbstractView


class APIV1ProductPostCreate(AbstractView):
    def dispatch_request(self, **kwargs):
        return True