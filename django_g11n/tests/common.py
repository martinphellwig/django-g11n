'''
Created on 23 Jun 2016

@author: martin
'''
import ipaddress
from io import StringIO


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

