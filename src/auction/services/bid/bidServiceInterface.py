from abc import ABC, abstractmethod

class IBidService(ABC):
    @abstractmethod
    def create(self, ownerId, lotId, price):
        pass

    @abstractmethod
    def update(self, bidId, price):
        pass

    @abstractmethod
    def delete(self, bidId):
        pass
    
    @abstractmethod
    def getById(self, bidId):
        pass
    
    @abstractmethod
    def getAll(self):
        pass