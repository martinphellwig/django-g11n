"main testing module"
from django.test import TestCase

# pylint: disable=too-few-public-methods
class MockToolsLanguage(object):
    "Mock the language module"
    def __init__(self):
#     - bibliographic code
#     - terminologic code
#     - alpha-2 code
#     - Name in English
#     - Name in French.
#     - ISO-639-2 boolean (False if it is a local addition)
        self._data = [
            ['aar','','aa','Afar','afar', False],
        ]

    def get(self):
        "Mock the get function"
        return self._data

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
        self.restore = update_languages.language

        self.update.language = MockToolsLanguage()

    def tearDown(self):
        TestCase.tearDown(self)
        self.update.language = self.restore

    def test_001_insert(self):
        self.call_command('update_languages')
        # Calling twice, as the second time it should exclude it.
        #pylint: disable=protected-access
        self.update.language._data = []
        self.call_command('update_languages')


if __name__ == '__main__': # pragma: no cover
    # pylint: disable=wrong-import-position
    import django
    django.setup()
    django.core.management.call_command('test')

