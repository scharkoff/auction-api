from abc import ABC, abstractmethod

class IUsersService(ABC):
    @abstractmethod
    def getAll():
        pass
    
    @abstractmethod
    def getById():
        pass
    
    @abstractmethod
    def create():
        pass
    
    @abstractmethod
    def update():
        pass
    
    @abstractmethod
    def delete():
        pass

