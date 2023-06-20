from abc import ABC, abstractmethod

class ILotService(ABC):
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