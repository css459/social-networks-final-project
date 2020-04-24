import json
from abc import ABC, abstractmethod

import requests


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

    def __init__(self, url, in_links=None, in_link_relation=None):
        """
        Creates a parser instance tied to a JSON
        file at the specified URL. The instance will
        provide an interface to this JSON file. The file
        will be parsed by the end of initialization with
        all required class properties present.

        :param url:              A Crunchbase URL of an expected
                                 type (e.g.: Org, Investor)
        :param in_links:         An optional list of URLs which
                                 directly reference this URL
        :param in_link_relation: An optional list of objects which
                                 specify how each in-link relates to
                                 this URL.
        :except ParserException: Thrown when the JSON at the
                                 given URL is unable to be
                                 successfully parsed.
        """
        assert url is not None

        self.url = url
        self.in_links = in_links
        self.in_link_relation = in_link_relation

        # Download the JSON at URL
        self._raw = self._download()

        """
        The Crunchbase UUID of the subclass
        entity. This is required to be set by
        `_parse()` by the end of initialization.
        """
        self.uuid = None

        # Parse the downloaded JSON at `self._raw`
        self._parse()

        # Stores the out-links of this entity
        self.out_links = self._make_out_links()

        assert self.uuid is not None

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

    @abstractmethod
    def _make_out_links(self):
        """
        Computes and returns the out-links
        of this URL as a list of URLs it
        directly references.

        :return: List of URLs as Strings
        """
        raise NotImplementedError

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


class ParserException(Exception):
    """
    Raised when parsing a JSON file results in an
    error due to unexpected formatting, or missing
    required fields.
    """
    pass
