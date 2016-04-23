import re

import requests
from bs4 import BeautifulSoup

SEARCH_URL = 'https://www.iattc.org//VesselRegister/SearchVessel.aspx?Lang=ENG'
SEARCH_REQUEST_DATA_TEMPLATE = {
    'btnSearch': 'Search',
    'Gears': -1,
    'Flags': -1,
    'DateConfirmed':'_ctl15',
    '__VIEWSTATEGENERATOR': 'B0132FB3',
    '__VIEWSTATE':'/wEPDwULLTE1MTQ0ODQ4NDJkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYHBQVHZWFycwUFRmxhZ3MFBl9jdGwxMwUGX2N0bDEzBQZfY3RsMTQFBl9jdGwxNAUGX2N0bDE1iFEcH83gdaLuYZycnk6vXnKQbfTYF/8OlJRFPCOnCUs=',
    '__EVENTVALIDATION':'/wEdAF1Q9b6Ve5MKUozI51W8QUUmwvK2xWrKM28XIQtDQETRytnY3P3xBpyHaxL2RkS8t9dPp6miBYpGt13kzRE56RK/IlvXCCq8DQre/mwgzyyG6AxlyBB7Z4heRX4QXJb7JtKAdP/JOW0dY4dIsRHgDQe5wObD8ob4oQvjPFFsu0lEtggvkBATcacK4bwnSqvv/8TgeKOf6oRTQ7BZdSrGbi7ou5XJXzurPqDbUPV2TXbIR37qmlddxWep1MJgL1mr63Qc31SyZ/po2xoflIHjEDYFGnHW7lx3Db7RLgWVFpGkhI2/xiR/a8dmDw5vvyhR/VKuJeq9Qg88xx9Pv3xFOQixDxJUjZeh+q/mlEl0OOuEmhx1wonj/wS+7CYoCL+XfFVClMsHwoZQpCh6w6xUgTj18LjD2jcaIzoT9orzGIbN93kYOS3q2rBEEGPwStKp9w2Ln5X9rFIjMk3T7+mNuRfFclQ2XtCysp7ewi/3vmj4AxvGjRQ/UeLyBzo/9cFao1vJtIDgtuFEdNfeR2kSv3EjJ9pQzylP3miDKq9Da+jsnSGnisX2pYisP36Fsw9UHVU16EvOTgV2jZW3V3YqGfqBDAG0yNq1JvsJORHl7qkuSqN10NDhmmsx+G5bgArPmk/1Uc/a4ZmDxpwr9DpydbZKJmdylPKXbJWzKuVTMm48QLV3qOsJOrLs3ijlh4XQg+oRzfmT4rySpqOqBkIRd8+54hQ0YeKt49Cbk1ElxQWOcSiZtT3LvQuSE/Flbg0stGgTX6HIGVQkKOlA1y4t7zH/tY0bdOKkiriYnFPVRPaG24JoL/RhEQd8//sbnGrwFD41JdS2uJwhpZCDGzIzTyz0vnOr7dfYqDPM/RapMOriDHCbB27n6CB66CZnScy5NCyYGPOhEbu+wK4tLkhXFVs9SSHm0q4jTet9EQDhvsNQAmjiqerYDfyJcxHNeXAQ5MjoqcUpnpkDFKQ/gkys6ylZp6WyDuOQ7aiwjn8YMK4oR7SDn05kyWvivPQtYqSVlI9HNTRceKU8JYfKGfsuI1v/C3M3q6HVXJ5IbWy4s2k8QKPMqo76XyezEodJAk/D43nggP7Lkq+P45NqDpBdjHzhwEGRW5F3hhJi4ToIz8A8jAghwGMnKqmIBlpPPKecribHRxMsaJwRjsQYW+mLsXl9PzHgPLblS3VJB47ScXRJvHxxiktrBVa+XYOswBwoNbr18/MfjEVIVgjQ9ZOQ+CFr0ZPOMw91ayq5Gvgcens5PZE8ig4BlqQISmRb38qq1kK3CwyCn6na6LPvIdkjhrTSH6tP2XwAsTbVNW7r+sKxDHNVV4Ylj/80cl6RHNJdCoY4LQ8U0XH87PGsk2XxJqmDyrte7z4aJEIC0Kk8kRblAilHPAtu8Xct9Q3DCjVnl0S97gR+6DjvwyExqNBIlNWYuDrw+f+Q5pkgYR07zPM7ksq6E9Bdo4FK4UAwLjD489dkd5RefcuEkj+3jBU1HfSL3uAGEmVEvD7jfxuDna1W45Pe95OPs+ph7eYz6o2A35CKPLq0mfzPts6Ow/dSdfveYh5AyGoyJqpLYDPKXqUYVVeP/aowGpqv6NxM9OoCkOTVF+vkoJyyJ8UmRo+DUWN26vHm1XxuOYz4yY604jSafDhmbCYXYN+MWtM1jjwZZs/TG3LVrgFJfm2sCobwqqqkL7WGuc/OmFIxCv/4sIPXlxJzLJQ0LjLf8FLfm8A6X9F0Di6nJqW3Qr4zZIBUBDTnYnkWs/2v+aNga2hdYUenwyAHw8nTITLBmNZau3Mgap8flJDrVKBK7nVDGdEH8D9KWyDLiSakdfhzpHDHYln4tRY0dM6D/cBfHMICrtBVibSzeo512AT3yIAwVl/qwn8uU0/G12gXCPSdoOqCrORUP0RAd8Z2fO0NXobwwFYv7t5mr0lOBqaOvvmUBuZBAGaTjtTdVzRZn7DFyWrI8V/OY78N2LnyL92xDpoudgkhQGaj6TOHcdfYkjUfdmHhseH8g8kxJyyaoq2zH++0tPQcJA=='
}

VESSEL_DETAILS_URL = 'https://www.iattc.org//VesselRegister/VesselDetails.aspx'

def search_by_name(name):
    request_data = SEARCH_REQUEST_DATA_TEMPLATE
    request_data['VesselName'] = name

    response = requests.post(SEARCH_URL, data=request_data)
    search_results = parse_search_results(response.text)
    return search_results

def parse_search_results(html):
    soup = BeautifulSoup(html, 'html.parser')
    html_search_results = soup.find_all('td', class_='VesselNameLink')

    search_results = []
    for result in html_search_results:
        vessel_name = result.find('a').text
        vessel_link = result.find('a').attrs['href']
        number_matches = re.search(r'VesNo=(\d*)&', vessel_link)
        vessel_number = number_matches.groups()[0]
        search_results.append({'vessel_name': vessel_name, 'vessel_number': vessel_number})

    return search_results

def get_vessel_details(vessel_number):
    response = requests.get(VESSEL_DETAILS_URL, params={'VesNo': vessel_number, 'Lang': 'ENG'})
    soup = BeautifulSoup(response.text, 'html.parser')

    vessel_name = soup.find('td', class_='VesselNameTitle').text
    details_table = soup.find('table', id='DetailsTable')

    field_map = {
        'Flag: ': 'flag',
        'Gear: ': 'gear',
        'Port of registration:': 'port',
        'Gross tonnage: ': 'gross-tonnage'
    }

    results = { v: None for k, v in field_map.items() }

    for child in details_table.children:
        try:
            row_class = child.td.text
            if row_class in field_map:
                results[field_map[row_class]] = child.td.nextSibling.text
        except AttributeError:
            pass

    return results
