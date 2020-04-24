from parser.base import Parser, ParserException

TEST_URL = "https://www.crunchbase.com/v4/data/entities/organizations/" \
           "ce3d7079-97a0-e664-66cf-add27867cee1?field_ids=%5B%22identifier" \
           "%22,%22layout_id%22,%22facet_ids%22,%22title%22,%22short_description" \
           "%22,%22is_locked%22%5D&layout_mode=view"


class OrganizationParser(Parser):

    def __init__(self, url, in_links=None, in_link_relation=None):
        super().__init__(url, in_links, in_link_relation)

    def _parse(self):
        try:
            pass
        except KeyError as e:
            raise ParserException(e)

    def _make_out_links(self):
        return []
