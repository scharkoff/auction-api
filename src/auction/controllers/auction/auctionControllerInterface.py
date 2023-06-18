from abc import ABC, abstractmethod

class IAuctionController(ABC):
    @abstractmethod
    def create(request):
        pass

    @abstractmethod
    def update(request):
        pass

    @abstractmethod
    def close(request):
        pass
    
    @abstractmethod
    def close(request):
        pass
    
    @abstractmethod
    def getById(request):
        pass
    
    @abstractmethod
    def search(request):
        pass