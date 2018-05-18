import random
import string
import time

from falcon import testing
from sqlalchemy import (
    create_engine,
    text,
)
from sqlalchemy.orm import sessionmaker

from demo import config
from tests import config_test
# This stays here to override the connection string
config.CONN_STR = config_test.CONN_STR

from db_setup import set_er_up
from demo.app import api


class MyTestCase(testing.TestCase):
    def setUp(self):
        super(MyTestCase, self).setUp()
        self.app = api
        set_er_up(conn_str=config_test.CONN_STR)
        self.session = sessionmaker(bind=create_engine(config_test.CONN_STR))()

    def tearDown(self):
        self.session.close()

    def check_account_created(self, username, exprects_success=True):
        """
        Helper method to check if an account was created
        """
        results = self.session.execute(
            text("SELECT * from users where username = :username;"),
            params=dict(username=username),
        ).fetchall()

        if exprects_success:
            self.assertEqual(len(results), 1)
        else:
            self.assertEqual(len(results), 0)

    def generate_username(self):
        """
        Helper method to generate a unique username
        """
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(18))


class TestRootAPI(MyTestCase):
    def test_get_message(self):
        doc = {
            "msg": "hello world!"
        }

        result = self.simulate_get('/')
        self.assertEqual(result.json, doc)


