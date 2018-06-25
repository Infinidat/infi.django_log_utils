from .test_base import BaseTestCase
from testfixtures import LogCapture


class AuthTestCase(BaseTestCase):

    def test_login_and_logout(self):
        r = self.login()
        self.assertEquals(r['X-User'], 'admin@example.com')
        r = self.logout()
        self.assertEquals(r['X-User'], '-')
