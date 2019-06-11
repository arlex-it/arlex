from flask.views import View

class AbstractView(View):
    """
    Abstract view.
    """

    @classmethod
    def view(cls):
        """
        Return the specific class view, with the correct name
        """
        return cls.as_view(cls.__name__)
