class slot_wrapper:
    __slots__ = "__slot", "__type", "__name"

    def __new__(cls, slot, type, name):
        self = super().__new__(cls)
        self.__slot = slot
        self.__type = type
        self.__name = name
        return self

    def __get__(self, instance, owner):
        return self.__slot.__get__(instance, owner)

    def __set__(self, instance, value):
        if type(value) is not self.__type:
            raise TypeError(f"property {self.__name!r} must be {self.__type.__qualname__ !r}, got {type(value).__qualname__ !r}")
        return self.__slot.__set__(instance, value)

    def __delete__(self, instance):
        raise TypeError(f"property {self.__name!r} can't be deleted")


class _class_creator(type):
    def __new__(mcs, name, bases, dct, /, *, names, types):
        assert type(names) is tuple
        assert type(types) is tuple
        assert len(names) == len(types)
        assert all(map(lambda _: type(_) is str, names))
        assert all(map(lambda _: isinstance(_, type), types))

        assert type(dct.get("__slots__", ())) is tuple
        dct["__slots__"] = names

        assert "__new__" not in dct

        def new(_cls, *args, **kwargs):
            if len(args) > len(names):
                raise TypeError("too many args")
            elif len(args) <= len(names):
                args = list(args)
                for k in names[len(args):]:
                    try:
                        args.append(kwargs.pop(k))
                    except KeyError:
                        raise TypeError(f"property {k!r} not initialized")

            for _ in kwargs:
                raise TypeError(f"unexpected argument '{_}'")

            self = super(_cls, _cls).__new__(_cls)

            for n, v in zip(names, args):
                setattr(self, n, v)

            return self

        dct["__new__"] = new

        cls = type(name, bases, dct)

        for n, t in zip(names, types):
            wrapper = slot_wrapper(getattr(cls, n), t, n)
            setattr(cls, n, wrapper)

        return cls


def encode_string(s):
    return s.encode("unicode-escape").replace(b'"', br'\"')
