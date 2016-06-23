"main testing module"
from django.test import TestCase

# Create your tests here.
class UpdateCurrenciesTestCase(TestCase):
    "main test case"
    # pylint: disable=missing-docstring, no-member, invalid-name
    @classmethod
    def setUpClass(cls):
        returns = super(UpdateCurrenciesTestCase, cls).setUpClass()
        return returns

    def setUp(self):
        returns = TestCase.setUp(self)
        from django.core.management import call_command
        self._call_command = call_command
        self._call_command('update_countries')

        from . import common

        self.mock = common.RequestsMock()
        url = "http://www.currency-iso.org/dam/downloads/lists/list_one.xml"
        file_name = 'list_one.xml'

        self.mock.add_response_text_from_data(url, file_name)
        self.mock.insert_mock()

        return returns

    def tearDown(self):
        TestCase.tearDown(self)
        self.mock.remove_mock()

    def test_001_insert(self):
        self._call_command('update_currencies')
        # Calling twice, as the second time it should exclude it.
        self._call_command('update_currencies')



if __name__ == '__main__': # pragma: no cover
    # pylint: disable=wrong-import-position
    import django
    django.setup()
    django.core.management.call_command('test')

