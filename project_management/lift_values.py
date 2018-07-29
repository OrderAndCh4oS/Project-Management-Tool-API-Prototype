from functools import singledispatch


@singledispatch
def lift_values(obj, match, target_name=None, **kwargs):
    """Lift key-value pairs from a nested structure to the top

    For key-value pairs anywhere in the nested structure, if
    match(path, key, value) returns a value other than `None`, the
    key-value pair is moved to the top-level dictionary when target_name
    is None, or to a new dictionary stored under target_name is not None,
    using the return value of the match function as the key

    For example, for an input

        {'foo': True, 'bar': [{'spam': False, 'ham': 42}]}

    and the match function lambda p, k, v: p + (k,) if isinstance(v, bool) else None
    and target_name "flags", this function returns

        {'flags': {('foo',): True, ('bar', 'spam'): False}, 'bar': [{'ham': 42}]}

    """
    # leaf nodes, no match testing needed, no moving of values
    return obj


@lift_values.register(list)
def _handle_list(obj, match, **kwargs):
    # list values, no lifting, just passing on the recursive call
    return [lift_values(v, match, **kwargs) for v in obj]


@lift_values.register(dict)
def _handle_list(obj, match, target_name=None, _path=(), _target=None):
    result = {}
    if _target is None:
        # this is the top-level object, key-value pairs are lifted to
        # a new dictionary stored at this level:
        if target_name is not None:
            _target = result[target_name] = {}
        else:
            # no target name? Lift key-value pairs into the top-level
            # object rather than a separate sub-object.
            _target = result

    for key, value in obj.items():
        new_key = match(_path, key, value)
        if new_key is not None:
            _target[new_key] = value
        else:
            result[key] = lift_values(value, match, _path=_path + (key,), _target=_target)

    return result


def lift_integers(path, key, value):
    if isinstance(value, int):
        return '__'.join(path[-1:] + (key,))

# result = lift_values(a_dictionary, lift_integers, 'numbers')
