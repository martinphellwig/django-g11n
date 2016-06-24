"main testing module"
from django.test import TestCase

# Create your tests here.
class GuessTldByIpTestCase(TestCase):
    "main test case"
    # pylint: disable=missing-docstring, no-member, invalid-name
    @classmethod
    def setUpClass(cls):
        returns = super(GuessTldByIpTestCase, cls).setUpClass()
        return returns

    def setUp(self):
        from . import common
        from ..tools import models
        TestCase.setUp(self)
        from django.core.management import call_command
        self.call = common.call_command_returns
        print('# Setting up IP ranges, this will take a while.')
        common.setup_ipranges_all()
        print('# ... done.')
        common.setup_currencies()

    def tearDown(self):
        TestCase.tearDown(self)

    def test_001_guess(self):
        expected = 'GB'
        actually = self.call('guess_tld_by_ip',  '109.74.193.121')
        self.assertEqual(expected, actually)

        provided = 'GB'
        expected = 'GBP'
        actually = self.call('currency_by_tld', provided)
        self.assertEqual(expected, actually)




if __name__ == '__main__': # pragma: no cover
    # pylint: disable=wrong-import-position
    import django
    django.setup()
    django.core.management.call_command('test')

