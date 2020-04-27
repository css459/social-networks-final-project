from parser.org import OrganizationInvestorParser

TEST_URL = "https://www.crunchbase.com/v4/data/entities/organizations/" \
           "ce3d7079-97a0-e664-66cf-add27867cee1?field_ids=%5B%22identifier" \
           "%22,%22layout_id%22,%22facet_ids%22,%22title%22,%22short_description" \
           "%22,%22is_locked%22%5D&layout_mode=view"

# Example of Initialization
org_parser = OrganizationInvestorParser(url=TEST_URL)

# Example of file saving and file reading
org_parser.to_file()
org_parser.from_file()

# Example of loading instance from file
uuid = 'ce3d7079-97a0-e664-66cf-add27867cee1'
entity_id = 'organization'
org_parser2 = OrganizationInvestorParser(uuid=uuid, entity_def_id=entity_id)
print(org_parser2.to_json())

# This line will cause an exception
invalid_org_parser = OrganizationInvestorParser(url=TEST_URL, uuid=uuid, entity_def_id=entity_id)
