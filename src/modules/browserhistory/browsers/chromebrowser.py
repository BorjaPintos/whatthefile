import sqlite3
import traceback
from typing import List

from src.modules.browserhistory.domain.dowloand import Download
from src.modules.browserhistory.domain.search import Search
from src.modules.browserhistory.domain.visite import Visite

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

DOWNLOADSQUERYv2 = """
select d.url,
d.full_path, 
d.start_time / 1000000 + (strftime('%s', '1601-01-01T00:00:00')) as start_time,
d.received_bytes,
d.total_bytes 
from downloads d;"""

SEARCHQUERYv1 = """select kst.term, u.url, u.title, 
u.last_visit_time / 1000000 + (strftime('%s', '1601-01-01T00:00:00')) as last_visit_time  
from keyword_search_terms kst left join urls u on kst.url_id == u.id;"""


def _execute_query(path, query: str):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def _get_downloadsv1(path: str) -> List:

    returned_list = []
    for row in _execute_query(path, DOWNLOADSQUERYv1):
        download = Download(path=path,
                            site_url=row[0], tab_url=row[1], target_path=row[2],
                            start_time=row[3], end_time=row[4],
                            mime_type=row[5], received_bytes=row[6], total_bytes=row[7])
        returned_list.append(download.__dict__)
    return returned_list

def _get_downloadsv2(path: str) -> List:

    returned_list = []
    for row in _execute_query(path, DOWNLOADSQUERYv2):
        download = Download(path=path,
                            site_url=row[0], target_path=row[1],
                            start_time=row[2],  received_bytes=row[3], total_bytes=row[4])
        returned_list.append(download.__dict__)
    return returned_list

def get_downloads(path: str) -> List:
    try:
        return _get_downloadsv1(path)
    except:
        pass
    try:
        return _get_downloadsv2(path)
    except:
        pass
    return []



def _get_visitesv1(path) -> List:
    returned_list = []
    for row in _execute_query(path, VISITQUERYv1):
        visite = Visite(path=path,
                        title=row[0], url=row[1], visit_count=row[2],
                        visit_time=row[3], last_visit_time=row[4],
                        from_url=row[5], from_title=row[6])
        returned_list.append(visite.__dict__)
    return returned_list


def get_visites(path: str) -> List:
    try:
        return _get_visitesv1(path)
    except:
        traceback.print_exc()
        pass
    return []


def get_searchsv1(path) -> List:
    returned_list = []
    for row in _execute_query(path, SEARCHQUERYv1):
        search = Search(path=path,
                        term=row[0], url=row[1], title=row[2],
                        last_visit_time=row[3])
        returned_list.append(search.__dict__)
    return returned_list

def get_searchs(path: str) -> List:
    try:
        return get_searchsv1(path)
    except:
        pass
    return []


