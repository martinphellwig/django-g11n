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

Of course you most likely want to use it programmatically, for that have a look
at django_g11n.tools.by_request, this has the following functions:

- ipaddress(request)
- guess_country(request)
- guess_language(request)
- guess_currency(request)
- guess_country_language_currency(request)

The will return data as you may guess from the functions name.


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