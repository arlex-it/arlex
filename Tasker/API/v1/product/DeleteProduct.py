from Tasker.API.v1 import AbstractView


class APIV1ProductDeleteProduct(AbstractView):
    def dispatch_request(self, **kwargs):
        return True