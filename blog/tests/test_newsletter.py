from django.test import TestCase
from django.template.defaultfilters import urlencode

from blog import models


class NewsletterTests(TestCase):

    def test_CanSignIntoNewsletter(self):
        email = 'sample@cheese.foo'
        self.client.post('/newsletter/', {'email': email},
                         content_type='application/json')
        result = models.NewsletterAddresse.objects.values('email')
        expected = [{'email': email}]
        self.assertListEqual(expected, list(result))

    def test_CanResignFromNewsletter(self):
        email = 'sample@cheese.foo'
        addresse = models.NewsletterAddresse.objects.create(email=email)
        email = urlencode(email)
        token = urlencode(addresse.token)
        self.client.post(f'/cancel-newsletter/{email}/{token}/')
        self.assertEqual(0, models.NewsletterAddresse.objects.count())
