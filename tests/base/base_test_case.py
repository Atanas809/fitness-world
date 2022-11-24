from django.contrib.auth import get_user_model
from django.test import TestCase

from fitness_world.photos.models import Photo

UserModel = get_user_model()


class BaseTestCase(TestCase):
    def create_and_login_user(self, **credentials):
        user = UserModel.objects.create_user(**credentials)

        self.client.login(**credentials)

        return user

    def create_photos(self, user, count=6):
        photos = []

        for x in range(1, count + 1):
            photo = Photo.objects.create(
                image=f'images/axolotl{x}_GmxzBbK.jpeg',
                user=user,
            )

            photo.full_clean()
            photo.save()
            photos.append(photo)

        return photos

    def assertCollectionIsEmpty(self, collection):
        return self.assertEqual(0, len(collection), 'Collection is not empty!')
