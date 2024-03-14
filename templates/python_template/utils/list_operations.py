def flatten(iterable):
    arr = []
    for i in iterable:
        if isinstance(i, list):
            arr.extend(i)
        else:
            arr.append(i)
    return arr