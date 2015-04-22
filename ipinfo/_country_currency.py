"""
Fetch data to create a country to currency table
"""

URL_CURRENCY="http://www.currency-iso.org/dam/downloads/table_a1.xml"
URL_COUNTRY="http://en.wikipedia.org/w/index.php?title=ISO_3166-2&action=edit"

import requests
from io import StringIO
from xml.etree import ElementTree

CURRENCY_OVERRIDE = {
    'EL SALVADOR':'USD',
    'BHUTAN':'BTN',
    'CUBA':'CUP',
    'HAITI':'HTG',
    'BOLIVIA, PLURINATIONAL STATE OF':'BOB',
    'PANAMA':'PAB',
    'SWITZERLAND':'CHF',
    'NAMIBIA':'NAD',
    'UNITED STATES':'USD',
    'URUGUAY':'UYU',
    'LESOTHO':'LSL',
    'COLOMBIA':'COP',
    'CHILE':'CLP',
    'MEXICO':'MXN',
    'EUROPE':'EUR'}

def _fetch_extract_country(url=URL_COUNTRY):
    "Get a list of country names and their 2 letter abbreviation"
    response = requests.get(url)
    lookup = dict()
    for line in response.text.split("[[ISO 3166-2:"):
        if '||' in line:
            columns = line.split('||')
            country_code = columns[0]
            country_code = country_code.split('|')[0]
            country_names = columns[1]
            country_names = country_names.split('|')

            tmp = list()
            for item in country_names:
                for value in ['[', ']', '}']:
                    item = item.replace(value, '')
                    item = item.strip()

                if '-->' in item:
                    item = item.split('-->')[1]

                if '&lt;' in item:
                    item = item.split('&lt;')[0]

                append_filter = ['{{', '=']
                set_filter = False
                for value in append_filter:
                    if value in item:
                        set_filter = True
                        break

                if not set_filter:
                    tmp.append(item)

            for key in tmp:
                key = key.upper()
                lookup[key] = country_code
                if ',' in key:
                    one, two = key.split(',', 1)
                    one = one.strip()
                    two = two.strip()
                    key = two + ' ' + one
                    lookup[key] = country_code

    lookup['EUROPEAN UNION'] = 'EU'
    lookup['EUROPE'] = 'EU'
    return lookup

def _replace(item, replacers):
    "Using replacers old/new values replace these in item."
    item = item.strip()
    item = item.upper()

    for old, new in replacers:
        item = item.replace(old, new)
    return item


def _fetch_parse_currency(url=URL_CURRENCY):
    "Fetch currency and parse it."
    response = requests.get(url)
    response.encoding = 'UTF-8'
    xml = StringIO()
    xml.write(response.text)

    xml.seek(0)
    tree = ElementTree.parse(xml)

    lookup = CURRENCY_OVERRIDE.copy()

    for entry in tree.getiterator():
        if entry.tag != 'CcyNtry':
            continue

        name = entry.find('CtryNm')
        abbr = entry.find('Ccy')

        if name == None or abbr == None:
            continue

        if name.text in lookup:
            continue

        replacements = [['\n', ''],
                        ['’', "'"],
                        [' (BRITISH)', ', BRITISH'],
                        [' (U.S.)', ', U.S.'],
                        ['CONGO, ', 'CONGO, THE ']]

        name = _replace(name.text, replacements)
        abbr = _replace(abbr.text, replacements)

        if name.startswith('ZZ'):
            continue

        do_continue = False

        for test in ['(IMF)', 'SUCRE', 'BANK']:
            if test in name:
                do_continue = True
                break

        if do_continue:
            continue

        lookup[name] = abbr

    return lookup


def fetch_cctld_currency():
    "Return a dictionary where key is a cctld and value is its currency."
    dic = dict()
    country_code = _fetch_extract_country()
    country_currency = _fetch_parse_currency()

    for country, currency in country_currency.items():
        code = country_code[country]
        dic[code] = currency

    return dic

