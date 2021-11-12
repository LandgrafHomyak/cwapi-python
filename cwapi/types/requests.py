from .._utils import parse_2_kwargs

__all__ = ("request", "authorized_request", "CreateAuthCodeRequest", "GrantTokenRequest", "AuthAdditionalOperationRequest", "GrantAdditionalOperationRequest", "GetInfoRequest", "ViewCraftbookRequest", "RequestProfileRequest", "RequestBasicInfoRequest", "RequestGearInfoRequest", "RequestStockRequest", "GuildInfoRequest", "WantToBuyRequest")


class request:
    def dump(self):
        raise NotImplementedError


class authorized_request(request):
    __slots__ = "__token"

    def __new__(cls, token):
        self = super().__new__(cls)
        self.token = token
        return self

    @property
    def token(self):
        return self.__token

    @token.setter
    def token(self, value):
        if type(value) is not str:
            raise TypeError(f"token must be str, got {type(value).__qualname__}")
        self.__token = value

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


create_class(
    "CreateAuthCodeRequest",
    False,
    '''b"""{"action":"createAuthCode","payload":{"userId":%d}}""" % (self.__uid,)''',
    (int, "userId", "uid")
)

create_class(
    "GrantTokenRequest",
    False,
    '''b"""{"action":"grantToken","payload":{"userId":%d,"authCode":"%b"}}""" % (self.__uid, self.__code.encode("unicode-escape").replace(b'"', br'\\"'))''',
    (int, "userId", "uid"),
    (str, "authCode", "code"),
)

create_class(
    "AuthAdditionalOperationRequest",
    True,
    '''b"""{"token":%b,"action":"authAdditionalOperation","payload":{"operation":"%b"}}""" % (self.token.encode("unicode-escape").replace(b'"', br'\\"'), self.__operation.encode("unicode-escape").replace(b'"', br'\\"'))''',
    (str, "operation", "operation"),
)

create_class(
    "GrantAdditionalOperationRequest",
    True,
    '''b"""{"token":%b,"action":"grantAdditionalOperation","payload":{"requestId":"%b","authCode":"%b"}}""" % (self.token.encode("unicode-escape").replace(b'"', br'\\"'), self.__request_id.encode("unicode-escape").replace(b'"', br'\\"'), self.__code.encode("unicode-escape").replace(b'"', br'\\"'))''',
    (str, "requestId", "request_id"),
    (str, "authCode", "code"),
)


class GetInfoRequest(request):
    def dump(self):
        return b"""{"action":"getInfo"}"""


class ViewCraftbookRequest(authorized_request):
    def dump(self):
        return b"""{"token":"%b","action":"viewCraftbook"}""" % (self.token.encode("unicode-escape").replace(b'"', br'\\"'),)


class RequestProfileRequest(authorized_request):
    def dump(self):
        return b"""{"token":"%b","action":"requestProfile"}""" % (self.token.encode("unicode-escape").replace(b'"', br'\\"'),)


class RequestBasicInfoRequest(authorized_request):
    def dump(self):
        return b"""{"token":"%b","action":"requestBasicInfo"}""" % (self.token.encode("unicode-escape").replace(b'"', br'\\"'),)


class RequestGearInfoRequest(authorized_request):
    def dump(self):
        return b"""{"token":"%b","action":"requestGearInfo"}""" % (self.token.encode("unicode-escape").replace(b'"', br'\\"'),)


class RequestStockRequest(authorized_request):
    def dump(self):
        return b"""{"token":"%b","action":"requestStock"}""" % (self.token.encode("unicode-escape").replace(b'"', br'\\"'),)


class GuildInfoRequest(authorized_request):
    def dump(self):
        return b"""{"token":"%b","action":"requestStock"}""" % (self.token.encode("unicode-escape").replace(b'"', br'\\"'),)


create_class(
    "WantToBuyRequest",
    True,
    '''b"""{"token":%b,"action":"wantToBuy","payload":{"itemCode":"%b","quantity":%d,"price":%d,"exactPrice":%b}}""" % (self.token.encode("unicode-escape").replace(b'"', br'\\"'), self.__code.encode("unicode-escape").replace(b'"', br'\\"'), self.__quantity, self.__price, b"true" if self.__exact_price else b"false")''',
    (str, "itemCode", "code"),
    (int, "quantity", "quantity"),
    (int, "price", "price"),
    (bool, "exactPrice", "exact_price"),
)
