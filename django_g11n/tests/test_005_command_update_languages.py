"main testing module"
from django.test import TestCase


# Create your tests here.
class UpdateLanguageCountriesTestCase(TestCase):
    "main test case"
    # pylint: disable=missing-docstring, no-member, invalid-name
    @classmethod
    def setUpClass(cls):
        returns = super(UpdateLanguageCountriesTestCase, cls).setUpClass()
        return returns

    def setUp(self):
        TestCase.setUp(self)
        from django.core.management import call_command
        self.call_command = call_command

    def tearDown(self):
        TestCase.tearDown(self)

    def test_001_insert(self):
        #self.call_command('update_countries')
        #self.call_command('update_languages')
        #self.call_command('update_language_countries')
        pass


if __name__ == '__main__': # pragma: no cover
    # pylint: disable=wrong-import-position
    import django
    django.setup()
    django.core.management.call_command('test')

