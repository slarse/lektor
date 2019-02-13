"""Source file with while loops for testing the coverage tool."""


def bounded_looping(n, limit):
    """Loop at least n times, but at most limit times.
    Limit takes precedence, and must be positive.
    """
    if limit < 0:
        return
    elif n > limit:
        n = limit
    i = 0
    while i < n:
        i += 1


def bounded_looping_break(n, limit):
    """Same as bounded_looping, but with a while-true construct."""
    if limit < 0:
        return
    elif n > limit:
        n = limit
    i = 0
    while True:
        if i >= n:
            break
        else:  # redundant else for fun
            i += 1
