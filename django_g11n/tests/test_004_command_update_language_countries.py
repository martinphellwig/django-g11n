"main testing module"
import os
from django.test import TestCase

# pylint: disable=too-few-public-methods
class MockLibRequests(object):
    "Mock the language module"
    def __init__(self):
        _ = os.path.dirname(os.path.abspath(__file__))
        self.data = os.path.join(_, 'data', 'ISO-639-2_utf-8.txt')
        self.url = None
        self.text = None
        self.partial = False

    def get(self, url):
        "GET request."
        self.url = url
        with open(self.data, 'r') as file_open:
            _ = file_open.readlines()
            self.text = ''.join(_)

        return self


# Create your tests here.
class UpdateLanguagesTestCase(TestCase):
    "main test case"
    # pylint: disable=missing-docstring, no-member, invalid-name
    @classmethod
    def setUpClass(cls):
        returns = super(UpdateLanguagesTestCase, cls).setUpClass()
        return returns

    def setUp(self):
        TestCase.setUp(self)
        from django.core.management import call_command
        self.call_command = call_command

        from ..management.commands import update_languages
        self.update = update_languages
        self.restore = update_languages.language.requests

        self.update.language.requests = MockLibRequests()

    def tearDown(self):
        TestCase.tearDown(self)
        self.update.language.requests = self.restore

    def test_001_update_language(self):
        self.call_command('update_languages')
        # Calling twice, as the second time it should exclude it.
        #pylint: disable=protected-access, undefined-variable
        #
        from ..tools import models
        models.ALL['Language'].objects.create(
            code_a2='**', english='Double Star', french='Astérisque Double')
        self.update.language.requests.partial = True
        self.call_command('update_languages')

    def test_002_update_language_country(self):
        self.call_command('update_countries')
        self.call_command('update_languages')
        self.call_command('update_language_countries')
        #
        from ..tools import models
        models.ALL['LanguageCountrySpecifier'].objects.create(
            short='??', value='Question Marks', override=False)
        model = models.ALL['LanguageCountry']()
        model.language_id=4
        model.country_id=16
        model.specifier_id=1
        model.override=False
        model.save()
        self.call_command('update_language_countries')


if __name__ == '__main__': # pragma: no cover
    # pylint: disable=wrong-import-position
    import django
    django.setup()
    django.core.management.call_command('test')

