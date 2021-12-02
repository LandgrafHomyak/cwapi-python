from enum import Enum, Flag
from typing import ClassVar, Generator, Iterable, Iterator, Literal, Mapping, NoReturn, Optional, Tuple, Union, final, overload


@final
class Operation(str, Enum):
    def __str__(self) -> str: ...

    GetBasicInfo: ClassVar[str] = "GetBasicInfo"
    GetUserProfile: ClassVar[str] = "GetUserProfile"
    ViewCraftbook: ClassVar[str] = "ViewCraftbook"
    GetGearInfo: ClassVar[str] = "GetGearInfo"
    GetStock: ClassVar[str] = "GetStock"
    GuildInfo: ClassVar[str] = "GuildInfo"
    TradeTerminal: ClassVar[str] = "TradeTerminal"


@final
class Class(str, Enum):
    def __str__(self) -> str: ...

    warrior: ClassVar[str] = "\U0001F423"

    knight: ClassVar[str] = "\u2694\uFE0F"
    sentinel: ClassVar[str] = "\U0001F6E1"
    ranger: ClassVar[str] = "\U0001F3F9"

    collector: ClassVar[str] = "\U0001F4E6"
    blacksmith: ClassVar[str] = "\u2692"
    alchemist: ClassVar[str] = "\u2697\uFE0F"


@final
class Castle(str, Enum):
    def __str__(self) -> str: ...

    oplot: ClassVar[str] = "\u2618\uFE0F"
    rassvet: ClassVar[str] = "\U0001F339"
    skala: ClassVar[str] = "\U0001F5A4"
    tortuga: ClassVar[str] = "\U0001F422"
    night: ClassVar[str] = "\U0001F987"
    ferma: ClassVar[str] = "\U0001F346"
    amber: ClassVar[str] = "\U0001F341"


@final
class SecondaryClass:
    @property
    def class_(self) -> Class: ...

    @class_.setter
    def class_(self, value: Class) -> NoReturn: ...

    @property
    def lvl(self) -> int: ...

    @lvl.setter
    def lvl(self, value: int) -> NoReturn: ...

    def __new__(cls, class_: Class, lvl: int) -> SecondaryClass: ...

    def __str__(self) -> str: ...


@final
class Guild:
    @property
    def name(self) -> str: ...

    @name.setter
    def name(self, value: str) -> NoReturn: ...

    @property
    def tag(self) -> Optional[str]: ...

    @tag.setter
    def tag(self, value: str) -> NoReturn: ...

    @tag.deleter
    def tag(self) -> NoReturn: ...

    @property
    def emoji(self) -> Optional[str]: ...

    @emoji.setter
    def emoji(self, value: str) -> NoReturn: ...

    @emoji.deleter
    def emoji(self) -> NoReturn: ...

    def __new__(cls, name: str, tag: Optional[str], emoji: Optional[str]) -> Guild: ...

    def __str__(self) -> str: ...


@final
class Status(str, Enum):
    def __str__(self) -> str: ...

    Idle: ClassVar[str] = "Idle"
    Busy: ClassVar[str] = "Busy"


@final
class Action(str, Enum):
    def __str__(self) -> str: ...

    Idle: ClassVar[str] = "Idle"
    Conflict: ClassVar[str] = "Conflict"
    Quest: ClassVar[str] = "Quest"


@final
class Condition(str, Enum):
    def __str__(self) -> str: ...

    Normal: ClassVar[str] = "Normal"
    Reinforced: ClassVar[str] = "Reinforced"
    Broken: ClassVar[str] = "Broken"


@final
class Quality(str, Enum):
    # only known qualities

    def __str__(self) -> str: ...

    Common = "Common"

    Fine: ClassVar[str] = "Fine"
    High: ClassVar[str] = "High"
    Great: ClassVar[str] = "Great"
    Excellent: ClassVar[str] = "Excellent"
    Masterpiece: ClassVar[str] = "Masterpiece"

    EpicFine: ClassVar[str] = "Epic Fine"
    EpicHigh: ClassVar[str] = "Epic High"
    EpicGreat: ClassVar[str] = "Epic Great"
    EpicExcellent: ClassVar[str] = "Epic Excellent"
    EpicMasterpiece: ClassVar[str] = "Epic Masterpiece"


@final
class Gear:
    @property
    def name(self) -> str: ...

    @name.setter
    def name(self, value: str) -> NoReturn: ...

    @property
    def atk(self) -> int: ...

    @atk.setter
    def atk(self, value: int) -> NoReturn: ...

    @property
    def def_(self) -> int: ...

    @def_.setter
    def def_(self, value: int) -> NoReturn: ...

    @property
    def condition(self) -> Condition: ...

    @condition.setter
    def condition(self, value: Condition) -> NoReturn: ...

    @property
    def quality(self) -> Quality: ...

    @quality.setter
    def quality(self, value: Quality) -> NoReturn: ...

    @property
    def mana(self) -> Quality: ...

    @mana.setter
    def mana(self, value: Quality) -> NoReturn: ...

    def __new__(cls, name: str, atk: int, def_: int, condition: Condition, quality: Quality, mana: int) -> Gear: ...


