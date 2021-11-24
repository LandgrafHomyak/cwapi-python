__all__ = ()

class _optional_slot_wrapper:
    __slots__ = "__slot", "__type", "_name"

    def __new__(cls, slot, type, name) -> object:
        self = super().__new__(cls)
        self.__slot = slot
        self.__type = type
        self._name = name
        return self

    def __get__(self, instance, owner):
        return self.__slot.__get__(instance, owner)

    def __set__(self, instance, value):
        if type(value) is not self.__type:
            raise TypeError(f"property {self._name !r} must be {self.__type.__qualname__ !r}, got {type(value).__qualname__ !r}")
        return self.__slot.__set__(instance, value)

    def __delete__(self, instance):
        self.__slot.__set__(instance, None)


class _slot_wrapper(_optional_slot_wrapper):
    def __delete__(self, instance):
        raise TypeError(f"property {self._name !r} can't be deleted")


class _dataclass_creator(type):
    def __new__(mcs, name, bases, dct, /, *, names, types, super_names=()):
        assert type(names) is tuple
        assert type(types) is tuple
        assert len(names) == len(types)
        assert all(map(lambda _: type(_) is str, names))
        assert all(map(lambda _: isinstance(_, type) or type(_) is _optional, types))

        dct["__slots__"] = dct.get("__slots__", ())
        assert type(dct["__slots__"]) is tuple
        dct["__slots__"] += names

        assert "__new__" not in dct

        final_args_list = super_names + names

        def new(_cls, *args, **kwargs):
            if len(args) > len(final_args_list):
                raise TypeError("too many args")
            elif len(args) <= len(final_args_list):
                args = list(args)
                for k in final_args_list[len(args):]:
                    try:
                        args.append(kwargs.pop(k))
                    except KeyError:
                        raise TypeError(f"property {k !r} not initialized")

            for _ in kwargs:
                raise TypeError(f"unexpected argument '{_}'")

            self = super(cls, _cls).__new__(_cls, *args[:len(super_names)])

            for n, v in zip(names, args[len(super_names):]):
                if v is None:
                    delattr(self, n)
                else:
                    setattr(self, n, v)

            return self

        dct["__new__"] = new

        cls = type(name, bases, dct)

        for n, t in zip(names, types):
            slot = getattr(cls, n)
            if type(t) is _optional:
                wrapper = _optional_slot_wrapper(slot, t.type, n)
            else:
                wrapper = _slot_wrapper(slot, t, n)
            setattr(cls, n, wrapper)

        return cls


def encode_string(s):
    return s.encode("unicode-escape").replace(b'"', br'\"')


class _optional:
    __slots__ = "type"

    def __new__(cls, tp):
        self = super().__new__(cls)
        self.type = tp
        return self
