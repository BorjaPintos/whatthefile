from src.utils.time import Time


class Visite:

    def __init__(self, **kwargs):
        self.type = "Visit"
        self.path = kwargs.get("path")
        self.browser = kwargs.get("browser")
        self.title = kwargs.get("title", None)
        self.url = kwargs.get("url", None)
        self.visit_count = kwargs.get("visit_count", None)
        self.visit_time = Time.change_output_date_format_from_epoch(kwargs.get("visit_time", None))
        self.last_visit_time = Time.change_output_date_format_from_epoch(kwargs.get("last_visit_time", None))
        self.from_url = kwargs.get("from_url", None)
        self.from_title = kwargs.get("from_title", None)
        self.timestamp = self.visit_time

