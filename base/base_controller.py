from abc import ABC, abstractmethod
from base.base_view import BaseView


class BaseController(ABC):
    @abstractmethod
    def __init__(self, view: BaseView):
        self.view = view
