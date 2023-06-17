from abc import ABC, abstractmethod

class IAuthService(ABC):
    @abstractmethod
    def register(self, username, password, email):
        pass

    @abstractmethod
    def login(self, request, username, password):
        pass

    @abstractmethod
    def logout(self, request):
        pass
