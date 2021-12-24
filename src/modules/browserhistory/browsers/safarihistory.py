import traceback
from typing import List

from src.modules.browserhistory.browsers.ibrowserhistory import IBrowserHistory
from src.modules.browserhistory.domain.visite import Visite
from src.utils import sqlite


class SafaryHistory(IBrowserHistory):
    VISITQUERYv1 = """
    select 
    hv.title, 
    hi.url, 
    hi.visit_count, 
    hv.visit_time + (strftime('%s', '2001-01-01T00:00:00')), 
    hi2.url,
    hv2.title
    from history_visits hv left join history_items hi on hv.history_item == hi.id
    left join history_visits hv2 on hv.redirect_source == hv2.id
    left join history_items hi2 on hv2.history_item == hi2.id
    """

    def __init__(self, path: str):
        self._path = path

    def get_downloads(self) -> List:
        return []

    def _get_visitesv1(self) -> List:
        returned_list = []
        for row in sqlite.execute_query(self._path, self.VISITQUERYv1):
            visite = Visite(path=self._path,
                            title=row[0], url=row[1], visit_count=row[2],
                            visit_time=row[3],
                            from_url=row[4], from_title=row[5])
            returned_list.append(visite.__dict__)
        return returned_list


    def get_visites(self) -> List:
        try:
            return self._get_visitesv1()
        except:
            traceback.print_exc()
            pass
        return []


    def get_searchs(self) -> List:

        return []


