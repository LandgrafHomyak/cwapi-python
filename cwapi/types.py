from enum import Enum, Flag

from cwapi._utils import _dataclass_creator, _optional, _slot_wrapper, encode_string

__all__ = ()


class Operation(str, Enum):
    # todo find how to get name in __new__

    def __str__(self):
        return self.value

    GetBasicInfo = "GetBasicInfo"
    GetUserProfile = "GetUserProfile"
    ViewCraftbook = "ViewCraftbook"
    GetGearInfo = "GetGearInfo"
    GetStock = "GetStock"
    GuildInfo = "GuildInfo"
    TradeTerminal = "TradeTerminal"


class Class(str, Enum):
    def __str__(self):
        return self.value

    warrior = "\U0001F423"

    knight = "\u2694\uFE0F"
    sentinel = "\U0001F6E1"
    ranger = "\U0001F3F9"

    collector = "\U0001F4E6"
    blacksmith = "\u2692"
    alchemist = "\u2697\uFE0F"


class Castle(str, Enum):
    def __str__(self):
        return self.value

    oplot = "\u2618\uFE0F"
    rassvet = "\U0001F339"
    skala = "\U0001F5A4"
    tortuga = "\U0001F422"
    night = "\U0001F987"
    ferma = "\U0001F346"
    amber = "\U0001F341"


_SUPERSCRIPT_DIGIT_MAP = {
    0x30: 0x2070,
    0x31: 0x00B9,
    0x32: 0x00B2,
    0x33: 0x00B3,
    0x34: 0x2074,
    0x35: 0x2075,
    0x36: 0x2076,
    0x37: 0x2077,
    0x38: 0x2078,
    0x39: 0x2079,
}


class SecondaryClass(
    metaclass=_dataclass_creator,
    names=("class_", "lvl"),
    types=(Class, int)
):
    def __str__(self):
        return f"{self.class_ !s}{str(self.lvl).translate(_SUPERSCRIPT_DIGIT_MAP)}"


class Guild(
    metaclass=_dataclass_creator,
    names=("name", "tag", "emoji"),
    types=(str, _optional(str), _optional(str))
):
    def __str__(self):
        return (f"[{self.tag}]" if self.tag is not None else "") + self.name


class Status(str, Enum):
    def __str__(self):
        return self.value

    Idle = "Idle"
    Busy = "Busy"


class Action(str, Enum):
    def __str__(self):
        return self.value

    Idle = "Idle"
    Conflict = "Conflict"
    Quest = "Quest"


class Condition(str, Enum):
    def __str__(self):
        return self.value

    Normal = "Normal"
    Reinforced = "Reinforced"
    Broken = "Broken"


class Quality(str, Enum):
    def __str__(self):
        return self.value

    Common = "Common"

    Fine = "Fine"
    High = "High"
    Great = "Great"
    Excellent = "Excellent"
    Masterpiece = "Masterpiece"

    EpicFine = "Epic Fine"
    EpicHigh = "Epic High"
    EpicGreat = "Epic Great"
    EpicExcellent = "Epic Excellent"
    EpicMasterpiece = "Epic Masterpiece"


class Gear(
    metaclass=_dataclass_creator,
    names=("name", "atk", "def_", "condition", "quality", "mana"),
    types=(str, int, int, Condition, Quality, int),
):
    pass


class GearSlot(str, Enum):
    def __str__(self):
        return self.value

    weapon = "weapon"
    offhand = "offhand"

    head = "head"
    body = "body"
    hands = "hands"
    feet = "feet"

    coat = "coat"

    amulet = "amulet"
    ring = "ring"


class GearSet:
    __slots__ = "__dct"

    def __new__(cls, **kwargs):
        self = super().__new__(cls)
        self.__gears_dict = {s: None for s in GearSlot.__members__.keys()}
        for s, v in kwargs.items():
            self[GearSlot(s)] = v
        return self

    def __getitem__(self, s):
        return self.__dct[GearSlot(s)]

    def __setitem__(self, s, v):
        if type(v) is not Gear:
            raise TypeError(f"GearsSet can be filled only by {Gear.__qualname__ !r} objects, got {type(v).__qualname__ !r}")
        self.__dct[GearSlot(s)] = v

    def __delitem__(self, s):
        self.__dct[GearSlot(s)] = None

    def __iter__(self):
        return iter(self.__dct.items())

    def __contains__(self, s):
        return GearSlot(s) in self.__dct


