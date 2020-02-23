from django.test import TestCase, Client
from .models import Post, User
import datetime as dt
from django.core import mail

class PostsTest(TestCase):

    def SetUp(self):
        self.client = Client()
        
    def testProfilePageCode(self):
        self.user = User.objects.create_user('dummy', 'dummy@dummy.com', 'dummy')
        response = self.client.get('/dummy/')
        self.assertEqual(response.status_code, 200)

    def testNewAnonymous(self):
        response = self.client.get('/new/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/auth/login/?next=/new/')
       
    def testNewRegistred(self):
        self.user = User.objects.create_user('dummy', 'dummy@dummy.com', 'dummy')
        self.client.post('/auth/login/', {'username': 'dummy', 'password': 'dummy'}, follow=True)
        response = self.client.get('/new/')
        self.assertEqual(response.status_code, 200)

    def testPostPresense(self):
        self.user = User.objects.create_user('dummy', 'dummy@dummy.com', 'dummy')
        self.post = Post.objects.create(text="This is a test post", author=self.user, id=1)
        response = self.client.get('')
        self.assertContains(response, 'This is a test post')
        response = self.client.get('/dummy/')
        self.assertContains(response, 'This is a test post')
        response = self.client.get('/dummy/1/')
        self.assertContains(response, 'This is a test post')

    def testPostEdit(self):
        self.user = User.objects.create_user('dummy', 'dummy@dummy.com', 'dummy')
        self.client.post('/auth/login/', {'username': 'dummy', 'password': 'dummy'}, follow=True)
        self.post = Post.objects.create(text="This is a test post", author=self.user, id=1)
        response = self.client.get('/dummy/1/edit')
        self.assertEqual(response.status_code, 200)
        self.post.text = 'This is an updated post'
        self.post.save()
        response = self.client.get('/dummy/1/')
        self.assertContains(response, 'This is an updated post')
        response = self.client.get('/dummy/')
        self.assertContains(response, 'This is an updated post')
        response = self.client.get('')
        self.assertContains(response, 'This is an updated post')

class EmailTest(TestCase):
    def SetUp(self):
        self.client = Client()
    
    def test_send_msg(self):
        self.user = User.objects.create_user('dummy_two', 'dummy_two@dummy_two.com', 'dummy_two')
        mail.send_mail(
            "Successful registration", "Sup, welcome to Yatubah", 'yatube@yatube.com', ['dummy_two@dummy_two.com'], fail_silently=False,
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Successful registration")