@final
class GearSlot(str, Enum):
    def __str__(self) -> str: ...

    weapon: ClassVar[str] = "weapon"
    offhand: ClassVar[str] = "offhand"

    head: ClassVar[str] = "head"
    body: ClassVar[str] = "body"
    hands: ClassVar[str] = "hands"
    feet: ClassVar[str] = "feet"

    coat: ClassVar[str] = "coat"

    amulet: ClassVar[str] = "amulet"
    ring: ClassVar[str] = "ring"


@final
class GearSet:
    def __new__(cls, *, weapon: Gear = ..., offhand: Gear = ..., head: Gear = ..., body: Gear = ..., hands: Gear = ..., feet: Gear = ..., coat: Gear = ..., amulet: Gear = ..., ring: Gear = ...) -> GearSet: ...

    def __getitem__(self, s: Union[GearSlot, str]) -> Optional[Gear]: ...

    def __setitem__(self, s: Union[GearSlot, str], v: Gear) -> NoReturn: ...

    def __delitem__(self, s: Union[GearSlot, str]) -> NoReturn: ...

    def __iter__(self) -> Iterator[Tuple[GearSlot, Optional[Gear]]]: ...

    def __contains__(self, s: Union[GearSlot, str]) -> bool: ...


@final
class Recipe:
    @property
    def id(self) -> str: ...

    @id.setter
    def id(self, value: str) -> NoReturn: ...

    @property
    def name(self) -> str: ...

    @name.setter
    def name(self, value: str) -> NoReturn: ...

    @property
    def price(self) -> int: ...

    @price.setter
    def price(self, value: int) -> NoReturn: ...

    def __new__(cls, id: str, name: str, price: int) -> Recipe: ...


@final
class RecipeBook:
    @overload
    def __new__(cls, *args: Recipe) -> RecipeBook: ...

    @overload
    def __new__(cls, iterable: Iterable[Recipe], /) -> RecipeBook: ...

    def __iter__(self) -> Iterator[Recipe]: ...

    def __getitem__(self, id: str) -> Recipe: ...

    def __setitem__(self, id: str, rec: Recipe) -> NoReturn: ...

    def __delitem__(self, id: str) -> NoReturn: ...

    def __contains__(self, id: str) -> bool: ...

    def __len__(self) -> int: ...


@final
class QuantityRange:
    @property
    def start(self) -> int: ...

    @start.setter
    def start(self, v: int) -> NoReturn: ...

    @property
    def end(self) -> int: ...

    @end.setter
    def end(self, v: int) -> NoReturn: ...

    def __new__(cls, start: int, end: int) -> QuantityRange: ...

    def __contains__(self, v: int) -> bool: ...

    def __lt__(self, other: int) -> bool: ...

    def __le__(self, other: int) -> bool: ...

    def __gt__(self, other: int) -> bool: ...

    def __ge__(self, other: int) -> bool: ...

    def __eq__(self, other: QuantityRange) -> bool: ...


@final
class StockCell:
    @property
    def code(self) -> str: ...

    @code.setter
    def code(self, v: str) -> NoReturn: ...

    @property
    def name(self) -> str: ...

    @name.setter
    def name(self, v: str) -> NoReturn: ...

    @property
    def quantity(self) -> Union[int, QuantityRange]: ...

    @quantity.setter
    def quantity(self, v: Union[int, QuantityRange]) -> NoReturn: ...

    def __new__(cls, code: str, name: str, quantity: Union[int, QuantityRange]) -> StockCell: ...


@final
class Stock:
    @overload
    def __new__(cls, *args: StockCell) -> Stock: ...

    @overload
    def __new__(cls, iterable: Iterable[StockCell], /) -> Stock: ...

    @staticmethod
    def compiler(n2q: Mapping[str, int], c2n: Mapping[str, str], /) -> Generator[StockCell]: ...

    def __getitem__(self, c: str) -> StockCell: ...

    def __setitem__(self, c: str, r: StockCell) -> NoReturn: ...

    def __delitem__(self, c: str) -> NoReturn: ...

    def __contains__(self, c: str) -> bool: ...

    def __iter__(self) -> Iterator[StockCell]: ...


@final
class _GuildStock(Stock):
    @property
    def size(self) -> int: ...

    @size.setter
    def size(self, v: int) -> NoReturn: ...

    @property
    def limit(self) -> int: ...

    @limit.setter
    def limit(self, v: int) -> NoReturn: ...

    @overload
    def __new__(cls, size: int, limit: int, *args: StockCell) -> _GuildStock: ...

    @overload
    def __new__(cls, iterable: Iterable[StockCell], /, size: int, limit: int) -> _GuildStock: ...


@final
class GuildRolesSet:
    def __new__(cls, *args: Union[GuildRole, GuildRolesSet]) -> GuildRolesSet: ...

    def __or__(self, other: Union[GuildRole, GuildRolesSet]) -> GuildRolesSet: ...

    def __and__(self, role: GuildRole) -> bool: ...

    def __contains__(self, role: GuildRole) -> bool: ...

    def __str__(self) -> str: ...


@final
class GuildRole(Flag):
    NoRole: ClassVar[GuildRole] = None
    # Commander: ClassVar[GuildRole] = "Commander"
    Creator: ClassVar[GuildRole] = "Creator"
    Squire: ClassVar[GuildRole] = "Squire"
    Bartender: ClassVar[GuildRole] = "Bartender"
    Treasurer: ClassVar[GuildRole] = "Treasurer"

    def __or__(self, other: Union[GuildRole, GuildRolesSet]) -> GuildRolesSet: ...
