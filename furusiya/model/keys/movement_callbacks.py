def up(callback, *args, **kwargs):
    return callback(0, -1, *args, **kwargs)


def down(callback, *args, **kwargs):
    return callback(0, 1, *args, **kwargs)


def left(callback, *args, **kwargs):
    return callback(-1, 0, *args, **kwargs)


def right(callback, *args, **kwargs):
    return callback(1, 0, *args, **kwargs)
