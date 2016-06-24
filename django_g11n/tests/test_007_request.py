"main testing module"
from django.test import TestCase, Client

# Create your tests here.
class VariousTestCase(TestCase):
    "main test case"
    # pylint: disable=missing-docstring, no-member, invalid-name, no-self-use
    def test_001(self):
        client = Client()
        client.get('', REMOTE_ADDR='109.74.193.121')


if __name__ == '__main__': # pragma: no cover
    # pylint: disable=wrong-import-position
    import django
    django.setup()
    django.core.management.call_command('test')

