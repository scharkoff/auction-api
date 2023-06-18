from abc import ABC, abstractmethod

class IUsersController(ABC):
    @abstractmethod
    def getAll(request):
        pass
    
    @abstractmethod
    def getById(request):
        pass
    
    @abstractmethod
    def create(request):
        pass
    
    @abstractmethod
    def update(request):
        pass
    
    @abstractmethod
    def delete(request):
        pass
