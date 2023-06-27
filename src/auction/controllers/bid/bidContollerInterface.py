from abc import ABC, abstractmethod

class IBidController(ABC):
    @abstractmethod
    def create(request):
        pass

    @abstractmethod
    def update(request):
        pass

    @abstractmethod
    def delete(request):
        pass
    
    @abstractmethod
    def getById(request):
        pass
    
    @abstractmethod
    def getAll(request):
        pass

    @abstractmethod
    def getUserBidByLotId(request):
        pass