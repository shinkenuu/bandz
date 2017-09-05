import ast
from rest_framework.test import APITestCase
from rest_framework import status
from unittest import TestCase
from . import services, models


class GooglePlacesTestCase(TestCase):
    def setUp(self):
        pass

    def test_google_place_api(self):
        place = services.get_place_from_google_places(
            'EjJSLiBBdWd1c3RhIC0gQ29uc29sYcOnw6NvLCBTw6NvIFBhdWxvIC0gU1AsIEJyYXNpbA')
        self.assertTrue('Augusta' in place.formatted_address)


class MusicGenreTestCase(APITestCase):
    def setUp(self):
        self.music_genre = models.MusicGenre.objects.create(name='Whatever')

    def test_create(self):
        response = self.client.post('/api/music-genres/', {'name': 'Estilo'})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_list(self):
        response = self.client.get('/api/music-genres/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve(self):
        response = self.client.get('/api/music-genres/{}/'.format(self.music_genre.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update(self):
        response = self.client.put('/api/music-genres/{}/'.format(self.music_genre.pk), {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.patch('/api/music-genres/{}/'.format(self.music_genre.pk), {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete(self):
        response = self.client.delete('/api/music-genres/{}/'.format(self.music_genre.pk))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class PlaceTestCase(APITestCase):
    def setUp(self):
        self.place = services.get_place_from_google_places(
            'EjJSLiBBdWd1c3RhIC0gQ29uc29sYcOnw6NvLCBTw6NvIFBhdWxvIC0gU1AsIEJyYXNpbA')

    def test_create(self):
        response = self.client.post('/api/places/', {'id': 'ChIJLzxRozNXzpQRSi7uA3HN3B8'})  # Brooklin
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list(self):
        self.place.save()
        response = self.client.get('/api/places/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve(self):
        self.place.save()
        response = self.client.get('/api/places/{}/'.format(self.place.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update(self):
        self.place.save()
        response = self.client.put(
            '/api/places/{}/'.format(self.place.pk),
            {'id': self.place.id, 'formatted_address': ''})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data.get('formatted_address', ''), '')

        response = self.client.patch(
            '/api/places/{}/'.format(self.place.pk),
            {'id': self.place.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        self.place.save()
        response = self.client.delete('/api/places/{}/'.format(self.place.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class EventTestCase(APITestCase):
    def setUp(self):
        host_user = models.User.objects.create_user(username='host', email='host@gmail.com', password='host1234')
        host_place = services.get_place_from_google_places('ChIJLzxRozNXzpQRSi7uA3HN3B8')
        host_place.save()
        self.host = models.Host.objects.create(
            name='Host Name',
            description='Host Description',
            user=host_user,
            url='http://www.facebook.com/host',
            max_capacity=150,
            place=host_place
        )
        self.event = models.Event.objects.create(
            name='Event name',
            description='Event description',
            starts_at='2017-08-28 22:00:00',
            ends_at='2017-08-29 00:00:00',
            min_age=16,
            price=10.00,
            host=self.host,
        )

    def test_create(self):
        response = self.client.post(
            '/api/events/',
            {
                'name': 'Event name on creation test',
                'description': 'Event description',
                'starts_at': '2017-08-28 22:00:00',
                'ends_at': '2017-08-29 00:00:00',
                'min_age': 16,
                'price': 10.00,
                'host': self.host.id,
            })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(
            '/api/events/',
            {
                'name': 'Event name on creation test',
                'description': 'Event description',
                'starts_at': '2017-08-28 22:00:00',
                'ends_at': '2017-08-29 00:00:00',
                'min_age': 16,
                'price': 10.00,
                'host': 0,
            })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list(self):
        self.event.save()
        response = self.client.get('/api/events/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve(self):
        self.event.save()
        response = self.client.get('/api/events/{}/'.format(self.event.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update(self):
        self.event.save()
        response = self.client.patch(
            '/api/events/{}/'.format(self.event.pk),
            {
                'band_id': 1
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        self.event.save()
        response = self.client.delete('/api/events/{}/'.format(self.event.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class PropositionTestCase(APITestCase):
    def setUp(self):
        host_user = models.User.objects.create_user(username='host', email='host@gmail.com',
                                                    password='host1234')
        host_place = services.get_place_from_google_places('ChIJLzxRozNXzpQRSi7uA3HN3B8')
        host_place.save()
        self.host = models.Host.objects.create(
            name='Host Name',
            description='Host Description',
            user=host_user,
            url='http://www.facebook.com/host',
            max_capacity=150,
            place=host_place
        )

        band_user = models.User.objects.create_user(username='band', email='band@gmail.com',
                                                    password='band1234')
        band_place = services.get_place_from_google_places(
            'EjJSLiBBdWd1c3RhIC0gQ29uc29sYcOnw6NvLCBTw6NvIFBhdWxvIC0gU1AsIEJyYXNpbA')
        band_place.save()
        self.band = models.Band.objects.create(
            name='Band Name',
            description='band Description',
            user=band_user,
            url='http://www.facebook.com/band',
            place=band_place
        )

        self.event = models.Event.objects.create(
            name='Event name',
            description='Event description',
            starts_at='2017-08-28 22:00:00',
            ends_at='2017-08-29 00:00:00',
            min_age=16,
            price=10.00,
            host=self.host,
        )

        self.proposition = models.Proposition(
            band=self.band,
            host=self.host,
            event=self.event,
            message='Vamos fechar?',
            price=200.00,
        )

    def test_create(self):
        response = self.client.post(
            '/api/propositions/',
            {
                'band': self.band.id,
                'host': self.host.id,
                'event': self.event.id,
                'message': 'Proposition message',
                'price': 10.00,
            })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(
            '/api/propositions/',
            {
                'band': self.band.id,
                'host': self.host.id + 1,
                'event': self.event.id,
                'message': 'Proposition message',
                'price': 10.00,
            })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list(self):
        self.proposition.save()
        response = self.client.get('/api/propositions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve(self):
        self.proposition.save()
        response = self.client.get('/api/propositions/{}/'.format(self.proposition.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update(self):
        self.proposition.save()
        response = self.client.patch(
            '/api/propositions/{}/'.format(self.proposition.pk),
            {
                'band_id': self.band.id + 1
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.patch(
            '/api/propositions/{}/'.format(self.proposition.pk),
            {
                'host_id': self.host.id + 1
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.patch(
            '/api/propositions/{}/'.format(self.proposition.pk),
            {
                'event_id': self.event.id + 1
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        self.proposition.save()
        response = self.client.delete('/api/propositions/{}/'.format(self.proposition.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_event_update(self):
        self.proposition.save()
        response = self.client.patch(
            '/api/propositions/{}/'.format(self.proposition.pk),
            {
                'confirmed': True,
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data.get('confirmed', False))

        response = self.client.get('/api/events/{}/'.format(self.event.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        band_confirmed_in_event_dict = ast.literal_eval(response.data.get('band', {}))
        self.assertEqual(band_confirmed_in_event_dict.get('id', 0), self.band.id)
        self.assertTrue(response.data.get('confirmed', False))
