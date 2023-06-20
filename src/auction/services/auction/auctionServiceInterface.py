from abc import ABC, abstractmethod

class IAuctionService(ABC):
    @abstractmethod
    def create(self, title, startTime, endTime):
        pass

    @abstractmethod
    def update(self, auctionId, title, startTime, endTime):
        pass

    @abstractmethod
    def close(self, auctionId):
        pass
    
    @abstractmethod
    def close(self, auctionId):
        pass
    
    @abstractmethod
    def getById(self, auctionId):
        pass
    
    @abstractmethod
    def search(self, query):
        pass