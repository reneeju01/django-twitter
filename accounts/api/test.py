from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User


LOGIN_URL = '/api/accounts/login/'
LOGOUT_URL = '/api/accounts/logout/'
SIGNUP_URL = '/api/accounts/signup/'
LOGIN_STATUS_URL = '/api/accounts/login_status/'


class AccountApiTests(TestCase):

    def setUp(self):
        # This function will be executed before each test function executes
        self.client = APIClient()
        self.user = self.createUser(
            username = 'tester',
            email = 'tester@gmail.com',
            password = 'correct password',
        )

    def createUser(self, username, email, password):
        # Do not use User.objects.create()
        # Since password needs to be encrypted, username 和 email need to be
        # normalized
        return User.objects.create_user(username, email, password)

    def test_login(self):
        # login need to use post method, not get
        response = self.client.get(LOGIN_URL, {
            'username': self.user.username,
            'password': 'correct password',
        })
        # login failed，http status code return 405 = METHOD_NOT_ALLOWED
        self.assertEqual(response.status_code, 405)

        # post wrong username
        print('------------ start testing --------------')
        response = self.client.post(LOGIN_URL, {
            'username': 'notexists',
            'password': 'correct password',
        })
        self.assertEqual(response.status_code, 400)
        # print(response.content)
        print(response.data)
        print(response.data['errors']['username'])
        print(response.data['errors']['username'][0])
        self.assertEqual(response.data['errors']['username'][0],
                             'User does not exist.')

        print('------------ end testing --------------')

        # post wrong password
        response = self.client.post(LOGIN_URL, {
            'username': self.user.username,
            'password': 'wrong password',
        })
        self.assertEqual(response.status_code, 400)

        # validate login status as False
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], False)

        # post correct password
        response = self.client.post(LOGIN_URL, {
            'username': self.user.username,
            'password': 'correct password',
        })
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data['user'], None)
        self.assertEqual(response.data['user']['email'], 'tester@gmail.com')

        # test login status as True
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], True)

    def test_logout(self):
        # login first
        self.client.post(LOGIN_URL, {
            'username': self.user.username,
            'password': 'correct password',
        })
        # validate login status as True
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], True)

        # logout with get method not post, receive 405 = METHOD_NOT_ALLOWED
        response = self.client.get(LOGOUT_URL)
        self.assertEqual(response.status_code, 405)

        # use post successful logout
        response = self.client.post(LOGOUT_URL)
        self.assertEqual(response.status_code, 200)

        # validate login status as False
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], False)

    def test_signup(self):
        data = {
            'username': 'someone',
            'email': 'someone@gmail.com',
            'password': 'any password',
        }
        # Test get request failed
        response = self.client.get(SIGNUP_URL, data)
        self.assertEqual(response.status_code, 405)

        # Test the wrong email
        response = self.client.post(SIGNUP_URL, {
            'username': 'someone',
            'email': 'not a correct email',
            'password': 'any password'
        })
        # print(response.data)
        self.assertEqual(response.status_code, 400)

        # Test password is too short
        response = self.client.post(SIGNUP_URL, {
            'username': 'someone',
            'email': 'someone@gmail.com',
            'password': '123',
        })
        # print(response.data)
        self.assertEqual(response.status_code, 400)

        # Test username is too long
        response = self.client.post(SIGNUP_URL, {
            'username': 'username is tooooooooooooooooo loooooooong',
            'email': 'someone@gmail.com',
            'password': 'any password',
        })
        # print(response.data)
        self.assertEqual(response.status_code, 400)

        # Successfully registered
        response = self.client.post(SIGNUP_URL, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['user']['username'], 'someone')

        # Verify that the user is logged in
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], True)
