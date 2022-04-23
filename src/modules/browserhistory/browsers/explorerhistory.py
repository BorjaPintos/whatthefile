import traceback
from datetime import datetime, timedelta
from typing import List
import pyesedb
from src.modules.browserhistory.browsers.ibrowserhistory import IBrowserHistory
from src.modules.browserhistory.domain.dowloand import Download
from src.modules.browserhistory.domain.visite import Visite
import re


class IExplorerHistory(IBrowserHistory):


    def __init__(self, path: str):
        super().__init__()
        self.browser = "IExplorer"
        self._path = path


    def _get_downloadsv1(self) -> List:
        returned_list = []
        return returned_list


    def get_downloads(self) -> List:
        try:
            return self._get_downloadsv1()
        except:
            pass
        return []

    def _get_visitesv1(self) -> List:
        returned_list = []
        with open(self._path, "rb") as file_object:
            try:
                esedb_file = pyesedb.file()
                esedb_file.open_file_object(file_object)
                try:
                    containers_table = esedb_file.get_table_by_name("Containers")
                    containers_list = []
                    for i in range(0, containers_table.get_number_of_records() - 1):
                        container_record = containers_table.get_record(i)
                        container_id = container_record.get_value_data_as_integer(0)
                        containers_list.append(container_id)

                    for container_id in containers_list:
                        container_table = esedb_file.get_table_by_name("Container_" + str(container_id))
                        for i in range(0, container_table.get_number_of_records() - 1):
                            try:
                                record = container_table.get_record(i)
                                type = record.get_value_data_as_integer(6)
                                if type == 2097153:
                                    visited_time = self.convert_timestamp(record.get_value_data_as_integer(13))
                                    visit_count = record.get_value_data_as_integer(8)
                                    visited_url= record.get_value_data_as_string(17)
                                    url = "http" + re.split("Visited: .*@http", visited_url)[1]
                                    visite = Visite(path=self._path, browser=self.browser,
                                        url=url, visit_count=visit_count,
                                        visit_time=visited_time)
                                    returned_list.append(visite.__dict__)
                            except Exception:
                                pass

                except Exception:
                    pass
                finally:
                    esedb_file.close()
            except Exception:
                pass
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


    @staticmethod
    def convert_timestamp(timestamp):
        epoch_start = datetime(year=1601, month=1,day=1)
        seconds_since_epoch = timestamp/10**7
        timestamp = epoch_start + timedelta(seconds=seconds_since_epoch)
        return timestamp.timestamp()