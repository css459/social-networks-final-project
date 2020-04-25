import parser.util as util
from parser.base import Parser, ParserException


# TODO: OrganizationStartupParser


class OrganizationInvestorParser(Parser):

    def __init__(self, url, in_links=None, in_link_relation=None):

        # The base class will handle all downloading, parsing, and
        # out-link generation so long as all required methods have
        # been implemented.
        super().__init__(url, in_links, in_link_relation)

        # Input must be an organization, otherwise
        # the parse doesn't make sense
        assert self.entity_def_id == 'organization'

    #
    # Static Data Extractors
    #

    @staticmethod
    def _get_name(d):
        return str(d['properties']['title'])

    @staticmethod
    def _get_num_investments(d):
        try:
            return int(d['cards']['investments_summary']['num_investments'])
        except KeyError:
            return 0

    @staticmethod
    def _get_num_exits(d):
        try:
            return int(d['cards']['exits_summary']['num_exits'])
        except KeyError:
            return 0

    @staticmethod
    def _get_num_news_article_features(d):
        try:
            return int(d['cards']['news_headline']['num_articles'])
        except KeyError:
            return 0

    @staticmethod
    def _get_num_funds(d):
        try:
            return int(d['cards']['funds_headline']['num_funds'])
        except KeyError:
            return 0

    @staticmethod
    def _get_num_funding_rounds(d):
        try:
            return int(d['cards']['funding_rounds_summary']['num_funding_rounds'])
        except KeyError:
            return 0

    @staticmethod
    def _get_num_technologies_used(d):
        try:
            return int(d['cards']['builtwith_summary']['builtwith_num_technologies_used'])
        except KeyError:
            return 0

    @staticmethod
    def _get_num_advisor_positions(d):
        try:
            return int(d['cards']['advisors_headline']['num_current_advisor_positions'])
        except KeyError:
            return 0

    @staticmethod
    def _get_advisor_uuids(d):
        try:
            return [i['person_identifier']['uuid'] for i in d['cards']['current_advisors_image_list']]
        except KeyError:
            return []

    @staticmethod
    def _get_investment_uuids(d):
        try:
            return [i['organization_identifier']['uuid'] for i in d['cards']['investments_list']]
        except KeyError:
            return []

    #
    # Required Methods
    #

    def _parse(self):

        # _parse() must define all data to track as class properties
        # and raise ParserException if the raw data cannot be properly parsed
        try:
            self.name = OrganizationInvestorParser._get_name(self._raw)
            self.advisor_uuids = OrganizationInvestorParser._get_advisor_uuids(self._raw)
            self.investment_uuids = OrganizationInvestorParser._get_investment_uuids(self._raw)
            self.num_funds = OrganizationInvestorParser._get_num_funds(self._raw)
            self.num_funding_rounds = OrganizationInvestorParser._get_num_funding_rounds(self._raw)
            self.num_exits = OrganizationInvestorParser._get_num_exits(self._raw)
            self.num_news_article_features = OrganizationInvestorParser._get_num_news_article_features(self._raw)
            self.num_investments = OrganizationInvestorParser._get_num_investments(self._raw)
            self.num_technologies_used = OrganizationInvestorParser._get_num_technologies_used(self._raw)
            self.num_advisor_positions = OrganizationInvestorParser._get_num_advisor_positions(self._raw)

            if not self.advisor_uuids and self.num_advisor_positions > 0:
                raise ParserException("Could not find advisor IDs when known number of advisors is "
                                      + str(self.num_advisor_positions))

            if not self.investment_uuids and self.num_investments > 0:
                raise ParserException("Could not find investment IDs when known number of investments is "
                                      + str(self.num_advisor_positions))
        except KeyError as e:
            raise ParserException(e)

    # TODO: See parser.util.get_http_from_uuid
    def _make_out_links(self):
        return []  # REMOVE

        # Form from investor and advisor UUIDs
        acc = []
        for u in self.advisor_uuids:
            http = util.get_http_from_uuid(u, 'person')
            if http:
                acc.append(http)
        for u in self.investment_uuids:
            http = util.get_http_from_uuid(u, 'organization')
            if http:
                acc.append(http)

        return acc
