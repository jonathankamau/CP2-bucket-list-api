from app.test_config import BaseTestCase


class BucketListItemTestCase(BaseTestCase):
    def test_create_new_bucket_list_item(self):
        data = {'name': 'Change Title Of Story',
                'description': 'The Author changed the story hence the change'}
        response = self.client.post('/bucketlists/1/items/', data=data, headers=self.token, follow_redirects=True)

        self.assertEqual(201, response.status_code)

        response = response.data.decode('utf-8')
        self.assertIn('date_modified', response)
        self.assertIn(data['name'], response)
        self.assertIn(data['description'], response)

    def test_error_on_create_item_on_non_existent_bucketlist(self):
        data = {'name': 'Change Title Of Story'}
        response = self.client.post('/bucketlists/100/items/', data=data, headers=self.token, follow_redirects=True)

        self.assertEqual(404, response.status_code)

        response = response.data.decode('utf-8')
        self.assertIn('error', response)
        self.assertIn('bucketlist list does not exists', response)

    def test_error_on_create_bucketlist_item_without_token(self):
        data = {'name': 'Change Title Of Story'}
        response = self.client.post('/bucketlists/1/items/', data=data, follow_redirects=True)

        self.assertEqual(401, response.status_code)

        response = response.data.decode('utf-8')
        self.assertIn('error', response)
        self.assertIn('no token to submitted', response)

    def test_update_bucketlist_item_name_and_description(self):
        data = {'name': 'Updated name for item',
                'description': 'Test change name'}
        response = self.client.put('/bucketlists/1/items/1', data=data, headers=self.token, follow_redirects=True)

        response = response.data.decode('utf-8')
        self.assertIn(data['name'], response)
        self.assertIn(data['description'], response)

    def test_update_bucketlist_item_to_done(self):
        data = {'done': 'true'}
        response = self.client.put('/bucketlists/1/items/1', data=data, headers=self.token, follow_redirects=True)

        response = response.data.decode('utf-8')
        self.assertIn('true', response)

    def test_update_bucketlist_item_to_not_done(self):
        data = {'done': 'false'}
        response = self.client.put('/bucketlists/1/items/1', data=data, headers=self.token, follow_redirects=True)

        response = response.data.decode('utf-8')
        self.assertIn('false', response)

    def test_update_bucketlist_item_invalid_status(self):
        data = {'done': 'ffdse'}
        response = self.client.put('/bucketlists/1/items/1', data=data, headers=self.token, follow_redirects=True)

        self.assertEqual(400, response.status_code)

    def test_error_on_updating_non_existent_bucketlist_item(self):
        data = {'name': 'Updated name for item',
                'description': 'Test change name'}
        response = self.client.put('/bucketlists/1/items/100', data=data, headers=self.token, follow_redirects=True)

        self.assertEqual(404, response.status_code)

        response = response.data.decode('utf-8')
        self.assertIn('error', response)
        self.assertIn('bucketlist item not found', response)
