from src.utils.time import Time


class Search:

    def __init__(self, **kwargs):
        self.path = kwargs.get("path")
        self.term = kwargs.get("term", None)
        self.url = kwargs.get("url", None)
        self.title = kwargs.get("title", None)
        self.last_visit_time = Time.change_output_date_format_from_epoch(kwargs.get("last_visit_time", None))