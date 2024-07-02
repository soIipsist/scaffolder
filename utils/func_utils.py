from inspect import signature


def get_callable_args(func, args: dict = None):
    """Given a function, return all of its arguments with default values included."""

    if not callable(func):
        raise ValueError("not a function")

    func_signature = signature(func)
    func_params = {param.name: param for param in func_signature.parameters.values()}

    func_dict = {}
    for key, param in func_params.items():
        if key != "self":
            p = None if param.default == param.empty else param.default
            if args and args.get(key):
                p = args.get(key)
            func_dict.update({key: p})
    return func_dict
