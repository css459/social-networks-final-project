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


def get_entity_def_id(d):
    """
        Returns the Entity ID of the URL
        from its JSON as Dictionary.

        :param d:   JSON data as Dictionary
        :return:    Entity ID as String
        """
    e = d['properties']['identifier']['entity_def_id']
    if '_identifier' in e:
        e = str(e).replace('_identifier', '')
    return e


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


# TODO: Other mappings for UUID --> URL
def get_http_from_uuid(uuid, entity_def_id):
    """
    Form a URL from a UUID and Entity ID of UUID.
    If a UUID and entity ID is provided for which
    there is no known URL, print a warning and return
    `None`

    :param uuid:            Input UUID
    :param entity_def_id:   Entity ID tag of the UUID
    :return:                URL as String or `None`
    """
    # Maps entity_def_id --> URL format
    # The value string is split where the UUID goes
    url_map = {
        'organization': ["https://www.crunchbase.com/v4/data/entities/organizations/",
                         "?field_ids=%5B%22identifier" +
                         "%22,%22layout_id%22,%22facet_ids%22,%22title%22,%22short_description" +
                         "%22,%22is_locked%22%5D&layout_mode=view"],
        'person': 'TODO',
        'founder': 'TODO',
        'funding_round': 'TODO',
        'location': 'TODO',
    }

    # Some entity_ids may have the postfix "_identifier"
    # For the purpose of this converter, remove it
    entity_def_id = str(entity_def_id).replace('_identifier', '')

    try:
        [u1, u2] = url_map[entity_def_id]
        return u1 + str(uuid) + u2
    except (KeyError, ValueError):
        print('[ WRN ] No known URL for type', entity_def_id, 'UUID:', uuid)
        return None


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
    uuids, _ = get_uuid_out_links(d, this_uuid)

    # Get only a singular key for each UUID
    # if a UUID only has 'identifier', then
    # ignore that UUID altogether
    tmp = {}
    for (k, v) in uuids.items():
        if 'identifier' in v:
            v = v.remove('identifier')
        if v:
            tmp[k] = v[0]
    uuids = tmp

    return list(filter(None, [get_http_from_uuid(u, i)
                              for (u, i) in uuids.items()]))


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


def find_all_by_key(d, key, ignore_keys=None):
    """
    Finds all paths containing the key or value, `key`
    :param d:           Input Dictionary
    :param key:         Query value
    :param ignore_keys: Optional list of keys to ignore. Ignores
                        the entire path to value.
    :return:            Paths as 2D list.
    """
    if ignore_keys is None:
        ignore_keys = default_ignore_keys

    acc = []
    for g in dict_generator(d):
        # Ignore paths 'g' in 'd' that contain ignored keys
        if len([e for e in g if e in ignore_keys]) == 0 and key in g:
            acc.append(g)
    return acc
