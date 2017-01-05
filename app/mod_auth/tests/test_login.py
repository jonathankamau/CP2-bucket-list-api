from app.test_config import BaseTestCase


class LoginTestCase(BaseTestCase):
    def test_successful_login_on_valid_credentials(self):
        response = self.client.post('/auth/login/', data={
            'username': 'brian',
            'password': 'password'
        }, follow_redirects=True)

        self.assertEqual(200, response.status_code)

        response = response.data.decode('utf-8')
        self.assertIn('data: ', response)
        self.assertIn('brian', response)
        self.assertIn('token: ', response)

    def test_login_fails_no_username_submitted(self):
        response = self.client.post('/auth/login/', data={
            'password': 'password'
        }, follow_redirects=True)

        self.assertEqual(400, response.status_code)

        response = response.data.decode('utf-8')
        self.assertIn('error', response)
        self.assertIn('unable to login user', response)
        self.assertIn('username data field missing from POST request', response)

    def test_login_fails_no_password_submitted(self):
        response = self.client.post('/auth/login/', data={
            'username': 'brian'
        }, follow_redirects=True)

        self.assertEqual(400, response.status_code)

        response = response.data.decode('utf-8')
        self.assertIn('error', response)
        self.assertIn('unable to login user', response)
        self.assertIn('password data field missing from POST request', response)

    def test_login_fails_invalid_credentials(self):
        response = self.client.post('/auth/login/', data={
            'username': 'john',
            'password': 'password'
        }, follow_redirects=True)

        self.assertEqual(401, response.status_code)
        self.assertIn('error', response)
        self.assertIn('unable to login user', response)
        self.assertIn('invalid username/password combination', response)
