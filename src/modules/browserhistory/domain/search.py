from src.utils.time import Time


class Search:

    def __init__(self, **kwargs):
        self.path = kwargs.get("path")
        self.browser = kwargs.get("browser")
        self.term = kwargs.get("term", None)
        self.url = kwargs.get("url", None)
        self.title = kwargs.get("title", None)