import os

from parser.org import OrganizationInvestorParser

# Get all UUIDs in data/organization
uuids = [p.split('.')[0] for p in os.listdir('data/organization')]

#
# NETWORK
#

# Load the parsers into a list
# The default edge criteria is directed: Investing in another organization
entity_id = 'organization'
parsers = [OrganizationInvestorParser(uuid=uuid, entity_def_id=entity_id) for uuid in uuids]
print('==> Loaded', len(parsers), 'Parsers')

#
# Diagnostics: Find nodes with in-degree or out-degree zero
#

# id_zero = [p for p in parsers if not p.in_links]
od_zero = [p for p in parsers if not p.out_links]

# print('==> Nodes with in-degree of zero:\t', len(id_zero))
print('==> Nodes with out-degree of zero:\t', len(od_zero))

# Average out-degree
out_deg = [p.num_out_links for p in parsers if p.num_out_links != 0]
avg_out_deg = round(sum(out_deg) / len(out_deg), 4)
print('==> Non-zero average out-degree:\t', avg_out_deg)

# TODO: The in-links need to be computed retroactively
# In/Out degree ratio for those not zero
# zero_uuid = [p.uuid for p in id_zero] + [p.uuid for p in od_zero]
# non_zero = [p for p in parsers if p.uuid not in zero_uuid]

# in_out_ratios = [len(p.in_links) / len(p.out_links) for p in non_zero]
# mean_in_out_ratio = round(sum(in_out_ratios) / len(in_out_ratios), 4)

# print('==> Average ratio of in-degree and out-degrees for nodes with non-zero in/out-degrees:\t',
#       mean_in_out_ratio)
