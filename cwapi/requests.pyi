from abc import abstractmethod
from typing import final, NoReturn

from cwapi.types import Operation


class request:
    @abstractmethod
    def dump(self) -> bytes: ...


@final
class CreateAuthCodeRequest(request):
    @property
    def userId(self) -> int: ...

    @userId.setter
    def userId(self, value: int) -> NoReturn: ...

    def __new__(cls, userId: int) -> CreateAuthCodeRequest: ...

    def dump(self) -> bytes: ...


@final
class GrantTokenRequest(request):
    @property
    def userId(self) -> int: ...

    @userId.setter
    def userId(self, value: int) -> NoReturn: ...

    @property
    def authCode(self) -> str: ...

    @authCode.setter
    def authCode(self, value: str) -> NoReturn: ...

    def __new__(cls, userId: int, authCode: str) -> GrantTokenRequest: ...

    def dump(self) -> bytes: ...


@final
class AuthAdditionalOperationRequest(request):
    @property
    def token(self) -> str: ...

    @token.setter
    def token(self, value) -> NoReturn: ...

    @property
    def operation(self) -> Operation: ...

    @operation.setter
    def operation(self, value: str) -> NoReturn: ...

    @property
    def authCode(self) -> str: ...

    @authCode.setter
    def authCode(self, value: str) -> NoReturn: ...

    def __new__(cls, token: str, operation: Operation) -> AuthAdditionalOperationRequest: ...

    def dump(self) -> bytes: ...


@final
class GrantAdditionalOperationRequest(request):
    @property
    def token(self) -> str: ...

    @token.setter
    def token(self, value) -> NoReturn: ...

    @property
    def requestId(self) -> str: ...

    @requestId.setter
    def requestId(self, value: str) -> NoReturn: ...

    @property
    def authCode(self) -> str: ...

    @authCode.setter
    def authCode(self, value: str) -> NoReturn: ...

    def __new__(cls, token: str, requestId: str, authCode: str) -> GrantAdditionalOperationRequest: ...

    def dump(self) -> bytes: ...


@final
class GetInfoRequest(request):
    def __new__(cls) -> GetInfoRequest: ...

    def dump(self) -> bytes: ...


@final
class ViewCraftbookRequest(request):
    @property
    def token(self) -> str: ...

    @token.setter
    def token(self, value) -> NoReturn: ...

    def __new__(cls, token: str) -> ViewCraftbookRequest: ...

    def dump(self) -> bytes: ...


@final
class RequestProfileRequest(request):
    @property
    def token(self) -> str: ...

    @token.setter
    def token(self, value) -> NoReturn: ...

    def __new__(cls, token: str) -> RequestProfileRequest: ...

    def dump(self) -> bytes: ...


@final
class RequestBasicInfoRequest(request):
    @property
    def token(self) -> str: ...

    @token.setter
    def token(self, value) -> NoReturn: ...

    def __new__(cls, token: str) -> RequestBasicInfoRequest: ...

    def dump(self) -> bytes: ...


@final
class RequestGearInfoRequest(request):
    @property
    def token(self) -> str: ...

    @token.setter
    def token(self, value) -> NoReturn: ...

    def __new__(cls, token: str) -> RequestGearInfoRequest: ...

    def dump(self) -> bytes: ...


@final
class RequestStockRequest(request):
    @property
    def token(self) -> str: ...

    @token.setter
    def token(self, value) -> NoReturn: ...

    def __new__(cls, token: str) -> RequestStockRequest: ...

    def dump(self) -> bytes: ...


@final
class GuildInfoRequest(request):
    @property
    def token(self) -> str: ...

    @token.setter
    def token(self, value) -> NoReturn: ...

    def __new__(cls, token: str) -> GuildInfoRequest: ...

    def dump(self) -> bytes: ...


@final
class WantToBuyRequest(request):
    @property
    def token(self) -> str: ...

    @token.setter
    def token(self, value) -> NoReturn: ...

    @property
    def itemCode(self) -> str: ...

    @itemCode.setter
    def itemCode(self, value: str) -> NoReturn: ...

    @property
    def quantity(self) -> int: ...

    @quantity.setter
    def quantity(self, value: int) -> NoReturn: ...

    @property
    def price(self) -> int: ...

    @price.setter
    def price(self, value: int) -> NoReturn: ...

    @property
    def exactPrice(self) -> bool: ...

    @exactPrice.setter
    def exactPrice(self, value: bool) -> NoReturn: ...

    def __new__(cls, token: str, itemCode: str, quantity: int, price: int, exactPrice: bool) -> WantToBuyRequest: ...

    def dump(self) -> bytes: ...
