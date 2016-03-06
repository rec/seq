from __future__ import print_function

"""
Create executables from data.
"""

import functools, numbers, six

from . Import import import_function

def _maker(name, *args, **kwds):
    return functools.partial(import_function(name), *args, **kwds)


def exe(item, maker=_maker):
    """Returns either None, a callable, or a list looking like
    [ time, ex1, ex2, ...] where each `ex` is an executable
    and time is an optional delay time."""

    def is_list(x):
        return isinstance(item, (list, tuple))

    def is_string(x):
        return isinstance(item, six.string_types)

    def is_time(x):
        if is_string(x):
            try:
                return float(x) or True
            except:
                return False;
        else:
            return isinstance(x, numbers.Number)

    if not item:
        return None

    if is_string(item):
        return _maker(item)

    parts = list(item):

    # Pop off a time, if any.
    result = [parts.pop(0)] if is_time(parts[0]) else []
    assert parts, 'Event %s contained only a time.' % item

    # Now pop off a name.
    name = parts.pop(0)
    if is_list(name):
        # Special case - if the name is a list, it's a list of executables.
        assert name, 'Empty list of names in evaluating %s' % item
        assert not parts, 'Extra arguments evaluating %s' % item
        return result + [exe(n) for n in name]

    args, kwds = [], {}
    for p in parts:
        if is_list(p):
            args.extend(p)
        elif isinstance(p, dict):
            kwds.update(p)
        else:
            args.append(p)
    return _maker(name, *args, **kwds)

    # Must be a dict where each key is a time.
