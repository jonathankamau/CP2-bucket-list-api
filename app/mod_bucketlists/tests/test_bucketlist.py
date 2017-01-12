from app.test_config import BaseTestCase


class BucketListTestCase(BaseTestCase):
    def test_creates_new_bucketlist_with_token(self):
        data = {
            'bucket_name': 'Christmas'
        }
        response = self.client.post('/bucketlists/', data=data, headers=self.token, follow_redirects=True)

        self.assertEqual(201, response.status_code)

        response = response.data.decode('utf-8')
        self.assertIn(data['bucket_name'], response)
        self.assertIn('date_created', response)

    def test_gets_bucketlist_names_for_the_user(self):
        response = self.client.get('/bucketlists/', headers=self.token, follow_redirects=True)

        response = response.data.decode('utf-8')
        self.assertIn('Checkpoint', response)
        self.assertIn('created_by', response)
        self.assertIn('date_created', response)

    def test_search_bucketlist_by_name(self):
        response = self.client.get('/bucketlists/?q=Check', headers=self.token, follow_redirects=True)

        response = response.data.decode('utf-8')
        self.assertIn('Checkpoint', response)
        self.assertIn('created_by', response)
        self.assertIn('date_created', response)
        self.assertIn('next', response)
        self.assertIn('prev', response)

    def test_error_on_bucketlist_creation_with_invalid_token(self):
        data = {
            'bucket_name': 'Christmas'
        }
        response = self.client.post('/bucketlists/', data=data, headers=self.invalid_token, follow_redirects=True)

        self.assertEqual(403, response.status_code)

        response = response.data.decode('utf-8')
        self.assertIn('error', response)
        self.assertIn('invalid token', response)

    def test_error_on_bucketlist_creation_with_expired_token(self):
        data = {
            'bucket_name': 'Christmas'
        }
        response = self.client.post('/bucketlists/', data=data, headers=self.expired_token, follow_redirects=True)

        self.assertEqual(403, response.status_code)

        response = response.data.decode('utf-8')
        self.assertIn('error', response)
        self.assertIn('expired token', response)
