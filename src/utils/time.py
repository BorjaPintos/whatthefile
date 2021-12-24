from src.domain.whatthefileconfiguration import WhatTheFileConfiguration

from datetime import datetime

class Time:

    _output_format = "epoch"

    @staticmethod
    def configure(conf: WhatTheFileConfiguration):
        try:
            Time._output_format = conf.get_property("whatthefile", "output_date_format")
        except:
            pass
            "using default value"


    @staticmethod
    def change_output_date_format_from_epoch(epoch : float):
        if epoch is None:
            return None
        try:
            if Time._output_format == "epoch_ms":
                return int(epoch*100)
            if Time._output_format == "epoch":
                return epoch
            else:
                timestamp = datetime.fromtimestamp(epoch)
                return timestamp.strftime(Time._output_format)
        except:
            return epoch

    @staticmethod
    def get_utc_timestamp() -> float:
        return datetime.utcnow().timestamp()