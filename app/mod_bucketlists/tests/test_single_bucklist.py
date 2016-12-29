from app.test_config import BaseTestCase


class SingleBucketListTestCase(BaseTestCase):
    def test_get_single_bucketlist(self):
        response = self.client.get('/bucketlists/1', headers=self.token, follow_redirects=True)

        self.assertEqual(200, response.status_code)

        response = response.data.decode('utf-8')
        self.assertIn('data', response)
        self.assertIn('items', response)
        self.assertIn('date_created', response)
        self.assertIn('created_by', response)

    def test_error_on_getting_non_existent_bucketlist(self):
        response = self.client.get('/bucketlists/1000', headers=self.token, follow_redirects=True)

        self.assertEqual(404, response.status_code)

        response = response.data.decode('utf-8')
        self.assertIn('error', response)
        self.assertIn('bucket list not found', response)

    def test_error_on_getting_bucketlist_with_invalid_token(self):
        response = self.client.get('/bucketlists/1', headers=self.invalid_token, follow_redirects=True)

        self.assertEqual(403, response.status_code)

        response = response.data.decode('utf-8')
        self.assertIn('error', response)
        self.assertIn('invalid token', response)
        self.assertIn('target', response)

    def test_error_on_getting_bucketlist_with_expired_token(self):
        response = self.client.get('/bucketlists/1', headers=self.expired_token, follow_redirects=True)

        self.assertEqual(403, response.status_code)

        response = response.data.decode('utf-8')
        self.assertIn('error', response)
        self.assertIn('expired token', response)
        self.assertIn('target', response)

    def test_updates_bucketlist_name(self):
        data = {'name': 'New Bucket'}
        response = self.client.post('/bucketlists/1', data=data, headers=self.token, follow_redirects=True)

        self.assertEqual(200, response.status_code)

        response = response.data.decode('utf-8')
        self.assertIn('updated bucketlist name', response)
        self.assertIn(data['name'], response)

    def test_error_updating_bucketlist_with_empty_name(self):
        data = {'name': ''}
        response = self.client.post('/bucketlists/1', data=data, headers=self.token, follow_redirects=True)

        self.assertEqual(400, response.status_code)

        response = response.data.decode('utf-8')
        self.assertIn('error', response)
        self.assertIn('BucketList name is empty', response)
        self.assertIn('target', response)

    def test_error_on_updating_bucketlist_name_to_existing_name(self):
        data = {'name': 'Bucket List'}  # TODO set backet name from config
        response = self.client.post('/bucketlists/1', data=data, headers=self.token, follow_redirects=True)

        self.assertEqual(400, response.status_code)

        response = response.data.decode('utf-8')
        self.assertIn('error', response)
        self.assertIn('new BucketList name is equal to new name', response)
        self.assertIn('target', response)

    def test_deletes_users_bucketlist(self):
        response = self.client.delete('/bucketlists/1', headers=self.token, follow_redirects=True)

        self.assertEqual(400, response.status_code)

        response = response.data.decode('utf-8')
        self.assertIn('data', response)
        self.assertIn('successfully deleted bucketlist', response)
