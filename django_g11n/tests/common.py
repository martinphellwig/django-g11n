'''
Created on 23 Jun 2016

@author: martin
'''
import os
import ipaddress
from io import StringIO
import requests


def ip_to_hex(ip_address):
    "Convert IP to hex."
    address = ipaddress.ip_address(ip_address)
    hex_address = hex(int(address))[2::].zfill(32)
    return hex_address


def setup_ipranges():
    "Setup some ip ranges"
    from ..tools import models

    from_ip = ip_to_hex("1.0.0.0")
    till_ip = ip_to_hex("239.255.255.255")
    model = models.ALL['IPRange']
    model.objects.create(
        identifier='all', regional_nic='XX', tld='XX', ipv=4,
        network_hex=from_ip, broadcast_hex=till_ip)

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
        _ = os.path.dirname(os.path.abspath(__file__))
        _ = os.path.join(_, 'data', file_name)
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



