from src.utils.time import Time

class Download:

    def __init__(self, **kwargs):
        self.type = "Download"
        self.path = kwargs.get("path")
        self.browser = kwargs.get("browser")
        self.site_url = kwargs.get("site_url", None)
        self.tab_url = kwargs.get("tab_url", None)
        self.target_path = kwargs.get("target_path", None)
        self.start_time = Time.change_output_date_format_from_epoch(kwargs.get("start_time", None))
        self.end_time = Time.change_output_date_format_from_epoch(kwargs.get("end_time", None))
        self.mime_type = kwargs.get("mime_type", None)
        self.received_bytes = kwargs.get("received_bytes", None)
        self.total_bytes = kwargs.get("total_bytes", None)
        self.timestamp = self.end_time

