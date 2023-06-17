from abc import ABC, abstractmethod

class IAuctionService(ABC):
    @abstractmethod
    def create(self, title, startTime, endTime):
        pass

    @abstractmethod
    def update(self, auctionId, title=None, startTime=None, endTime=None):
        pass

    @abstractmethod
    def close(self, auctionId):
        pass
    
    @abstractmethod
    def close(self, auctionId):
        pass
    
    @abstractmethod
    def get(self, auctionId):
        pass
    
    @abstractmethod
    def search(self, query):
        pass