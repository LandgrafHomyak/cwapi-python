from ._utils import _class_creator, encode_string

__all__ = ("request", "CreateAuthCodeRequest", "GrantTokenRequest", "AuthAdditionalOperationRequest", "GrantAdditionalOperationRequest", "GetInfoRequest", "ViewCraftbookRequest", "RequestProfileRequest", "RequestBasicInfoRequest", "RequestGearInfoRequest", "RequestStockRequest", "GuildInfoRequest", "WantToBuyRequest")


class request:
    def dump(self):
        raise NotImplementedError


def create_class(name, has_token, dump, *fields):
    code = f"class {name}({'authorized_request' if has_token else 'request'}):\n\t__slots__ = {tuple(f'__{f[2]}' for f in fields) !r}\n"
    for f in fields:
        code += f"\t@property\n"
        code += f"\tdef {f[1]}(self):return self.__{f[2]}\n"
        code += f"\t@{f[1]}.setter\n"
        code += f"\tdef {f[1]}(self, value):\n"
        code += f"\t\tif type(value) is not {f[0].__name__}:raise TypeError(f'''field '{f[1]}' must be {f[0].__qualname__}, got {{type(value).__qualname__}}''')\n"
        code += f"\t\tself.__{f[2]} = value\n"
        if f[1] != f[2]:
            code += f"\t{f[2]} = {f[1]}\n"

    code += f"\tdef __new__(cls, *args, **kwargs):\n"
    code += f"\t\t{', '.join((('token',) if has_token else ()) + tuple(f[2] for f in fields) + ('',))} = parse_2_kwargs(args, kwargs, {(('token',) if has_token else ()) + tuple(f[1] for f in fields)!r}, {(('token',) if has_token else ()) + tuple(f[2] for f in fields)!r}, ({', '.join((('str',) if has_token else ()) + tuple(f[0].__name__ for f in fields) + ('',))}))\n"
    code += f"\t\tself = super().__new__(cls{', token' if has_token else ''})\n"
    code += f"\t\t{', '.join(tuple(f'self.__{f[2]}' for f in fields) + ('',))} = {', '.join(tuple(f[2] for f in fields))}\n"
    code += f"\t\treturn self\n"
    code += f"\tdef dump(self): return {dump}"
    return exec(code, globals())


class CreateAuthCodeRequest(
    request, metaclass=_class_creator,
    names=("userId",),
    types=(int,)
):
    def dump(self):
        return b"""{"action":"createAuthCode","payload":{"userId":%d}}""" % (self.userId,)


class GrantTokenRequest(
    request, metaclass=_class_creator,
    names=("userId", "authCode"),
    types=(int, str)
):
    def dump(self):
        return b"""{"action":"grantToken","payload":{"userId":%d,"authCode":"%b"}}""" % (self.userId, encode_string(self.authCode))


class AuthAdditionalOperationRequest(
    request, metaclass=_class_creator,
    names=("token", "operation"),
    types=(str, str)
):
    def dump(self):
        return b"""{"token":%b,"action":"authAdditionalOperation","payload":{"operation":"%b"}}""" % (encode_string(self.token), encode_string(self.operation))


class GrantAdditionalOperationRequest(
    request, metaclass=_class_creator,
    names=("token", "requestId", "authCode"),
    types=(str, str, str)
):
    def dump(self):
        return b"""{"token":%b,"action":"grantAdditionalOperation","payload":{"requestId":"%b","authCode":"%b"}}""" % (encode_string(self.token), encode_string(self.requestId), encode_string(self.authCode))


class GetInfoRequest(
    request, metaclass=_class_creator,
    names=(),
    types=()
):
    def dump(self):
        return b"""{"action":"getInfo"}"""


class ViewCraftbookRequest(
    request, metaclass=_class_creator,
    names=("token",),
    types=(str,)
):
    def dump(self):
        return b"""{"token":"%b","action":"viewCraftbook"}""" % (encode_string(self.token),)


class RequestProfileRequest(
    request, metaclass=_class_creator,
    names=("token",),
    types=(str,)
):
    def dump(self):
        return b"""{"token":"%b","action":"requestProfile"}""" % (encode_string(self.token),)


class RequestBasicInfoRequest(
    request, metaclass=_class_creator,
    names=("token",),
    types=(str,)
):
    def dump(self):
        return b"""{"token":"%b","action":"requestBasicInfo"}""" % (encode_string(self.token),)


class RequestGearInfoRequest(
    request, metaclass=_class_creator,
    names=("token",),
    types=(str,)
):
    def dump(self):
        return b"""{"token":"%b","action":"requestGearInfo"}""" % (encode_string(self.token),)


class RequestStockRequest(
    request, metaclass=_class_creator,
    names=("token",),
    types=(str,)
):
    def dump(self):
        return b"""{"token":"%b","action":"requestStock"}""" % (encode_string(self.token),)


class GuildInfoRequest(
    request, metaclass=_class_creator,
    names=("token",),
    types=(str,)
):
    def dump(self):
        return b"""{"token":"%b","action":"requestStock"}""" % (encode_string(self.token),)


class WantToBuyRequest(
    request, metaclass=_class_creator,
    names=("token", "itemCode", "quantity", "price", "exactPrice"),
    types=(str, str, int, int, bool)
):
    def dump(self):
        return b"""{"token":%b,"action":"wantToBuy","payload":{"itemCode":"%b","quantity":%d,"price":%d,"exactPrice":%b}}""" % (encode_string(self.token), encode_string(self.itemCode), self.quantity, self.price, b"true" if self.exactPrice else b"false")
