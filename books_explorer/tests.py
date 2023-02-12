import uuid
from django.contrib.auth.models import User
from django.test import Client, TestCase
from .models import CSVFiles


class UploadFileViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'testuser'
        self.password = 'secret'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_upload_file_view_with_valid_file(self):
        self.client.login(username=self.username, password=self.password)
        file = open('test.csv', 'w')
        file.write('uuid,title,author,date_published,publisher\n')
        file.write(
            'f91ee86d-776e-4977-a443-2dc853883485,'
            'The Great Gatsby,'
            'F. Scott Fitzgerald,'
            '1925-04-10,'
            ' Charles Scribner\'s Sons')
        file.close()

        with open('test.csv', 'rb') as f:
            response = self.client.post('/upload_file/', {'csv_file': f})
            self.assertRedirects(response, '/{}'.format(CSVFiles.objects.first().uuid))
            self.assertEqual(response.status_code, 302)

    def test_upload_file_view_with_invalid_file(self):
        self.client.login(username=self.username, password=self.password)
        file = open('test.csv', 'w')
        file.write('col1,col2\n')
        file.write('1,\n')
        self.assertRaises(ValueError)
        self.assertEqual(CSVFiles.objects.count(), 0)

    def test_with_unauthenticated_user(self):
        self.client.login(username="asfasf", password="?1231axfasf#r123")
        response = self.client.get('/upload_file/')
        self.assertEqual(response.status_code, 302)


class HomeViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'testuser'
        self.password = 'secret'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.csv_file = CSVFiles.objects.create(aws_url='test.com', author=self.user,
                                                uuid=uuid.UUID('345e790c-58ee-4e89-b7db-d743e845ce66'))

    def test_home_view_with_authenticated_user(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['all_data']), 1)
        """
        There is only one file in the database and on amazon, so the length of the list should be 1! 
        response.context['all_data'] [{'uuid': UUID('345e790c-58ee-4e89-b7db-d743e845ce66'), 'author': <User: testuser>, 'aws_url': 'test.com', 'data':                                    uuid       title  ... date_published   publisher
        0  d7edd490-9d35-43f4-84ef-d48c4022fe22  ReOstTCwJT  ...          21308  aeWPaVrqLZ
        1  f91ee86d-776e-4977-a443-2dc853883485  LZaCktNoMI  ...           6806  oFFSiSxLJa
        2  f1192fc2-893c-45aa-8a3c-0217bafeafab  WWknRaONzz  ...          20725  YokMgOQzBd
        3  1aa60165-b87e-4864-9fc8-d1085644d831  cDsdxvVFvw  ...          59929  zZGgKFqVvq
        """

    def test_home_view_with_unauthenticated_user(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login?next=/')


class RenderOneFileViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'testuser'
        self.password = 'secret'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.csv_file = 'books1.csv'

    def test_render_one_file_view_with_valid_uuid(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/345e790c-58ee-4e89-b7db-d743e845ce66')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['data'].shape, (8, 5))  # 8 rows and 5 columns in csv file 😉

    def test_render_one_file_view_with_invalid_uuid(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/345e790c-58ee-4e89-b7db-123123123')
        self.assertEqual(response.status_code, 404)
