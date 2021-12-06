import json
from warnings import warn

from ._utils import _dataclass_creator, _optional, _slot_wrapper
from .types import _GuildStock, Action, Condition, Gear, GearSet, Guild, GuildRole, GuildRolesSet, Operation, Class, Castle, Quality, Recipe, RecipeBook, SecondaryClass, Status, Stock

__all__ = ("CreateAuthCodeResponse", "GuildInfoResponse", "ApiException", "InvalidTokenError", "WantToBuyResponse", "RequestProfileResponse", "RequestBasicInfoResponse", "RequestStockResponse", "GetInfoResponse", "RequestGearInfoResponse", "ViewCraftbookResponse", "AuthAdditionalOperationResponse", "GrantAdditionalOperationResponse", "GrantTokenResponse", "BadFormatError", "NotInGuildError", "NoSuchUserError", "LevelIsLowError", "ForbiddenError", "ApiException")


class response:
    __slots__ = ()

    def __bool__(self):
        return True


class response_error(Exception, response):
    __slots__ = ()

    def __bool__(self):
        return False


class CreateAuthCodeResponse(
    response, metaclass=_dataclass_creator,
    names=("userId",),
    types=(int,),
):
    pass


class GrantTokenResponse(
    response, metaclass=_dataclass_creator,
    names=("userId", "id", "token"),
    types=(int, str, str),
):
    pass


class AuthAdditionalOperationResponse(
    response, metaclass=_dataclass_creator,
    names=("userId", "operation", "requestId"),
    types=(int, Operation, str),
):
    pass


class GrantAdditionalOperationResponse(
    response, metaclass=_dataclass_creator,
    names=("userId", "requestId"),
    types=(int, str),
):
    pass


class GetInfoResponse(
    response, metaclass=_dataclass_creator,
    names=("balance",),
    types=(int,),
):
    pass


class ViewCraftbookResponse(
    response, metaclass=_dataclass_creator,
    names=("userId", "craft", "alchemy"),
    types=(int, _optional(RecipeBook), _optional(RecipeBook)),
):
    pass


class RequestBasicInfoResponse(
    response, metaclass=_dataclass_creator,
    names=("userId", "class_", "atk", "def_"),
    types=(int, Class, int, int),
):
    pass


class RequestProfileResponse(
    RequestBasicInfoResponse, metaclass=_dataclass_creator,
    names=("castle", "secondaryClass", "hp", "maxHp", "exp", "gold", "guild", "lvl", "status", "action", "mana", "pouches", "stamina", "userName"),
    types=(Castle, _optional(SecondaryClass), int, int, int, int, _optional(Guild), int, Status, Action, int, int, int, str),
    super_names=("userId", "class_", "atk", "def_")
):
    @property
    def full_name(self):
        if self.guild is None or self.guild.tag is None:
            return f"{self.userName}"
        else:
            return f"[{self.guild.tag}]{self.userName}"

    @property
    def full_name_z(self):
        if self.guild is None or self.guild.emoji is None:
            return f"{self.castle.icon}{self.full_name}"
        else:
            return f"{self.guild.emoji}{self.full_name}"

    @property
    def full_name_k(self):
        return f"{self.class_.icon}{self.full_name}"


class RequestGearInfoResponse(GearSet):
    __slots__ = "userId"

    def __new__(cls, userId, **kwargs):
        self = super().__new__(cls, **kwargs)
        self.userId = userId
        return self

    def set(self):
        return GearSet(**{str(s): v for s, v in self if v is not None})


RequestGearInfoResponse.userId = _slot_wrapper(RequestGearInfoResponse.userId, int, "userId")


class RequestStockResponse(Stock):
    __slots__ = "userId", "stockSize", "stockLimit"

    def __new__(cls, *args, **kwargs):
        if len(args) >= 1 and type(args[0]) is not int:
            args, _userId, _stockSize, _stockLimit = (lambda iterable, /, userId, stockSize, stockLimit: (iterable, userId, stockSize, stockLimit))(*args, **kwargs)
        else:
            _userId, _stockSize, _stockLimit, args = (lambda userId, stockSize, stockLimit, *_args: (userId, stockSize, stockLimit, _args))(*args, **kwargs)

        self = super().__new__(cls, *args)
        self.userId = _userId
        self.stockSize = _stockSize
        self.stockLimit = _stockLimit
        return self


RequestStockResponse.userId = _slot_wrapper(RequestStockResponse.userId, int, "userId")
RequestStockResponse.stockSize = _slot_wrapper(RequestStockResponse.stockSize, int, "stockSize")
RequestStockResponse.stockLimit = _slot_wrapper(RequestStockResponse.stockLimit, int, "stockLimit")


