from abc import ABC, abstractmethod


class Mail(ABC):
    @abstractmethod
    def get_code_by_many_tries(self):
        pass
