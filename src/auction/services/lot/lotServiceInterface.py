from abc import ABC, abstractmethod

class ILotService(ABC):
    @abstractmethod
    def create(self, ownerId, auctionId, startTime, endTime, title, description, image):
        pass

    @abstractmethod
    def update(self, lotId, startTime, endTime, title, description, image):
        pass

    @abstractmethod
    def delete(self, lotId):
        pass
    
    @abstractmethod
    def getById(self, lotId):
        pass
    
    @abstractmethod
    def getAll(self):
        pass