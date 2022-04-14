import traceback
from typing import List

from src.modules.browserhistory.browsers.ibrowserhistory import IBrowserHistory
from src.modules.browserhistory.domain.dowloand import Download
from src.modules.browserhistory.domain.search import Search
from src.modules.browserhistory.domain.visite import Visite
from src.utils import sqlite


class EdgeHistory(IBrowserHistory):

    VISITQUERYv1 = """
    select 
    u.title, 
    u.url, 
    u.visit_count, 
    v.visit_time / 1000000 + (strftime('%s', '1601-01-01T00:00:00')) as visit_time, 
    u.last_visit_time / 1000000 + (strftime('%s', '1601-01-01T00:00:00')) as last_visit_time, 
    u2.url,
    u2.title
    from visits v left join urls u on v.url == u.id 
    left join visits v2 on v.from_visit == v2.id 
    left join urls u2 on v2.url == u2.id;
    """

    DOWNLOADSQUERYv1 = """
    select d.site_url, d.tab_url,
    d.target_path, 
    d.start_time / 1000000 + (strftime('%s', '1601-01-01T00:00:00')) as start_time,
    d.end_time / 1000000 + (strftime('%s', '1601-01-01T00:00:00')) as end_time,
    d.mime_type,
    d.received_bytes,
    d.total_bytes 
    from downloads d;"""

    SEARCHQUERYv1 = """select kst.term, u.url, u.title, 
    u.last_visit_time / 1000000 + (strftime('%s', '1601-01-01T00:00:00')) as last_visit_time  
    from keyword_search_terms kst left join urls u on kst.url_id == u.id;"""

    def __init__(self, path: str):
        super().__init__()
        self.browser = "Edge"
        self._path = path


    def _get_downloadsv1(self) -> List:

        returned_list = []
        for row in sqlite.execute_query(self._path, self.DOWNLOADSQUERYv1):
            download = Download(path=self._path, browser=self.browser,
                                site_url=row[0], tab_url=row[1], target_path=row[2],
                                start_time=row[3], end_time=row[4],
                                mime_type=row[5], received_bytes=row[6], total_bytes=row[7])
            returned_list.append(download.__dict__)
        return returned_list

    def get_downloads(self) -> List:
        try:
            return self._get_downloadsv1()
        except:
            pass
        return []

    def _get_visitesv1(self) -> List:
        returned_list = []
        for row in sqlite.execute_query(self._path, self.VISITQUERYv1):
            visite = Visite(path=self._path, browser=self.browser,
                            title=row[0], url=row[1], visit_count=row[2],
                            visit_time=row[3], last_visit_time=row[4],
                            from_url=row[5], from_title=row[6])
            returned_list.append(visite.__dict__)
        return returned_list

    def get_visites(self) -> List:
        try:
            return self._get_visitesv1()
        except:
            traceback.print_exc()
            pass
        return []

    def _get_searchsv1(self) -> List:
        returned_list = []
        for row in sqlite.execute_query(self._path, self.SEARCHQUERYv1):
            search = Search(path=self._path, browser=self.browser,
                            term=row[0], url=row[1], title=row[2])
            returned_list.append(search.__dict__)
        return returned_list

    def get_searchs(self) -> List:
        try:
            return self._get_searchsv1()
        except:
            pass
        return []
