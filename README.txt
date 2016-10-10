.. image:: https://img.shields.io/codeship/550d9e60-1630-0134-9ad4-2e1718fe265e/default.svg
   :target: https://bitbucket.org/hellwig/django-g11n
.. image:: https://coveralls.io/repos/bitbucket/hellwig/django-g11n/badge.svg?branch=default
   :target: https://coveralls.io/bitbucket/hellwig/django-g11n?branch=default
.. image:: https://img.shields.io/pypi/v/django-g11n.svg
   :target: https://pypi.python.org/pypi/django-g11n/
.. image:: https://img.shields.io/badge/Donate-PayPal-blue.svg
   :target: https://paypal.me/MartinHellwig
.. image:: https://img.shields.io/badge/Donate-Patreon-orange.svg
   :target: https://www.patreon.com/hellwig
   

####################
Django Globalisation
####################

What is it?
===========

- A Django app that helps in with internationalisation and localisation.

What problem does it solve?
===========================

- Guess the origin country of the request.
- Return the currency a country uses.
- Fetch the language code.
- Does not use commercial databases, uses original data sources.
- Both IPv4 and IPv6.
- Has a reasonable model layout.

How do I install it?
====================
::

  $ pip install django-g11n

Use `django-integrator <https://bitbucket.org/hellwig/django-integrator>`_  to
integrate this app to your django instance, alternatively you can do it the
common manual way.


How do I use it?
================
::

  # To fill initial data use the command
  $ python manage.py g11n_setup
  # To guess someones IP
  $ python manage.py guess_tld_by_ip 8.8.8.8
  # To find out what the currency is most likely associated with an tld
  $ python manage.py currency_by_tld gb
  #

Of course you most likely want to use it via a request instance, for that have a
look at django_g11n.tools.by_request, this has the following functions:

- ipaddress(request)
- guess_country(request)
- guess_language(request)
- guess_currency(request)
- guess_country_language_currency(request)

The will return data as you may guess from the functions name.

However since all the data is inside models, it is also usuable in an
interactive shell session like so:

