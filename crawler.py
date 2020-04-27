# Traverses all Organization URLs spanning from the seed URL
# and saves them to file. Implements a breadth-first-search
from parser.org import OrganizationInvestorParser

START = "https://www.crunchbase.com/v4/data/entities/organizations/" \
        "ce3d7079-97a0-e664-66cf-add27867cee1?field_ids=%5B%22identifier" \
        "%22,%22layout_id%22,%22facet_ids%22,%22title%22,%22short_description" \
        "%22,%22is_locked%22%5D&layout_mode=view"

# The total size of the network of connections, rooted
# by this starting URL
total_network_size = 1

start_org = OrganizationInvestorParser(url=START)

print('==> Starting Crawler from UUID:', start_org.uuid)
print('==> Out links:', start_org.num_out_links)

# A list of URLs we need to traverse
queue = list(set(start_org.out_links))

while queue:
    url = queue.pop(0)
    try:
        cur_parser = OrganizationInvestorParser(url=url)
        cur_parser.to_file()
        total_network_size += 1
        new_links = [x for x in list(set(cur_parser.out_links)) if x not in queue]

        print('==> Parsed:', cur_parser.uuid)
        print('==> Found', len(new_links), 'new URLs (out of', len(cur_parser.out_links), 'urls)')
        queue += new_links
        print('==> Queue Size:', len(queue))
    except Exception as e:
        print('[ WRN ] Unable to parse URL:')
        print(e)

print("TOTAL NETWORK SIZE:", total_network_size)
