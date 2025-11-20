from abc import ABC, abstractmethod


class Forecaster(ABC):
    def __init__(self, data, hyperParams):
        self.data = data
        self.meta_data = hyperParams

    @abstractmethod
    def Generate_Forecasts(self):
        pass

    @abstractmethod
    def Save_Forecasts(self):
        pass