"""
Misc. utility and JSON analysis functions
for parsers.
"""


def get_uuid(d):
    """
    Returns the UUID of the URL
    from its JSON as Dictionary.

    :param d:   JSON data as Dictionary
    :return:    UUID as String
    """
    return d['properties']['identifier']['uuid']


def dict_generator(d, pre=None):
    """
    Traverses a full Dictionary object and returns
    a list of all paths to all keys. This is a 2D list.

    :param d:   Input Dictionary
    :param pre: Accumulator for recursive traversal
    :return:    2D list of traversals with values
    """
    pre = pre[:] if pre else []
    if isinstance(d, dict):
        for key, value in d.items():
            if isinstance(value, dict):
                for d in dict_generator(value, pre + [key]):
                    yield d
            elif isinstance(value, list) or isinstance(value, tuple):
                for v in value:
                    for d in dict_generator(v, pre + [key]):
                        yield d
            else:
                yield pre + [key, value]
    else:
        yield pre + [d]


"""
The default keys which will be ignored for `get_only_values()`
and `get_numeric_values()`
"""
default_ignore_keys = ['recommended_search', 'builtwith_tech_used_list']


def get_only_values(d, ngram=1, ngram_join=' ', ignore_keys=None):
    """
    Returns only the values of the input dictionary `d`
    of unknown depth. Optionally, include a look-back
    number of keys to include with the values.

    :param d:               Input Dictionary
    :param ngram:           Number of keys to include in look-back
    :param ngram_join:      String which separates look-back keys
    :param ignore_keys:     Optional list of keys to ignore. Ignores
                            the entire path to value.
    :return:                NGrams as 2D list.
    """
    if ignore_keys is None:
        ignore_keys = default_ignore_keys

    acc = []
    for g in dict_generator(d):
        # Ignore paths 'g' in 'd' that contain ignored keys
        if len([e for e in g if e in ignore_keys]) == 0:
            acc.append(ngram_join.join([str(x) for x in g[-ngram:]]))
    return acc


def get_uuid_out_links(d, this_uuid):
    """
    Finds all referenced UUIDs in the Dictionary
    `d` that are not its own UUID. Returns also
    the tags for each UUID, and the number of
    occurrences for each.

    :param d:           Input Dictionary
    :param this_uuid:   The UUID representing this Dictionary
    :return:            A Dictionary of {uuid: [tags]} and
                        a Dictionary of {uuid: num_occurrences}
    """
    uuids = {}
    counts = {}
    for v in get_only_values(d, ngram=3, ngram_join='**'):
        [ref, lit, uuid] = v.split('**')
        if lit != 'uuid' or uuid == this_uuid:
            continue

        if uuid not in uuids:
            uuids[uuid] = [ref]
            counts[uuid] = 1
        else:
            if ref not in uuids[uuid]:
                uuids[uuid].append(ref)
            counts[uuid] += 1

    return uuids, counts


# TODO: Implement function to convert tagged UUIDs to Crunchbase URLS
def get_http_out_links(d, this_uuid):
    """
    Calls `get_uuid_out_links` and parses tagged UUIDs
    to Crunchbase URLs which point to a JSON file representing
    that UUID. Passes through the list of occurrences for each
    UUID as a list of occurrences of the same length.

    :param d:           Input Dictionary
    :param this_uuid:   The UUID representing this Dictionary
    :return:            A List of URLs and
                        a list of occurrences for each URL.
    """
    uuids, counts = get_uuid_out_links(d, this_uuid)
    # ...
    raise NotImplementedError


def get_numeric_values(d, ignore_keys=None):
    """
    Finds only paths in the Dictionary `d` which
    end in numeric values (leaves).

    :param d:           Input Dictionary
    :param ignore_keys: Optional list of keys to ignore. Ignores
                        the entire path to value.
    :return:            Paths as 2D list.
    """
    if ignore_keys is None:
        ignore_keys = default_ignore_keys

    def _is_num(x):
        return isinstance(x, (int, float, complex)) and not isinstance(x, bool)

    acc = []
    for g in dict_generator(d):
        # Ignore paths 'g' in 'd' that contain ignored keys
        if len([e for e in g if e in ignore_keys]) == 0 and _is_num(g[-1]):
            acc.append(g)
    return acc
