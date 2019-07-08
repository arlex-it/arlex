from Tasker.API.v1 import AbstractView


class APIV1ProductPutInfo(AbstractView):
    def dispatch_request(self, **kwargs):
        return True