class TestRegisterAPI(MyTestCase):
    def test_register_pass(self):
        username = self.generate_username()
        doc = {
            "msg": "hello %s!" % username
        }
        result = self.simulate_post(
            '/register',
            json={
                "username": username,
                "password": "password123"
            }
        )
        self.assertEqual(result.json, doc)
        self.assertEqual(result.status_code, 201)
        self.check_account_created(username=username)


    def test_register_missing_password(self):
        print 'Do not send field at all'
        username = self.generate_username()
        result = self.simulate_post(
            '/register',
            json={
                "username": username,
            }
        )
        self.assertEqual(result.status_code, 400)
        self.assertTrue('errors' in result.json)
        self.assertEqual(len(result.json['errors']), 1)
        self.assertEqual(result.json['errors'][0]['field'], 'password')
        self.check_account_created(username=username, exprects_success=False)

        print 'Send null value'
        username = self.generate_username()
        result = self.simulate_post(
            '/register',
            json={
                "username": username,
                "password": None,
            }
        )
        self.assertEqual(result.status_code, 400)
        self.assertTrue('errors' in result.json)
        self.assertEqual(len(result.json['errors']), 1)
        self.assertEqual(result.json['errors'][0]['field'], 'password')
        self.check_account_created(username=username, exprects_success=False)

        print 'Send empty string'
        username = self.generate_username()
        result = self.simulate_post(
            '/register',
            json={
                "username": username,
                "password": "",
            }
        )
        self.assertEqual(result.status_code, 400)
        self.assertTrue('errors' in result.json)
        self.assertEqual(len(result.json['errors']), 1)
        self.assertEqual(result.json['errors'][0]['field'], 'password')
        self.check_account_created(username=username, exprects_success=False)

        print 'Send whitespace string'
        username = self.generate_username()
        result = self.simulate_post(
            '/register',
            json={
                "username": username,
                "password": "        ",
            }
        )
        self.assertEqual(result.status_code, 400)
        self.assertTrue('errors' in result.json)
        self.assertEqual(len(result.json['errors']), 1)
        self.assertEqual(result.json['errors'][0]['field'], 'password')
        self.check_account_created(username=username, exprects_success=False)

        print 'Send whitespace string - all tabs'
        username = self.generate_username()
        result = self.simulate_post(
            '/register',
            json={
                "username": username,
                "password": "\t\t\t\t",
            }
        )
        self.assertEqual(result.status_code, 400)
        self.assertTrue('errors' in result.json)
        self.assertEqual(len(result.json['errors']), 1)
        self.assertEqual(result.json['errors'][0]['field'], 'password')
        self.check_account_created(username=username, exprects_success=False)


    def test_register_missing_username(self):
        print 'Do not send field at all'
        result = self.simulate_post(
            '/register',
            json={
                "password": "password1234"
            }
        )
        self.assertEqual(result.status_code, 400)
        self.assertTrue('errors' in result.json)
        self.assertEqual(len(result.json['errors']), 1)
        self.assertEqual(result.json['errors'][0]['field'], 'username')

        print 'Send null value'
        result = self.simulate_post(
            '/register',
            json={
                "username": None,
                "password": "password1234"
            }
        )
        self.assertEqual(result.status_code, 400)
        self.assertTrue('errors' in result.json)
        self.assertEqual(len(result.json['errors']), 1)
        self.assertEqual(result.json['errors'][0]['field'], 'username')

        print 'Send whitespace string'
        result = self.simulate_post(
            '/register',
            json={
                "username": "         ",
                "password": "password1234"
            }
        )
        self.assertEqual(result.status_code, 400)
        self.assertTrue('errors' in result.json)
        self.assertEqual(len(result.json['errors']), 1)
        self.assertEqual(result.json['errors'][0]['field'], 'username')

        print 'Send whitespace string -- all tabs'
        result = self.simulate_post(
            '/register',
            json={
                "username": "\t\t\t",
                "password": "password1234"
            }
        )
        self.assertEqual(result.status_code, 400)
        self.assertTrue('errors' in result.json)
        self.assertEqual(len(result.json['errors']), 1)
        self.assertEqual(result.json['errors'][0]['field'], 'username')


    def test_register_password_validation(self):
        print 'Business rule: passwords must be at least 10 characters long'
        password = "1234567890"
        self.assertEqual(len(password), 10)
        username = self.generate_username()
        doc = {
            "msg": "hello %s!" % username
        }
        result = self.simulate_post(
            '/register',
            json={
                "username": username,
                "password": password
            }
        )
        self.assertEqual(result.json, doc)
        self.assertEqual(result.status_code, 201)
        self.check_account_created(username=username)

        print 'Business rule: passwords must be at least 10 characters long'
        password = "12345"
        self.assertLess(len(password), 10)
        username = self.generate_username()
        result = self.simulate_post(
            '/register',
            json={
                "username": username,
                "password": password
            }
        )
        self.assertEqual(result.status_code, 400)
        self.assertTrue('errors' in result.json)
        self.assertEqual(len(result.json['errors']), 1)
        self.assertEqual(result.json['errors'][0]['field'], 'password')

        print 'Business rule: passwords must be 20 or less characters long'
        password = "12345678901234567890"
        self.assertEqual(len(password), 20)
        username = self.generate_username()
        doc = {
            "msg": "hello %s!" % username
        }
        result = self.simulate_post(
            '/register',
            json={
                "username": username,
                "password": password
            }
        )
        self.assertEqual(result.json, doc)
        self.assertEqual(result.status_code, 201)
        self.check_account_created(username=username)

        print 'Business rule: passwords must be 20 or less characters long'
        password = "1234567890123456789012345"
        self.assertGreater(len(password), 20)
        username = self.generate_username()
        result = self.simulate_post(
            '/register',
            json={
                "username": username,
                "password": password
            }
        )
        self.assertEqual(result.status_code, 400)
        self.assertTrue('errors' in result.json)
        self.assertEqual(len(result.json['errors']), 1)
        self.assertEqual(result.json['errors'][0]['field'], 'password')


    def test_register_username_validation(self):
        print 'Business rule: usernames must be at least 3 characters long'
        username = "123"
        self.assertEqual(len(username), 3)
        doc = {
            "msg": "hello %s!" % username
        }
        result = self.simulate_post(
            '/register',
            json={
                "username": username,
                "password": "password1234"
            }
        )
        self.assertEqual(result.json, doc)
        self.assertEqual(result.status_code, 201)
        self.check_account_created(username=username)

        print 'Business rule: usernames must be at least 3 characters long'
        username = "12"
        self.assertLess(len(username), 3)
        result = self.simulate_post(
            '/register',
            json={
                "username": username,
                "password": "password1234"
            }
        )
        self.assertEqual(result.status_code, 400)
        self.assertTrue('errors' in result.json)
        self.assertEqual(len(result.json['errors']), 1)
        self.assertEqual(result.json['errors'][0]['field'], 'username')

        print 'Business rule: usernames must be 50 or less characters long'
        username = "12345678901234567890123456789012345678901234567890"
        self.assertEqual(len(username), 50)
        doc = {
            "msg": "hello %s!" % username
        }
        result = self.simulate_post(
            '/register',
            json={
                "username": username,
                "password": "password1234"
            }
        )
        self.assertEqual(result.json, doc)
        self.assertEqual(result.status_code, 201)
        self.check_account_created(username=username)

        print 'Business rule: usernames must be 50 or less characters long'
        username = "12345678901234567890123456789012345678901234567890112345"
        self.assertGreater(len(username), 50)
        result = self.simulate_post(
            '/register',
            json={
                "username": username,
                "password": "password1234"
            }
        )
        self.assertEqual(result.status_code, 400)
        self.assertTrue('errors' in result.json)
        self.assertEqual(len(result.json['errors']), 1)
        self.assertEqual(result.json['errors'][0]['field'], 'username')
