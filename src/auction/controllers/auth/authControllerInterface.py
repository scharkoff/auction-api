from abc import ABC, abstractmethod

class IAuthController(ABC):
    @abstractmethod
    def register(self, request):
        pass

    @abstractmethod
    def login(self, request):
        pass

    @abstractmethod
    def logout(self, request):
        pass