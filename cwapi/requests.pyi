from abc import abstractmethod
from typing import final, overload, NoReturn


class request:
    @abstractmethod
    def dump(self) -> bytes: ...


class authorized_request(request):
    @property
    def token(self) -> str: ...

    @token.setter
    def token(self, value) -> NoReturn: ...

    def __new__(cls, token: str) -> authorized_request: ...


@final
class CreateAuthCodeRequest(request):
    @property
    def uid(self) -> int: ...

    @uid.setter
    def uid(self, value: int) -> NoReturn: ...

    @property
    def userId(self) -> int: ...

    @uid.setter
    def userId(self, value: int) -> NoReturn: ...

    @overload
    def __new__(cls, uid: int) -> CreateAuthCodeRequest: ...

    @overload
    def __new__(cls, userId: int) -> CreateAuthCodeRequest: ...

    def dump(self) -> bytes: ...


@final
class GrantTokenRequest(request):
    @property
    def uid(self) -> int: ...

    @uid.setter
    def uid(self, value: int) -> NoReturn: ...

    @property
    def userId(self) -> int: ...

    @uid.setter
    def userId(self, value: int) -> NoReturn: ...

    @property
    def code(self) -> str: ...

    @uid.setter
    def code(self, value: str) -> NoReturn: ...

    @property
    def authCode(self) -> str: ...

    @uid.setter
    def authCode(self, value: str) -> NoReturn: ...

    @overload
    def __new__(cls, uid: int, code: str) -> GrantTokenRequest: ...

    @overload
    def __new__(cls, userId: int, authCode: str) -> GrantTokenRequest: ...

    def dump(self) -> bytes: ...


@final
class AuthAdditionalOperationRequest(authorized_request):
    @property
    def operation(self) -> str: ...

    @operation.setter
    def operation(self, value: str) -> NoReturn: ...

    def __new__(cls, token: str, operation: str) -> AuthAdditionalOperationRequest: ...

    def dump(self) -> bytes: ...


@final
class GetInfoRequest(request):
    def dump(self) -> bytes: ...


@final
class ViewCraftbookRequest(authorized_request):
    def dump(self) -> bytes: ...


@final
class RequestProfileRequest(authorized_request):
    def dump(self) -> bytes: ...


@final
class RequestBasicInfoRequest(authorized_request):
    def dump(self) -> bytes: ...


@final
class RequestGearInfoRequest(authorized_request):
    def dump(self) -> bytes: ...


@final
class RequestStockRequest(authorized_request):
    def dump(self) -> bytes: ...


@final
class GuildInfoRequest(authorized_request):
    def dump(self) -> bytes: ...


@final
class WantToBuyRequest(authorized_request):
    @property
    def code(self) -> str: ...

    @code.setter
    def code(self, value: str) -> NoReturn: ...

    @property
    def itemCode(self) -> str: ...

    @code.setter
    def itemCode(self, value: str) -> NoReturn: ...

    @property
    def quantity(self) -> int: ...

    @code.setter
    def quantity(self, value: int) -> NoReturn: ...

    @property
    def price(self) -> int: ...

    @code.setter
    def price(self, value: int) -> NoReturn: ...

    @property
    def exact_price(self) -> bool: ...

    @code.setter
    def exact_price(self, value: bool) -> NoReturn: ...

    @property
    def exactPrice(self) -> bool: ...

    @code.setter
    def exactPrice(self, value: bool) -> NoReturn: ...

    @overload
    def __new__(cls, token: str, code: str, quantity: int, price: int, exact_price: bool) -> WantToBuyRequest: ...

    @overload
    def __new__(cls, token: str, itemCode: str, quantity: int, price: int, exactPrice: bool) -> WantToBuyRequest: ...

    def dump(self) -> bytes: ...
