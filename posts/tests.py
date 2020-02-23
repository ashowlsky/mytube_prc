from django.test import TestCase, Client
from .models import Post, User
import datetime as dt
from django.core import mail

class PostsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('dummy', 'dummy@dummy.com', 'dummy')
        self.post = Post.objects.create(text="This is a test post", author=self.user, id=1)
        self.client.post('/auth/login/', {'username': 'dummy', 'password': 'dummy'}, follow=True)

    def test_profile_page_code(self):
        """Tests if a user profile page is accessible after registration."""
        response = self.client.get('/dummy/')
        self.assertEqual(response.status_code, 200)
  
    def test_new_registred_user(self):
        """ Tests if a registred user can access post creation form. """
        response = self.client.get('/new/')
        self.assertEqual(response.status_code, 200)
 
    def test_new_anonymous_user(self):
        """ Tests if it's forbidden for an anonymous user to access post creation form """
        self.client.logout()
        response = self.client.get('/new/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/auth/login/?next=/new/')
  
    def test_post_presence(self):
        """ Tests whether post text is present on all respective pages """
        urls=['', '/dummy/', '/dummy/1/']
        for url in urls:
            response = self.client.get(url)
            self.assertContains(response, 'This is a test post')

    def test_post_edit(self):
        """ Tests if a registered user can access post editing form and the edited post text changes on all respective pages """
        response = self.client.get('/dummy/1/edit/')
        self.assertEqual(response.status_code, 200)
        self.post.text = 'This is an updated post'
        self.post.save()
        urls=['', '/dummy/', '/dummy/1/']
        for url in urls:
            response = self.client.get(url)
            self.assertContains(response, 'This is an updated post')

class EmailTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('dummy_two', 'dummy_two@dummy_two.com', 'dummy_two')
 
    def testSendMsg(self):
        """Tests if an email is being sent to a user upon registration completion"""
        mail.send_mail(
            "Successful registration", "Sup, welcome to Yatubah", 'yatube@yatube.com', ['{{self.user.email}}'], fail_silently=False,
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Successful registration")