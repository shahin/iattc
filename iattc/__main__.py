'''Query the IATTC by vessel name.

Usage:
    iattc VESSEL_NAME

Arguments:
    VESSEL_NAME     the name to search for
'''

from docopt import docopt
from query import search_by_name, get_vessel_details

def main(name):
    search_results = search_by_name(name)

    detail_search_results = []
    for result in search_results:
        detail_result = get_vessel_details(result['vessel_number'])
        detail_result.update(result)
        detail_search_results.append(detail_result)

    return detail_search_results

if __name__ == '__main__':
    args = docopt(__doc__)
    print(main(args['VESSEL_NAME']))
