from falcon import testing
from sqlalchemy import create_engine
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


class TestRootAPI(MyTestCase):
    def test_get_message(self):
        doc = {
            "msg": "hello world!"
        }

        result = self.simulate_get('/')
        self.assertEqual(result.json, doc)


class TestRegisterAPI(MyTestCase):
    def test_register(self):
        doc = {
            "msg": "hello weffey!"
        }

        result = self.simulate_post(
            '/register',
            json={
                "username": "weffey",
                "password": "password"
            }
        )
        self.assertEqual(result.json, doc)

        results = self.session.execute("SELECT * from users where username = 'weffey';").fetchall()
        self.assertEqual(len(results), 1)
