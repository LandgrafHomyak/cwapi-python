from ._utils import _dataclass_creator, encode_string

__all__ = ("CreateAuthCodeRequest", "GrantTokenRequest", "AuthAdditionalOperationRequest", "GrantAdditionalOperationRequest", "GetInfoRequest", "ViewCraftbookRequest", "RequestProfileRequest", "RequestBasicInfoRequest", "RequestGearInfoRequest", "RequestStockRequest", "GuildInfoRequest", "WantToBuyRequest")

from .types import Operation


class request:
    __slots__ = ()

    def dump(self):
        raise NotImplementedError


class CreateAuthCodeRequest(
    request, metaclass=_dataclass_creator,
    names=("userId",),
    types=(int,)
):
    def dump(self):
        return b"""{"action":"createAuthCode","payload":{"userId":%d}}""" % (self.userId,)


class GrantTokenRequest(
    request, metaclass=_dataclass_creator,
    names=("userId", "authCode"),
    types=(int, str)
):
    def dump(self):
        return b"""{"action":"grantToken","payload":{"userId":%d,"authCode":"%b"}}""" % (self.userId, encode_string(self.authCode))


class AuthAdditionalOperationRequest(
    request, metaclass=_dataclass_creator,
    names=("token", "operation"),
    types=(str, Operation)
):
    def dump(self):
        return b"""{"token":"%b","action":"authAdditionalOperation","payload":{"operation":"%b"}}""" % (encode_string(self.token), encode_string(str(self.operation)))


class GrantAdditionalOperationRequest(
    request, metaclass=_dataclass_creator,
    names=("token", "requestId", "authCode"),
    types=(str, str, str)
):
    def dump(self):
        return b"""{"token":"%b","action":"grantAdditionalOperation","payload":{"requestId":"%b","authCode":"%b"}}""" % (encode_string(self.token), encode_string(self.requestId), encode_string(self.authCode))


class GetInfoRequest(
    request, metaclass=_dataclass_creator,
    names=(),
    types=()
):
    def dump(self):
        return b"""{"action":"getInfo"}"""


class ViewCraftbookRequest(
    request, metaclass=_dataclass_creator,
    names=("token",),
    types=(str,)
):
    def dump(self):
        return b"""{"token":"%b","action":"viewCraftbook"}""" % (encode_string(self.token),)


class RequestProfileRequest(
    request, metaclass=_dataclass_creator,
    names=("token",),
    types=(str,)
):
    def dump(self):
        return b"""{"token":"%b","action":"requestProfile"}""" % (encode_string(self.token),)


class RequestBasicInfoRequest(
    request, metaclass=_dataclass_creator,
    names=("token",),
    types=(str,)
):
    def dump(self):
        return b"""{"token":"%b","action":"requestBasicInfo"}""" % (encode_string(self.token),)


class RequestGearInfoRequest(
    request, metaclass=_dataclass_creator,
    names=("token",),
    types=(str,)
):
    def dump(self):
        return b"""{"token":"%b","action":"requestGearInfo"}""" % (encode_string(self.token),)


class RequestStockRequest(
    request, metaclass=_dataclass_creator,
    names=("token",),
    types=(str,)
):
    def dump(self):
        return b"""{"token":"%b","action":"requestStock"}""" % (encode_string(self.token),)


class GuildInfoRequest(
    request, metaclass=_dataclass_creator,
    names=("token",),
    types=(str,)
):
    def dump(self):
        return b"""{"token":"%b","action":"guildInfo"}""" % (encode_string(self.token),)


class WantToBuyRequest(
    request, metaclass=_dataclass_creator,
    names=("token", "itemCode", "quantity", "price", "exactPrice"),
    types=(str, str, int, int, bool)
):
    def dump(self):
        return b"""{"token":"%b","action":"wantToBuy","payload":{"itemCode":"%b","quantity":%d,"price":%d,"exactPrice":%b}}""" % (encode_string(self.token), encode_string(self.itemCode), self.quantity, self.price, b"true" if self.exactPrice else b"false")
