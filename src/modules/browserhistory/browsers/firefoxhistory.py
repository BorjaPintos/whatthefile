import traceback
from typing import List

from src.modules.browserhistory.browsers.ibrowserhistory import IBrowserHistory
from src.modules.browserhistory.domain.dowloand import Download
from src.modules.browserhistory.domain.search import Search
from src.modules.browserhistory.domain.visite import Visite
from src.utils import sqlite


class FirefoxHistory(IBrowserHistory):

    VISITQUERYv1 = """
    select 
    mp.title, 
    mp.url, 
    mp.visit_count, 
    mh.visit_date/1000000 as visit_time,
    mp.last_visit_date/1000000 as last_visit_time, 
    mp2.url,
    mp2.title
    from moz_historyvisits mh left join moz_places mp on mh.place_id == mp.id
    left join moz_historyvisits mh2 on mh.from_visit == mh2.id 
    left join moz_places mp2 on mh2.place_id == mp2.id
    """

    DOWNLOADSQUERYv1 = """
    select 
    mp.url, 
    ma.content, 
    ma.dateAdded /1000000 as end_time
    from moz_annos ma join moz_places mp on ma.place_id == mp.id 
    where anno_attribute_id in (1, 3);"""

    SEARCHQUERYv1 = """
    select 
    mk.keyword, 
    mp.url,
    mp.title
    from moz_keywords mk left join moz_places mp on mk.place_id == mp.id;"""

    SEARCHQUERYv2 = """
    select 
    mk.keyword 
    from moz_keywords;"""

    def __init__(self, path: str):
        super().__init__()
        self.browser = "Firefox"
        self._path = path

    def _get_downloadsv1(self) -> List:

        returned_list = []
        for row in sqlite.execute_query(self._path, self.DOWNLOADSQUERYv1):
            download = Download(path=self._path, browser=self.browser,
                                site_url=row[0], target_path=str(row[1]).replace("file://", ""),
                                end_time=row[2])
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

    def _get_searchsv2(self) -> List:
        returned_list = []
        for row in sqlite.execute_query(self._path, self.SEARCHQUERYv2):
            search = Search(path=self._path, browser=self.browser,
                            term=row[0])
            returned_list.append(search.__dict__)
        return returned_list

    def get_searchs(self) -> List:
        try:
            return self._get_searchsv1()
        except:
            pass
        try:
            return self._get_searchsv2()
        except:
            pass
        return []
