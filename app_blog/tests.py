from datetime import datetime
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Blog, Files

NUMBER_OF_BLOGS = 10
USER_LOGIN = 'jacob'
USER_PASSWORD = '123456'
USER_EMAIL = '123456@jacob.com'


class BlogsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username=USER_LOGIN, email=USER_EMAIL, password=USER_PASSWORD)
        for blog_index in range(NUMBER_OF_BLOGS):
            Blog.objects.create(
                topic=f'topic {blog_index}',
                description=f'description {blog_index}',
                created_at=datetime.now(),
                author=user,
            )

    def test_blogs_exist_at_desired_location(self):
        url = reverse('main_page')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/main_page.html')

    def test_blogs_number(self):
        url = reverse('main_page')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['blogs']) == NUMBER_OF_BLOGS)

    def test_add_blogs_exist_at_desired_location(self):
        url = reverse('add_blog')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/add_blog.html')

    def test_add_blogs_post_correctly(self):
        url = reverse('add_blog')
        client = Client()
        client.login(username=USER_LOGIN, password=USER_PASSWORD)
        response = client.post(url, {
            'topic': 'TEST topic',
            'description': 'TEST description',
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/main_page.html')
        self.assertTrue(len(response.context['blogs']) == NUMBER_OF_BLOGS + 1)

    def test_blog_detail_exists_at_desired_location(self):
        for NUMBER_OF_BLOG in range(1, NUMBER_OF_BLOGS + 1):
            response = self.client.get(f'/blog/{NUMBER_OF_BLOG}/')
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'blog/blog_detail.html')

    def test_blog_detail_has_all_files_after_adding(self):
        url = reverse('add_blog')
        client = Client()
        client.login(username=USER_LOGIN, password=USER_PASSWORD)
        from io import BytesIO
        number_of_files = 3
        files = [BytesIO(b'data') for _ in range(number_of_files)]
        client.post(url, {
            'topic': 'TEST topic',
            'description': 'TEST description',
            'file_field': files,
        }, follow=True)
        response = self.client.get(f'/blog/{NUMBER_OF_BLOGS + 1}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog_detail.html')
        file = Files.objects.filter(blog_id=NUMBER_OF_BLOGS + 1)
        self.assertEqual(set(response.context['files'].all()), set(file))

    def test_blog_update_exists_at_desired_location(self):
        url = reverse('update_blogs')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/file_form_upload.html')

    def test_blog_update_changes_blogs(self):
        initial_blogs = {}
        blogs = Blog.objects.all()
        for blog in blogs:
            initial_blogs[blog.id] = [blog.description, blog.created_at]
        url = reverse('update_blogs')
        with open('additional_materials/csv_data_updater_example.csv', 'r') as file:
            response = self.client.post(url, {'file_field': file})
        self.assertEqual(response.status_code, 200)
        url = reverse('main_page')
        response = self.client.get(url)
        for blog_id, blog_info in initial_blogs.items():
            page_blog = response.context['blogs'].get(id=blog_id)
            self.assertNotEqual(page_blog.description, blog_info[0])
            self.assertNotEqual(page_blog.created_at, blog_info[1])