class Recipe(
    metaclass=_dataclass_creator,
    names=("id", "name", "price"),
    types=(str, str, int)
):
    def dump(self):
        return b"""{"id":"%b","name":"%b","price":%d}""" % (encode_string(self.id), encode_string(self.name), self.price)


_sentinel = object()


class RecipeBook:
    __slots__ = "__dct"

    def __new__(cls, *args):
        if len(args) == 1 and type(args[0]) is not Recipe:
            args = args[0]
        self = super().__new__(cls)
        self.__dct = dict()
        for rec in args:
            if rec.id in self:
                raise ValueError(f"duplication of recipe for item with id {rec.id !r}")
            self[rec.id] = rec
        return self

    def __iter__(self):
        return iter(self.__dct.values())

    def __getitem__(self, id):
        if type(id) is not str:
            raise TypeError(f"item id must be str, got {type(str).__qualname__ !r}")
        return self.__dct[id]

    def __setitem__(self, id, rec):
        if type(id) is not str:
            raise TypeError(f"item id must be str, got {type(str).__qualname__ !r}")
        if type(rec) is not Recipe:
            raise TypeError(f"recipe must be {Recipe.__qualname__ !r}, got {type(rec).__qualname__ !r}")
        self.__dct[id] = rec

    def __delitem__(self, id):
        if type(id) is not str:
            raise TypeError(f"item id must be str, got {type(str).__qualname__ !r}")
        del self.__dct[id]

    def __contains__(self, id):
        if type(id) is not str:
            raise TypeError(f"item id must be str, got {type(str).__qualname__ !r}")
        return id in self.__dct

    def __len__(self):
        return len(self.__dct)


class QuantityRange:
    __slots__ = "__start", "__end"

    @property
    def start(self):
        return self.__start

    @start.setter
    def start(self, v):
        if type(v) is not int:
            raise TypeError(f"range limits must be int, got {type(v).__qualname__ !r}")
        if v >= self.__end:
            raise ValueError("invalid range")
        self.__start = v

    @property
    def end(self):
        return self.__end

    @end.setter
    def end(self, v):
        if type(v) is not int:
            raise TypeError(f"range limits must be int, got {type(v).__qualname__ !r}")
        if v <= self.__start:
            raise ValueError("invalid range")
        self.__end = v

    def __new__(cls, start, end):
        self = super().__new__(cls)
        self.__start = float("-inf")
        self.end = end
        self.start = start
        return self

    def __contains__(self, v):
        if type(v) is not int:
            raise TypeError("only ints can be in range")
        return self.__start <= v <= self.__end

    def __lt__(self, other):
        if type(other) is not int:
            raise TypeError("comparing allowed only with ints")
        return self.__start < other

    def __le__(self, other):
        if type(other) is not int:
            raise TypeError("comparing allowed only with ints")
        return self.__start <= other

    def __gt__(self, other):
        if type(other) is not int:
            raise TypeError("comparing allowed only with ints")
        return self.__start > other

    def __ge__(self, other):
        if type(other) is not int:
            raise TypeError("comparing allowed only with ints")
        return self.__start >= other

    def __eq__(self, other):
        if type(other) is not QuantityRange:
            raise TypeError("check for identity allowed only with other ranges")
        return self.__start == other.__start and self.__end == other.__end


class StockCell:
    __slots__ = "code", "name", "__quantity"

    @property
    def quantity(self):
        return self.__quantity

    @quantity.setter
    def quantity(self, v):
        if type(v) is not int and type(v) is not QuantityRange:
            raise TypeError(f"quantity must be int ot {QuantityRange.__qualname__ !r}, got {type(v).__qualname__ !r}")
        self.__quantity = v

    def __new__(cls, code, name, quantity):
        self = super().__new__(cls)
        self.code = code
        self.name = name
        self.quantity = quantity
        return self


