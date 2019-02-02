import os
import tempfile

from unittest import mock
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from django.utils.http import urlencode
from PIL import Image

from ..photos import models as photo_models
from .serializers import PhotoSerializer

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
)


class BaseViewTest(APITestCase):
    """" Set up test database"""
    client = APIClient()

    @staticmethod
    def create_photo(photo, title, owner, description=None):
            photo_models.Photo.objects.create(
                photo=photo,
                title=title,
                description=description,
                owner=owner
            )

    def setUp(self):
        self.user = User.objects.create_user(
           username='admin',
           email='admin@admin.com',
           password='admin',
        )
        def test_cache():
            """Reroute the signal so that a @receiver decorated method is not called.

            Creating a Photo instance will send a signal to the @receiver method
            located in photos/models.py. This function reroutes the signal to itself.

            """ 
            with mock.patch('photo_sharing_site.photos.models.analyze_Photo', autospec=True) as mocked_handler:
                post_save.connect(mocked_handler, sender=photo_models.Photo, dispatch_uid='test_cache_mocked_handler')
                self.create_photo(
                    os.path.join(BASE_DIR, 'media', 'test1.png'),
                    'hotdog photo',
                    self.user,
                    'testing_testing',
                )
                self.create_photo(
                    None,
                    'not hotdog photo',
                    self.user,
                    'testing_testing',
                )
            self.assertEquals(mocked_handler.call_count, 1)


class GetPhotoTests(BaseViewTest):
    """Different tests are defined here"""

    def test_get(self):
        """
        Test GET request at endpoint api/photos/

        This will also test GET at the specific endpoints api/photos/uuid/
        """
        response = self.client.get(reverse('photo-list'))
        expected = photo_models.Photo.objects.all()
        serialized = PhotoSerializer(expected, many=True)

        self.assertEqual(expected, serialized.instance)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_Photo(self):
        """Test POST request at api/photos/"""
        message = {
            'title': 'testHotdog',
            'owner': User.objects.get(username='admin').id,
            'description': 'very random'
        }
        path = 'http://127.0.0.1:8000/api/photos/'
        request = self.client.post(path, data=message)
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

    def test_flag_photo(self):
        """Test PUT request at api/photos/uuid/flagged/"""
        message = {
            'title': 'testHotdog',
            'owner': User.objects.get(username='admin').id,
            'description': 'very random'
        }
        path = 'http://127.0.0.1:8000/api/photos/'
        request = self.client.post(path, data=message)
        uuid = request.data.get('id')
        path = 'http://127.0.0.1:8000/api/photos/' + uuid + '/flagged/'
        request = self.client.put(
            path,
            data=urlencode({'flagged': 'true'}),
            content_type='application/x-www-form-urlencoded'
        )
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_put_photo_instance(self):
        """Test PUT request at api/photos/uuid/photo/ by creating a tempfile."""
        message = {
            'title': 'testHotdog',
            'owner': User.objects.get(username='admin').id,
            'description': 'very random'
        }
        path = 'http://127.0.0.1:8000/api/photos/'
        request = self.client.post(path, data=message)
        uuid = request.data.get('id')
        path = 'http://127.0.0.1:8000/api/photos/' + uuid + '/photo/'

        image = Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        with open(tmp_file.name, 'rb') as data:
            request = self.client.put(
                path,
                {'image': data},
                format='multipart'
            )
            self.assertEqual(request.status_code, status.HTTP_200_OK)
        print('DONE')

        def test_get_next_photo(self):
            pass

        def test_list_photos(self):
            pass

        def test_authentication(self):
            pass
