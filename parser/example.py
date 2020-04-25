from parser.org import OrganizationParser

TEST_URL = "https://www.crunchbase.com/v4/data/entities/organizations/" \
           "ce3d7079-97a0-e664-66cf-add27867cee1?field_ids=%5B%22identifier" \
           "%22,%22layout_id%22,%22facet_ids%22,%22title%22,%22short_description" \
           "%22,%22is_locked%22%5D&layout_mode=view"

org_parser = OrganizationParser(TEST_URL)
print(org_parser.to_json())
