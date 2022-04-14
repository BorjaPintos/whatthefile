from abc import abstractmethod
from typing import List


class IBrowserHistory:

    def __init__(self):
        self.browser = ""

    def get_browser_name(self) -> str:
        return self.browser

    @abstractmethod
    def get_searchs(self) -> List:
        pass

    @abstractmethod
    def get_visites(self) -> List:
        pass

    @abstractmethod
    def get_downloads(self) -> List:
        pass