from abc import abstractmethod
from typing import List


class IBrowserHistory:

    @abstractmethod
    def get_searchs(self) -> List:
        pass

    @abstractmethod
    def get_visites(self) -> List:
        pass

    @abstractmethod
    def get_downloads(self) -> List:
        pass