class GuildInfoResponse(
    response, metaclass=_dataclass_creator,
    names=("userId", "tag", "level", "castle", "emoji", "glory", "members", "name", "lobby", "stock", "repair", "roles"),
    types=(int, _optional(str), int, Castle, _optional(str), int, int, str, _optional(str), _GuildStock, bool, GuildRolesSet),
):
    @property
    def full_name(self):
        if self.tag is None:
            return f"{self.name}"
        else:
            return f"[{self.tag}]{self.name}"

    @property
    def full_name_z(self):
        return f"{self.castle.icon if self.emoji is None else self.emoji}{self.full_name}"


class WantToBuyResponse(
    response, metaclass=_dataclass_creator,
    names=("userId", "itemName", "quantity"),
    types=(int, str, int)
):
    pass


class ApiException(response_error):
    __slots__ = ("__raw",)

    @property
    def raw(self):
        return self.__raw

    def __new__(cls, raw):
        if type(raw) is not str:
            raise TypeError("raw (unparsed) data required")

        self = super().__new__(cls)
        self.__raw = raw
        return self

    def __init__(self, raw):
        super().__init__(raw)

    def parse(self):
        return json.loads(self.__raw)


class BadFormatError(response_error):
    __slots__ = ()

    def __init__(self):
        super().__init__(f"invalid format in request")


class NoSuchUserError(response_error):
    __slots__ = ("userId",)

    def __new__(cls, userId):
        self = super().__new__(cls)
        self.userId = userId
        return self

    def __init__(self, userId):
        super().__init__(f"user with id {userId} doesn't plays in Chat Wars")


NoSuchUserError.userId = _slot_wrapper(NoSuchUserError.userId, int, "userId")


class InvalidTokenError(response_error):
    __slots__ = ("token",)

    def __new__(cls, token):
        self = super().__new__(cls)
        self.token = token
        return self

    def __init__(self, token):
        super().__init__(f"{token}")


InvalidTokenError.token = _slot_wrapper(InvalidTokenError.token, str, "token")


class InvalidCodeError(response_error):
    __slots__ = ()

    def __init__(self):
        super().__init__("passed code is invalid")


class ForbiddenError(response_error):
    __slots__ = "userId", "requiredOperation", "action"

    def __new__(cls, action, userId, requiredOperation):
        self = super().__new__(cls)
        self.action = action
        self.userId = userId
        self.requiredOperation = requiredOperation
        return self

    def __init__(self, action, userId, requiredOperation):
        super().__init__(f"request {action !r} for user with id {userId} required permission '{requiredOperation !s}'")


ForbiddenError.action = _slot_wrapper(ForbiddenError.action, str, "action")  # todo change to class
ForbiddenError.userId = _slot_wrapper(ForbiddenError.userId, int, "userId")
ForbiddenError.requiredOperation = _slot_wrapper(ForbiddenError.requiredOperation, Operation, "requiredOperation")


class NotInGuildError(response_error):
    __slots__ = ()

    def __init__(self):
        super().__init__(f"player not in guild")


class LevelIsLowError(response_error):
    __slots__ = ("action", "userId")

    def __new__(cls, action, userId):
        self = super().__new__(cls)
        self.action = action
        self.userId = userId
        return self

    def __init__(self, action, userId):
        super().__init__(f"user with id {userId} doesn't have required level for request {action !r}")


LevelIsLowError.action = _slot_wrapper(LevelIsLowError.action, str, "action")
LevelIsLowError.userId = _slot_wrapper(LevelIsLowError.userId, int, "userId")