StockCell.code = _slot_wrapper(StockCell.code, str, "code")
StockCell.name = _slot_wrapper(StockCell.name, str, "name")


class Stock:
    __slots__ = "__dct"

    def __new__(cls, *args):
        if len(args) == 1 and type(args[0]) is not StockCell:
            args = args[0]
        self = super().__new__(cls)
        self.__dct = dict()
        for cell in args:
            if cell.code in self:
                raise ValueError(f"duplication of item with code {cell.code !r}")
            self[cell.code] = cell
        return self

    @staticmethod
    def compiler(n2q, c2n, /):
        n2c = dict()
        for c, n in c2n.items():
            if n in n2c:
                n2c[n].append(c)
            else:
                n2c[n] = [c]
        for n, q in n2q.items():
            cc = n2c[n]
            lcc = len(cc)
            if lcc == 1:
                yield StockCell(code=cc[0], name=n, quantity=q)
            elif q == lcc:
                for c in cc:
                    yield StockCell(code=c, name=n, quantity=1)
            else:
                q = q - lcc + 1
                for c in cc:
                    yield StockCell(code=c, name=n, quantity=QuantityRange(1, q))

    def __getitem__(self, c):
        if type(c) is not str:
            raise TypeError(f"item code must be str, got {type(c).__qualname__ !r}")
        return self.__dct[c]

    def __setitem__(self, c, r):
        if type(c) is not str:
            raise TypeError(f"item code must be str, got {type(c).__qualname__ !r}")
        if type(r) is not StockCell:
            raise TypeError(f"stock cell must be {StockCell.__qualname__ !r}, got {type(c).__qualname__ !r}")
        self.__dct[c] = r

    def __delitem__(self, c):
        if type(c) is not str:
            raise TypeError(f"item code must be str, got {type(c).__qualname__ !r}")
        del self.__dct[c]

    def __contains__(self, c):
        if type(c) is not str:
            raise TypeError(f"item code must be str, got {type(c).__qualname__ !r}")
        return c in self.__dct

    def __iter__(self):
        return iter(self.__dct.values())


class _GuildStock(Stock):
    __slots__ = "size", "limit"

    def __new__(cls, *args, **kwargs):
        if len(args) >= 1 and type(args[0]) is not int:
            args, _size, _limit = (lambda iterable, /, size, limit: (iterable, size, limit))(*args, **kwargs)
        else:
            _size, _limit, args = (lambda size, limit, *_args: (size, limit, _args))(*args, **kwargs)

        self = super().__new__(cls, *args)
        self.size = _size
        self.limit = _limit
        return self


_GuildStock.size = _slot_wrapper(_GuildStock.size, int, "size")
_GuildStock.limit = _slot_wrapper(_GuildStock.limit, int, "limit")


class GuildRolesSet:
    __slots__ = "__fzs"

    def __new__(cls, *args):
        s = set()
        for a in args:
            if type(a) is GuildRolesSet:
                s |= a.__fzs
            elif type(a) is GuildRole:
                s.add(a)
            else:
                raise TypeError("unexpected role")
        self = super().__new__(cls)
        self.__fzs = frozenset(s - {GuildRole.NoRole})
        return self

    def __or__(self, other):
        return GuildRolesSet(self, other)

    def __and__(self, other):
        return other in self

    def __contains__(self, role):
        if type(role) is not GuildRole:
            raise TypeError(f"only {GuildRole.__qualname__} objects can be in set")
        if role is GuildRole.NoRole:
            return len(self.__fzs) == 0
        return role in self.__fzs

    def __str__(self):
        if len(self.__fzs) > 0:
            return str(set(self.__fzs))
        else:
            return str(GuildRole.NoRole)


class GuildRole(Flag):
    NoRole = None
    # Commander = "Commander"
    Creator = "Creator"
    Squire = "Squire"
    Bartender = "Bartender"
    Treasurer = "Treasurer"

    def __or__(self, other):
        return GuildRolesSet(self, other)
