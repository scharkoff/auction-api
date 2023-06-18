from abc import ABC, abstractmethod

class IAuthController(ABC):
    @abstractmethod
    def register(request):
        pass

    @abstractmethod
    def login(request):
        pass

    @abstractmethod
    def logout(request):
        pass