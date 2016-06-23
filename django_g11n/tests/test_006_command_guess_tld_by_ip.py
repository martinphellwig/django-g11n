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
        TestCase.setUp(self)
        from django.core.management import call_command
        self.call = common.call_command_returns
        #
        common.setup_ipranges()

    def tearDown(self):
        TestCase.tearDown(self)

    def test_001_insert(self):
        expected = 'XX'
        actually = self.call('guess_tld_by_ip', '192.168.0.1')
        self.assertEqual(expected, actually)


if __name__ == '__main__': # pragma: no cover
    # pylint: disable=wrong-import-position
    import django
    django.setup()
    django.core.management.call_command('test')