.. sourcecode:: python
		
  In [1]: from django_g11n.tools.fetch import iprange_by_ip
  
  In [2]: iprange = iprange_by_ip('194.60.62.36')
  
  In [3]: iprange.__dict__
  Out[3]: 
  {'_state': <django.db.models.base.ModelState at 0x7f581dd9f9e8>,
   'broadcast_hex': '000000000000000000000000c23c3fff',
   'dts_delete': None,
   'dts_insert': datetime.datetime(2016, 10, 10, 10, 19, 55, 241150, tzinfo=<UTC>),
   'dts_update': None,
   'id': 58935,
   'identifier': 'rigb4_0_24_c23c3fff_0_24_c23c0000',
   'ipv': 4,
   'network_hex': '000000000000000000000000c23c0000',
   'reference_id': 235,
   'regional_nic': 'ripencc',
   'tld': 'GB'}
  
  In [4]: country = iprange.reference
  
  In [5]: country.__dict__
  Out[5]: 
  {'_state': <django.db.models.base.ModelState at 0x7f581dd9fda0>,
   'code_2': 'GB',
   'code_3': 'GBR',
   'dts_delete': None,
   'dts_insert': datetime.datetime(2016, 10, 10, 10, 18, 31, 274177, tzinfo=<UTC>),
   'dts_update': None,
   'id': 235,
   'iso3166': True,
   'numeric': 826,
   'obsolete': False}
  
  In [6]: country.languagecountry_set.all()
  Out[6]: [<LanguageCountry: en-GB>]
  
  In [7]: language_country = country.languagecountry_set.all()[0]
  
  In [8]: language_country.language.__dict__
  Out[8]: 
  {'_state': <django.db.models.base.ModelState at 0x7f581dd3cba8>,
   'bibliographic': 'eng',
   'code_a2': 'en',
   'dts_delete': None,
   'dts_insert': datetime.datetime(2016, 10, 10, 10, 20, 1, 110024, tzinfo=<UTC>),
   'dts_update': None,
   'english': 'English',
   'french': 'anglais',
   'id': 123,
   'iso639_2': True,
   'obsolete': False,
   'terminologic': ''}
  
  In [9]: country.countryname_set.all()
  Out[9]: [<CountryName: United Kingdom>, <CountryName: United Kingdom of Great Britain and Northern Ireland>]
  
  In [10]: country.countryname_set.all()[1].__dict__
  Out[10]: 
  {'_country_cache': <Country: GB>,
   '_state': <django.db.models.base.ModelState at 0x7f581dd43d30>,
   'country_id': 235,
   'default': False,
   'dts_delete': None,
   'dts_insert': datetime.datetime(2016, 10, 10, 10, 18, 31, 337353, tzinfo=<UTC>),
   'dts_update': None,
   'id': 248,
   'iso3166': True,
   'language_id': 42,
   'value': 'United Kingdom of Great Britain and Northern Ireland'}
  
  In [11]: country.currency_set.all()
  Out[11]: [<Currency: GBP 826>]
  
  In [12]: country.currency_set.all()[0].__dict__
  Out[12]: 
  {'_reference_cache': <Country: GB>,
   '_state': <django.db.models.base.ModelState at 0x7f581dd49940>,
   'code': 'GBP',
   'country': 'UNITED KINGDOM OF GREAT BRITAIN AND NORTHERN IRELAND (THE)',
   'decimals': 2,
   'default': True,
   'dts_delete': None,
   'dts_insert': datetime.datetime(2016, 10, 10, 10, 18, 31, 670707, tzinfo=<UTC>),
   'dts_update': None,
   'id': 754,
   'is_fund': False,
   'iso4217': True,
   'name': 'Pound Sterling',
   'numeric': 826,
   'reference_id': 235}
  
  In [13]: country.region_set.all()
  Out[13]: [<Region: 826 United Kingdom of Great Britain and Northern Ireland>]
  
  In [14]: region = country.region_set.all()[0]
  
  In [15]: region.__dict__
  Out[15]: 
  {'_reference_cache': <Country: GB>,
   '_state': <django.db.models.base.ModelState at 0x7f581dd4e4a8>,
   'dts_delete': None,
   'dts_insert': datetime.datetime(2016, 10, 10, 10, 20, 1, 369095, tzinfo=<UTC>),
   'dts_update': datetime.datetime(2016, 10, 10, 10, 20, 5, 295071, tzinfo=<UTC>),
   'english': 'United Kingdom of Great Britain and Northern Ireland',
   'id': 116,
   'numeric': '826',
   'obsolete': False,
   'reference_id': 235,
   'unsd_m49': True}
  
  In [16]: def print_regions(region):
     ....:     while True:
     ....:         print(region.numeric, ' - ', region.english)
     ....:         chains = region.chains_region_is_lower.all()
     ....:         if chains.count() == 0:
     ....:             break
     ....:         region = chains[0].upper
     ....:         
  
  In [17]: print_regions(region)
  826  -  United Kingdom of Great Britain and Northern Ireland
  154  -  Northern Europe
  150  -  Europe
  001  -  World
  
  In [18]: 

As you can see above that most models refer back to the Country model via
the 'reference' field, this is done because most tables are filled from outside
source. For country, language and currencies we use ISO, for regions we use
UN-SD M49 and the ipranges are downloaded from the regional NIC's.
Since all of them have slightly different representation of the country names,
the country names in each table has been preserved on import and after import
the system tries to find the appropriate foreign relationship to the Country
table.

What license is this?
=====================
Two-clause BSD


How can I get support?
======================
Please use the repo's bug tracker to leave behind any questions, feedback,
suggestions and comments. I will handle them depending on my time and what looks
interesting. If you require guaranteed support please contact me via
e-mail so we can discuss appropriate compensation.


Signing Off
===========
Is my work helpful or valuable to you? You can repay me by donating via:

https://paypal.me/MartinHellwig

.. image:: https://img.shields.io/badge/PayPal-MartinHellwig-blue.svg
  :target: https://paypal.me/MartinHellwig
  :alt: Donate via PayPal.Me
  :scale: 120 %

-or-

https://www.patreon.com/hellwig

.. image:: https://img.shields.io/badge/Patreon-hellwig-orange.svg
  :target: https://www.patreon.com/hellwig
  :alt: Donate via Patreon
  :scale: 120 %


Thank you!