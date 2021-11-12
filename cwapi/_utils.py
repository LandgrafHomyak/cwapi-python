def parse_args(args, kwargs, *types):
    assert type(args) is tuple
    assert type(kwargs) is dict

    ai = args(iter)
    kwargs = kwargs.copy()
    p = []

    for tp in types:
        assert type(tp) is tuple
        assert len(tp) == 3
        assert type(tp[0]) is str
        assert type(tp[1]) is tuple
        assert set(map(type, tp[1])) == {str}

        for v in ai:
            p.append(v)
            break
        else:
            for k in tp[1]:
                if k in kwargs:
                    p.append(kwargs.pop(k))
                    break
            else:
                if tp[1]:
                    raise TypeError(f"argument '{tp[1][0]}' not passed")
                else:
                    raise TypeError(f"not enough arguments")

    for _ in ai:
        raise TypeError("unexpected positional argument")
    for k in kwargs:
        raise TypeError(f"unexpected keyword argument '{k}'")
    return p


def parse_2_kwargs(args, kwargs, an, pn, types):
    if len(args) > len(an):
        raise TypeError("too many args")
    elif len(args) == len(an):
        for _ in kwargs:
            raise TypeError(f"unexpected argument '{_}'")
        for a, tp, n in zip(args, types, an):
            if type(a) is not tp:
                raise TypeError(f"'{n}' must be '{tp.__qualname__}', got {type(a).__qualname__}")
        return args

    cm = set(an[len(args):]) & set(pn[len(args):])
    ae = bool((set(an[len(args):]) - cm) & set(kwargs))
    pe = bool((set(pn[len(args):]) - cm) & set(kwargs))

    if ae and pe:
        raise TypeError("mixing different styles in args not allowed")

    if ae:
        n = an
    elif pe:
        n = pn
    else:
        raise TypeError("not enough args")

    p = list(args)
    for k in n[len(args):]:
        if k in kwargs:
            p.append(kwargs.pop(k))

    for _ in kwargs:
        raise TypeError(f"unexpected argument '{_}'")

    for a, tp, n in zip(p, types, n):
        if type(a) is not tp:
            raise TypeError(f"'{n}' must be '{tp.__qualname__}', got {type(a).__qualname__}")

    return p