def parse_response(b, /):
    o = json.loads(b.decode("utf-8"))
    e = None if o["result"] == "Ok" else o["result"]

    if e == "BadFormat":
        raise BadFormatError
    elif e == "NoSuchUser":
        raise NoSuchUserError(userId=o["payload"]["userId"])
    elif e == "InvalidToken":
        raise InvalidTokenError(token=o["payload"]["token"])
    elif e == "InvalidCode":
        raise InvalidCodeError()
    elif e == "Forbidden":
        raise ForbiddenError(action=o["action"], userId=o["payload"]["userId"], requiredOperation=Operation(o["payload"]["requiredOperation"]))
    elif e == "NotInGuild":
        raise NotInGuildError
    elif e == "LevelIsLow":
        raise LevelIsLowError(action=o["action"], userId=o["payload"]["userId"])

    elif e is None:
        a = o["action"]

        if a == "createAuthCode":
            return CreateAuthCodeResponse(userId=o["payload"]["userId"])
        elif a == "grantToken":
            return GrantTokenResponse(userId=o["payload"]["userId"], id=o["payload"]["id"], token=o["payload"]["token"])
        elif a == "authAdditionalOperation":
            return AuthAdditionalOperationResponse(userId=o["payload"]["userId"], operation=Operation(o["payload"]["operation"]), requestId=o["uuid"])
        elif a == "grantAdditionalOperation":
            return GrantAdditionalOperationResponse(userId=o["payload"]["userId"], requestId=o["payload"]["requestId"])
        elif a == "getInfo":
            return GetInfoResponse(balance=o["payload"]["balance"])
        elif a == "viewCraftbook":
            if o["payload"].get("craft", None) is not None:
                c = RecipeBook(Recipe(id=r["id"], name=r["name"], price=r.get("price", 0)) for r in o["payload"]["craft"])
            else:
                c = None
            if o["payload"].get("alchemy", None) is not None:
                a = RecipeBook(Recipe(id=r["id"], name=r["name"], price=r.get("price", 0)) for r in o["payload"]["alchemy"])
            else:
                a = None
            return ViewCraftbookResponse(userId=o["payload"]["userId"], craft=c, alchemy=a)
        elif a == "requestBasicInfo":
            return RequestBasicInfoResponse(userId=o["payload"]["userId"], class_=Class(o["payload"]["profile"]["class"]), atk=o["payload"]["profile"]["atk"], def_=o["payload"]["profile"]["def"])
        elif a == "requestProfile":
            if "guild" in o["payload"]["profile"]:
                g = Guild(name=o["payload"]["profile"]["guild"], tag=o["payload"]["profile"].get("guild_tag", None) or None, emoji=o["payload"]["profile"].get("guild_emoji", None) or None)
            else:
                g = None

            if (r := o["payload"]["profile"].get("secondaryClass", None)) is not None:
                r = SecondaryClass(class_=Class(r["class"]), lvl=r["lvl"])

            return RequestProfileResponse(userId=o["payload"]["userId"], class_=Class(o["payload"]["profile"]["class"]), atk=o["payload"]["profile"].get("atk", 0), def_=o["payload"]["profile"].get("def", 0), castle=Castle(o["payload"]["profile"]["castle"]), secondaryClass=r, hp=o["payload"]["profile"].get("hp", 0), maxHp=o["payload"]["profile"].get("maxHp", 0), exp=o["payload"]["profile"].get("exp", 0), gold=o["payload"]["profile"].get("gold", 0), guild=g, lvl=o["payload"]["profile"]["lvl"], status=Status(o["payload"]["profile"]["status"]), action=Action(o["payload"]["profile"]["action"]), mana=o["payload"]["profile"].get("mana", 0), pouches=o["payload"]["profile"].get("pouches", 0), stamina=o["payload"]["profile"].get("stamina", 0), userName=o["payload"]["profile"]["userName"])
        elif a == "requestGearInfo":
            return RequestGearInfoResponse(
                userId=o["payload"]["userId"],
                **{
                    sn: Gear(name=sv["name"], atk=sv.get("atk", 0), def_=sv.get("def_", 0), condition=Condition(sv.get("condition", Condition.Normal)), quality=Quality(sv.get("quality", Quality.Common)), mana=sv.get("mana", 0))
                    for sn, sv in o["payload"]["gearInfo"].items()
                }
            )
        elif a == "requestStock":
            warn(Warning("method 'requestStock' has bag and maybe raise error, refrain from using it"))
            return RequestStockResponse(Stock.compiler(o["payload"]["stock"], o["payload"]["itemCodes"]), userId=o["payload"]["userId"], stockSize=o["payload"]["stockSize"], stockLimit=o["payload"]["stockLimit"])
        elif a == "guildInfo":
            return GuildInfoResponse(userId=o["payload"]["userId"], tag=o["payload"].get("tag", None) or None, level=o["payload"]["level"], castle=Castle(o["payload"]["castle"]), emoji=o["payload"].get("emoji", None) or None, glory=o["payload"].get("glory", 0), members=o["payload"].get("members", 0), name=o["payload"]["name"], lobby=o["payload"].get("lobby", None) or None, stock=_GuildStock(Stock.compiler(o["payload"]["stock"], o["payload"]["itemCodes"]), size=o["payload"].get("stockSize", 0), limit=o["payload"].get("stockLimit", 0)), repair=o["payload"]["repair"], roles=GuildRolesSet(*map(GuildRole, o["payload"]["roles"])) if "roles" in o["payload"] else GuildRolesSet())
        elif a == "wantToBuy":
            return WantToBuyResponse(userId=o["payload"]["userId"], itemName=o["payload"]["itemName"], quantity=o["payload"].get("quantity", 0))

    raise ApiException(b.decode("utf-8"))
