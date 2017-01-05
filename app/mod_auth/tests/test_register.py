from app.test_config import BaseTestCase


class RegisterTestCase(BaseTestCase):
    def test_creates_new_user_successfully(self):
        response = self.client.post('/auth/register/', data={
            'username': 'user',
            'password': 'password'
        }, follow_redirects=True)

        self.assertEqual(201, response.status_code)

        response = response.data.decode('utf-8')
        self.assertIn('data', response)
        self.assertIn('brian', response)
        self.assertIn('new user created successfully', response)

    def test_registration_fails_no_username(self):
        response = self.client.post('/auth/register/', data={
            'password': 'password'
        }, follow_redirects=True)

        self.assertEqual(400, response.status_code)

        response = response.data.decode('utf-8')
        self.assertIn('error', response)
        self.assertIn('unable to create user', response)
        self.assertIn('username data field missing/empty from POST request', response)

    def test_registration_fails_no_password(self):
        response = self.client.post('/auth/register/', data={
            'username': 'brian'
        }, follow_redirects=True)

        self.assertEqual(400, response.status_code)

        response = response.data.decode('utf-8')
        self.assertIn('error', response)
        self.assertIn('unable to create user', response)
        self.assertIn('password data field missing/empty from POST request', response)

    def test_registration_fails_using_existing_username(self):
        response = self.client.post('/auth/register/', data={
            'username': 'brian',
            'password': 'password'
        }, follow_redirects=True)

        self.assertEqual(400, response.status_code)

        response = response.data.decode('utf-8')
        self.assertIn('error', response)
        self.assertIn('unable to create user', response)
        self.assertIn('username already registered', response)
