from parser.base import Parser, ParserException


class OrganizationParser(Parser):

    def __init__(self, url, in_links=None, in_link_relation=None):
        super().__init__(url, in_links, in_link_relation)

        # Define properties to track
        # Each property will have a mini-parser staticmethod
        # which gets its value, and is called in _parse().
        self.num_funds = 0
        self.num_funding_rounds = 0
        self.num_exits = 0
        self.num_news_article_features = 0
        self.num_investments = 0
        self.num_technologies_used = 0
        self.num_advisor_positions = 0

        # -------------------------------------------------------------
        # ALL subclasses must call _parse() at end of initialization
        self._parse()
        # -------------------------------------------------------------

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
            return int(d['cards']['advisors_headline']['advisors_headline'])
        except KeyError:
            return 0

    def _parse(self):
        try:
            self.num_funds = OrganizationParser._get_num_funds(self._raw)
            self.num_funding_rounds = OrganizationParser._get_num_funding_rounds(self._raw)
            self.num_exits = OrganizationParser._get_num_exits(self._raw)
            self.num_news_article_features = OrganizationParser._get_num_news_article_features(self._raw)
            self.num_investments = OrganizationParser._get_num_investments(self._raw)
            self.num_technologies_used = OrganizationParser._get_num_technologies_used(self._raw)
            self.num_advisor_positions = OrganizationParser._get_num_advisor_positions(self._raw)
        except KeyError as e:
            raise ParserException(e)

    # TODO: See parser.util.get_http_out_links
    def _make_out_links(self):
        return []
