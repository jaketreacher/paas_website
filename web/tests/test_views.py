from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.db.models import Q
from web.models import Event

from datetime import timedelta
from bs4 import BeautifulSoup


class EventViewTest(TestCase):
    @staticmethod
    def get_event_list(response):
        soup = BeautifulSoup(response.content, 'html.parser')
        event_list = list()
        for card_html in soup.find_all('div', {'class': 'event-card'}):
            url = card_html.find('a', href=True)['href']
            event_list.append(url)
        return event_list

    def setUp(self):
        User.objects.create_user('standard_user')
        User.objects.create_user('staff_user', is_staff=True)
        User.objects.create_user('super_user', is_staff=True, is_superuser=True)

        yesterday = timezone.now() - timedelta(days=1)
        tomorrow = timezone.now() + timedelta(days=1)

        Event.objects.create(name='Open Event', slug='open-event', open_date=yesterday)
        Event.objects.create(name='Closed Event', slug='closed-event', open_date=tomorrow)

    def test_open_event_shown_for_guest(self):
        response = self.client.get('/open-event')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'web/pages/event.html')

    def test_open_event_shown_for_all_users(self):
        for user in User.objects.all():
            self.client.force_login(user)
            response = self.client.get('/open-event')
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'web/pages/event.html')
            self.client.logout()

    def test_closed_event_redirect_to_home_for_guest(self):
        response = self.client.get('/closed-event')
        self.assertRedirects(response, reverse('home'), target_status_code=200)

    def test_closed_event_redirect_to_home_for_standard_user(self):
        self.client.force_login(User.objects.get(username='standard_user'))
        response = self.client.get('/closed-event')
        self.assertRedirects(response, reverse('home'), target_status_code=200)

    def test_closed_event_shown_for_staff_user(self):
        self.client.force_login(User.objects.get(username='staff_user'))
        response = self.client.get('/closed-event')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'web/pages/event.html')

    def test_closed_event_shown_for_super_user(self):
        self.client.force_login(User.objects.get(username='super_user'))
        response = self.client.get('/closed-event')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'web/pages/event.html')

    def test_open_even_listed_for_guest(self):
        response = self.client.get(reverse('event-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'web/pages/event-list.html')
        event_list = self.get_event_list(response)
        self.assertTrue('/open-event' in event_list)

    def test_open_event_listed_for_all_users(self):
        for user in User.objects.all():
            self.client.force_login(user)
            response = self.client.get(reverse('event-list'))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'web/pages/event-list.html')
            event_list = self.get_event_list(response)
            self.assertTrue('/open-event' in event_list)

    def test_closed_event_hidden_for_guest(self):
        response = self.client.get(reverse('event-list'))
        self.assertEqual(response.status_code, 200)
        event_list = self.get_event_list(response)
        self.assertFalse('/closed-event' in event_list)

    def test_closed_event_hidden_for_standard_user(self):
        self.client.force_login(User.objects.get(username='standard_user'))
        response = self.client.get(reverse('event-list'))
        self.assertEqual(response.status_code, 200)
        event_list = self.get_event_list(response)
        self.assertFalse('/closed-event' in event_list)

    def test_closed_event_listed_for_staff_user(self):
        self.client.force_login(User.objects.get(username='staff_user'))
        response = self.client.get(reverse('event-list'))
        self.assertEqual(response.status_code, 200)
        event_list = self.get_event_list(response)
        self.assertTrue('/closed-event' in event_list)

    def test_closed_event_listed_for_super_user(self):
        self.client.force_login(User.objects.get(username='super_user'))
        response = self.client.get(reverse('event-list'))
        self.assertEqual(response.status_code, 200)
        event_list = self.get_event_list(response)
        self.assertTrue('/closed-event' in event_list)