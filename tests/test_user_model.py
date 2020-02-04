import unittest
from flask import current_app
from app import create_app, db
from app.models import User, UserContact, UserRole


class TestUserModel(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_contest = self.app.app_context()
        self.app_contest.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_contest.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_password_setter(self):
        u = User(user_name='joe', email='joe@gmail.com', password='joe')
        self.assertTrue(u.password_hashed is not None)

    def test_password_hashing_method(self):
        u = User(user_name='joe', email='joe@gmail.com', password='joe')
        self.assertTrue(u.password_hashed is not 'joe')

    def test_password_verification(self):
        u = User(user_name='joe', email='joe@gmail.com', password='joe')
        self.assertTrue(u.verify_password('joe'))
        self.assertFalse(u.verify_password('jeoeee'))

    def test_password_hashing_are_random(self):
        u1 = User(user_name='joe', email='joe@gmail.com', password='joe')
        u2 = User(user_name='joee', email='joee@gmail.com', password='joeee')
        self.assertTrue(u1.password_hashed != u2.password_hashed)

    def test_is_confirmed(self):
        u = User(user_name='joe', email='joe@gmail.com', password='joe')
        self.assertFalse(u.is_confirmed)


if __name__ == '__main__':
    unittest.main()