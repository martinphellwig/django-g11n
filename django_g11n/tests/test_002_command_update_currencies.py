"main testing module"
from django.test import TestCase

class MockToolsCurrency(object):
    "Mock the currency module"
    def __init__(self):
        self._data = [
            ['AFGHANISTAN', '971', 'Afghani', 'AFN', '2', False, True, True],
            ['IMAGINARY', '999', 'Ima Dollar', 'IMG', '2', False, True, True]]

    def get(self):
        "Mock the get function"
        return self._data

# Create your tests here.
class UpdateCurrenciesTestCase(TestCase):
    "main test case"
    # pylint: disable=missing-docstring, no-member, invalid-name
    @classmethod
    def setUpClass(cls):
        returns = super(UpdateCurrenciesTestCase, cls).setUpClass()
        return returns

    def setUp(self):
        TestCase.setUp(self)
        from django.core.management import call_command
        self._call_command = call_command
        self._call_command('update_countries')

        from ..management.commands import update_currencies
        self._update_currencies = update_currencies
        self._restore = update_currencies.currency

        update_currencies.currency = MockToolsCurrency()

    def tearDown(self):
        TestCase.tearDown(self)
        self._update_currencies.currency = self._restore

    def test_001_insert(self):
        self._call_command('update_currencies')
        # Calling twice, as the second time it should exclude it.
        self._call_command('update_currencies')
        



if __name__ == '__main__': # pragma: no cover
    # pylint: disable=wrong-import-position
    import django
    django.setup()
    django.core.management.call_command('test')

