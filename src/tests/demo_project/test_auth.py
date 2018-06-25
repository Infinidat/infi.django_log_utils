from .test_base import BaseTestCase
from testfixtures import LogCapture
import sys


PY3 =  (sys.version_info > (3, 0))


class AuthTestCase(BaseTestCase):

    def test_login_and_logout(self):
        with LogCapture('auth') as l:
            self.login()
            self.logout()
            l.check(
                ('auth', 'INFO', "User admin@example.com logged in from ip 127.0.0.1"),
                ('auth', 'INFO', "User admin@example.com logged out from ip 127.0.0.1")
            )

    def test_invalid_login(self):
        with LogCapture('auth') as l:
            self.client.post('/admin/login/', {'username': self.MOCK_USERNAME, 'password': 'wrong'})
            u = '' if PY3 else 'u'
            l.check(('auth', 'WARNING', "Invalid login attempt: {'password': '********************', 'username': %s'admin'}" % u))
