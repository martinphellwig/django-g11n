'''
Created on 23 Jun 2016

@author: martin
'''
import json
import zipfile
import ipaddress
import os
from io import StringIO
import requests



def ip_to_hex(ip_address):
    "Convert IP to hex."
    address = ipaddress.ip_address(ip_address)
    hex_address = hex(int(address))[2::].zfill(32)
    return hex_address


def make_data_path(name):
    "Make the data path."
    _ = os.path.dirname(os.path.abspath(__file__))
    _ = os.path.join(_, 'data', name)
    return _


def setup_ipranges():
    "Setup some ip ranges"
    from ..tools import models

    from_ip = ip_to_hex("1.0.0.0")
    till_ip = ip_to_hex("239.255.255.255")
    model = models.ALL['IPRange']
    model.objects.create(
        identifier='all', regional_nic='XX', tld='XX', ipv=4,
        network_hex=from_ip, broadcast_hex=till_ip)


def bulk_json_insert(data):
    "Bulk insert json"
    tmp = dict()
    data = json.loads(data)
    from django.apps import apps
    from ..tools import models
    for item in data:
        model_name = item['model']
        model = apps.get_model(*model_name.rsplit('.', 1))
        fields = item['fields']
        fields['id'] = item['pk']

        for key in list(fields):
            # pylint: disable=protected-access
            field = model._meta.get_field(key)
            if field.is_relation:
                fields[key+'_id'] = fields.pop(key)

        if model not in tmp:
            tmp[model] = list()

        tmp[model].append(model(**fields))

    for model in list(tmp.keys()):
        model.objects.bulk_create(tmp[model])


def setup_ipranges_all():
    "Setup all ip's."
    from ..tools import models
    path = make_data_path('country.json')
    with open(path, 'r') as file_open:
        data = ''.join(file_open.readlines())
        bulk_json_insert(data)

    name = 'iprange_2016_06_23.json.zip'
    path = make_data_path(name)
    unzip = zipfile.ZipFile(path)
    data = unzip.read(name.rsplit('.', 1)[0]).decode('UTF-8')
    bulk_json_insert(data)
    

def call_command_returns(*args, **kwargs):
    "call command but wich returns the output."
    from django.core.management import call_command
    stdout = StringIO()
    kwargs['stdout'] = stdout
    call_command(*args, **kwargs)
    return stdout.getvalue().strip()


class RequestsMock(object):
    "Mock the request module"
    def __init__(self):
        self._restores = dict()
        self._response = dict()
        self.text = None

    def add_response_text_from_data(self, url, file_name):
        "If url is called the content of file_name is returned"
        _ = make_data_path(file_name)
        with open(_, 'r') as file_open:
            self._response[url] = ''.join(file_open.readlines())

    def insert_mock(self):
        "Insert the mock"
        self._restores['get'] = requests.get
        requests.get = self.get

    def remove_mock(self):
        "Remove the mock"
        requests.get = self._restores['get']

    def get(self, url):
        "Mocked request get function"
        self.text = self._response[url]
        return self


def setup_currencies():
    "Insert all currencies"
    from django.core.management import call_command
    call_command('update_countries')

    mock = RequestsMock()
    url = 'http://www.currency-iso.org/dam/downloads/lists/list_one.xml'
    file_name = 'list_one.xml'
    mock.add_response_text_from_data(url, file_name)
    mock.insert_mock()
    mock.remove_mock()
    call_command('update_currencies')

