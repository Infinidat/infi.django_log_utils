# -*- coding: utf-8 -*-

from test_base import BaseTestCase
from testfixtures import LogCapture
import json


class ReqDataTestCase(BaseTestCase):

    def test_anonymous_user(self):
        with LogCapture('reqdata') as l:
            self.login()
            l.check(
                ('reqdata', 'INFO', '(Anonymous) POST /admin/login/\n    username = "admin"\n    password = "********************"'),
            )

    def test_logged_in_user(self):
        self.login()
        with LogCapture('reqdata') as l:
            self.client.post('/admin/auth/group/add/', {'name': 'aaa'})
            l.check(
                ('reqdata', 'INFO', '(admin@example.com) POST /admin/auth/group/add/\n    name = "aaa"')
            )

    def test_json(self):
        with LogCapture('reqdata') as l:
            self.client.post('/admin/auth/group/add/', json.dumps({'name': 'aaa'}), content_type='application/json')
            l.check(
                ('reqdata', 'INFO', '(Anonymous) POST /admin/auth/group/add/\n    {\n        "name": "aaa"\n    }')
            )

    def test_json_unicode(self):
        with LogCapture('reqdata') as l:
            self.client.post('/admin/auth/group/add/', json.dumps({'name': u'דוד'}), content_type='application/json')
            l.check(
                ('reqdata', 'INFO', u'(Anonymous) POST /admin/auth/group/add/\n    {\n        "name": "דוד"\n    }')
            )

    def test_invalid_json(self):
        with LogCapture('reqdata') as l:
            self.client.post('/admin/auth/group/add/', u'{ג' + json.dumps({'name': 'aaa'}), content_type='application/json')
            l.check(
                ('reqdata', 'INFO', u'(Anonymous) POST /admin/auth/group/add/\n    {ג{"name": "aaa"}')
            )

    def test_raw(self):
        with LogCapture('reqdata') as l:
            self.client.post('/admin/auth/group/add/', 'aaa\nbbb', content_type='text/plain')
            l.check(
                ('reqdata', 'INFO', '(Anonymous) POST /admin/auth/group/add/\n    aaa\n    bbb')
            )

    def test_raw_unicode(self):
        with LogCapture('reqdata') as l:
            self.client.post('/admin/auth/group/add/', u'אבגד', content_type='text/plain')
            l.check(
                ('reqdata', 'INFO', u'(Anonymous) POST /admin/auth/group/add/\n    אבגד')
            )
