from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from ..models import Group, Post


User = get_user_model()


class StaticURLTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Name1')
        cls.user2 = User.objects.create_user(username='Name2')
        cls.group = Group.objects.create(
            title='Test group',
            slug='test-slug',
            description='Test description'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Trapatapatau'
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client_2 = Client()

        self.authorized_client.force_login(self.user)
        self.authorized_client_2.force_login(self.user2)

    def test_url_uses_correct_index(self):
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    # def test_about_author(self):
    #     response = self.guest_client.get('/about/author/')
    #     self.assertEqual(response.status_code, 200)

    # def test_about_tech(self):
    #     response = self.guest_client.get('/about/tech/')
    #     self.assertEqual(response.status_code, 200)

    def test_url_uses_correct_group(self):
        response = self.guest_client.get(f'/group/{StaticURLTests.group.slug}/')
        self.assertEqual(response.status_code, 200)

    def test_url_uses_correct_profile(self):
        response = self.guest_client.get(f'/profile/{StaticURLTests.user}/')
        self.assertEqual(response.status_code, 200)

    def test_url_authorized_post_id(self):
        response = self.guest_client.get(f'/posts/{StaticURLTests.post.id}/')
        self.assertEqual(response.status_code, 200)

    def test_create_url_authorized(self):
        """Проверка доступа для авторизованного пользователя к созданию поста"""
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, 200)

    def test_create_url_unauthorized(self):
        """Проверка доступа для неавторизованного пользователя к созданию поста"""
        response = self.guest_client.get('/create/')
        self.assertEqual(response.status_code, 302)

    def test_edit_url_unauthorized(self):
        """Проверка доступа для неавторизованного пользователя
         к редактированию поста"""
        response = self.guest_client.get(f'/posts/{StaticURLTests.post.id}/edit/')
        self.assertEqual(response.status_code, 302)

    def test_edit_url_not_by_author(self):
        """Проверка доступа для не автора к редактированию поста"""
        response = self.authorized_client_2.get(
            f'/posts/{self.post.id}/edit/')
        self.assertEqual(response.status_code, 302)

    def test_unexisting_url(self):
        """Проверка несуществующей страницы"""
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, 404)

    def test_urls_uses_correct_template(self):
        templates_url_names = {
            '/': 'posts/index.html',
            f'/group/{StaticURLTests.group.slug}/': 'posts/group_list.html',
            f'/profile/{StaticURLTests.user}/': 'posts/profile.html',
            f'/posts/{StaticURLTests.post.id}/edit/': 'posts/create_post.html',
            f'/posts/{StaticURLTests.post.id}/': 'posts/post_detail.html',
            '/create/': 'posts/create_post.html'
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)
