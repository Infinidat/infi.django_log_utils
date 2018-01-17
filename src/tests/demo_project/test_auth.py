from test_base import BaseTestCase
from testfixtures import LogCapture


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
            l.check(('auth', 'WARNING', "Invalid login attempt: {'username': u'admin', 'password': '********************'}"))
