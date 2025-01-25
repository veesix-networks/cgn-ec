from abc import ABC, abstractmethod


class BaseOutput(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def process_metrics(self, metrics):
        raise NotImplementedError("process_event not implemented")
