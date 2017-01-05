from app.test_config import BaseTestCase


class BucketListTestCase(BaseTestCase):
    def test_creates_new_bucketlist_with_token(self):
        data = {
            'bucket_name': 'Christmas'
        }
        response = self.client.post('/bucketlists/', data=data, headers=self.token, follow_redirects=True)

        self.assertEqual(201, response.status_code)

        response = response.data.decode('utf-8')
        self.assertIn('data', response)
        self.assertIn('new BucketList created successfully', response)
        self.assertIn(data['bucket_name'], response)
        self.assertIn('date_created', response)

    def test_gets_bucketlist_names_for_the_user(self):
        response = self.client.get('/bucketlists/', headers=self.token, follow_redirects=True)

        self.assertEqual(200, response.status_code)

        response = response.data.decode('utf-8')
        self.assertIn('data', response)
        self.assertIn('items', response)
        self.assertIn('date_created', response)

    def test_error_on_bucketlist_creation_with_invalid_token(self):
        token = {'Authorization': 'Token ' + 'abcd'}
        data = {
            'bucket_name': 'Christmas'
        }
        response = self.client.post('/bucketlists/', data=data, headers=token, follow_redirects=True)

        self.assertEqual(400, response.status_code)

        response = response.data.decode('utf-8')
        self.assertIn('error', response)
        self.assertIn('unable to create bucketlist', response)
        self.assertIn('invalid token', response)

    def test_error_on_bucketlist_creation_with_expired_token(self):
        data = {
            'bucket_name': 'Christmas'
        }
        response = self.client.post('/bucketlists/', data=data, headers=self.expired_token, follow_redirects=True)

        self.assertEqual(400, response.status_code)

        response = response.data.decode('utf-8')
        self.assertIn('error', response)
        self.assertIn('unable to create bucketlist', response)
        self.assertIn('expired token', response)
