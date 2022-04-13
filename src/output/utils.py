from src.output.outputfactory import OutputFactory
from src.utils import auxiliar


def pipe_to_another_output(params: dict, events: list) -> bool:
    if params is not None and "needs_pipe" in params \
            and auxiliar.convert_to_boolean(params["needs_pipe"]) \
            and "output" in params:
        pipe = OutputFactory.get_output_by_dict(params)
        pipe.dump_list(events)
        return True
    return False
