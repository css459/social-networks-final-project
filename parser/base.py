import json
import os
from abc import ABC, abstractmethod

import requests

from parser.util import get_uuid, get_entity_def_id, get_http_out_links

"""
Specifies the relative path of a folder in which
to save .JSON files of Parser's using the `to_file()`
command.
The structure of this directory is:
    data/
        <entity_id>/
            <uuid>.json
            ...
        ...
"""
DATA_DIR = "data/"


class Parser(ABC):
    """
    The Parser abstract class defines an
    architecture for Crunchbase JSON parsing.
    Inheritors of Parser should define the
    properties they wish to keep track of as
    class properties. They should be initialized
    using a URL, which points to a JSON file
    representing something like an Investor or
    Organization.
    """

    def __init__(self, url=None, in_links=None, in_link_relation=None,
                 uuid=None, entity_def_id=None, data_path=None):
        """
        Creates a parser instance tied to a JSON
        file at the specified URL. The instance will
        provide an interface to this JSON file. The file
        will be parsed by the end of initialization with
        all required class properties present.

        If `url` is None, then `uuid` and `entity_def_id` must
        be provided instead. The parser will attempt to load from file.

        :param url:              A Crunchbase URL of an expected
                                 type (e.g.: Org, Investor)
        :param in_links:         An optional list of URLs which
                                 directly reference this URL
        :param in_link_relation: An optional list of objects which
                                 specify how each in-link relates to
                                 this URL.
        :param uuid:             Optional UUID to load from file
        :param entity_def_id:    Optional entity_def_id to load from file
        :param data_path:        Optional data path override to load from file.
                                 Defaults to `DATA_DIR`
        :except ParserException: Thrown when the JSON at the
                                 given URL is unable to be
                                 successfully parsed.
        """
        assert bool(url is not None) != bool(uuid and entity_def_id)

        # Attempt to load from file instead of parsing
        if uuid and entity_def_id:
            if not data_path:
                data_path = DATA_DIR
            self.uuid = uuid
            self.entity_def_id = entity_def_id
            self.from_file(data_path=data_path)
            return

        self.url = url
        self.in_links = in_links
        self.in_link_relation = in_link_relation

        if self.in_links:
            self.num_in_links = len(self.in_links)
        else:
            self.num_in_links = 0

        # Download the JSON at URL
        self._raw = self._download()

        """
        The Crunchbase UUID of the subclass
        entity
        """
        self.uuid = get_uuid(self._raw)
        self.entity_def_id = get_entity_def_id(self._raw)

        # Parse all defined entities
        try:
            self._parse()
        except KeyError as e:
            raise ParserException(e)
        except ParserException as e:
            raise e

        # Stores the out-links of this entity
        self.out_links = self._make_out_links()

        if self.out_links:
            self.num_out_links = len(self.out_links)
        else:
            self.num_out_links = 0

    @abstractmethod
    def _parse(self):
        """
        Parses the relevant information for this Parser
        from the `self._raw` Dictionary, which contains
        the full JSON downloaded from the URL.

        This method should populate all required fields
        for the Parser subclass.

        :return: `None`
        :except ParserException: Thrown when the JSON at the
                                 given URL is unable to be
                                 successfully parsed.
        """
        raise NotImplementedError

    def _make_out_links(self):
        """
        Computes and returns the out-links
        of this URL as a list of URLs it
        directly references.

        :return: List of URLs as Strings
        """
        return get_http_out_links(self._raw, self.uuid)

    def _download(self):
        """
        Downloads the JSON from the specified
        `self.url` and parses it to a Dictionary.

        :return: Dictionary of JSON from `self.url`
        """
        headers = requests.utils.default_headers()
        headers.update({'User-Agent': 'Mozilla/5.0', })
        output = requests.get(self.url, headers=headers).text
        return json.loads(output)

    def to_json(self):
        """
        Returns the parsed JSON as a new JSON
        object. By default, this is all the class'
        parameters. This method can be overwritten
        by subclasses to define a custom JSON output.

        :return: Class as JSON String
        """
        return json.dumps(self.__dict__, indent=4, sort_keys=True)

    def to_file(self, data_path=DATA_DIR):
        """
        Saves the JSON representation of the parser
        to disk at `data_path`. If `data_path` doesn't
        exist, it will be created. If the entity ID subdirectory
        doesn't exist it will also be created. If the JSON file
        for this Parser already exists, it will be overwritten.

        :param data_path:   Path to data folder
        :return:            `None`
        """
        j = self.to_json()
        file_name = str(self.uuid) + '.json'
        p = os.path.join(str(data_path), str(self.entity_def_id))
        if not os.path.exists(p):
            os.makedirs(p)

        p = os.path.join(p, file_name)
        with open(p, 'w') as fp:
            fp.write(j + '\n')

    def from_file(self, data_path=DATA_DIR):
        """
        Loads the Parser class from its JSON file
        on disk.

        :param data_path:   Path to data folder
        :return:            `None`
        """
        file_name = str(self.uuid) + '.json'
        p = os.path.join(str(data_path), str(self.entity_def_id), file_name)
        with open(p, 'r') as fp:
            self.__dict__ = json.load(fp)


class ParserException(Exception):
    """
    Raised when parsing a JSON file results in an
    error due to unexpected formatting, or missing
    required fields.
    """
    pass
