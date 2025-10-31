from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Category, ContentItem, PersonalInfo, ContactMessage


class PortfolioTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Create test data
        self.category = Category.objects.create(
            name="Test Projects",
            slug="test-projects",
            description="Test category"
        )
        
        self.content_item = ContentItem.objects.create(
            category=self.category,
            title="Test Project",
            slug="test-project",
            description="Test project description",
            content_type="project"
        )
        
        self.personal_info = PersonalInfo.objects.create(
            name="Test User",
            title="Test Developer",
            location="Test City",
            email="test@example.com",
            bio="Test bio"
        )

    def test_home_page(self):
        """Test that home page loads successfully."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test User")

    def test_category_detail(self):
        """Test category detail page."""
        response = self.client.get(reverse('category_detail', kwargs={'slug': self.category.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.category.name)

    def test_content_detail(self):
        """Test content detail page."""
        response = self.client.get(reverse('content_detail', kwargs={'slug': self.content_item.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.content_item.title)

    def test_contact_form_submission(self):
        """Test contact form submission."""
        form_data = {
            'name': 'Test Contact',
            'email': 'contact@example.com',
            'phone': '1234567890',
            'message': 'Test message'
        }
        response = self.client.post(reverse('contact'), data=form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful submission
        
        # Check that message was saved
        self.assertTrue(ContactMessage.objects.filter(email='contact@example.com').exists())

    def test_models_str_methods(self):
        """Test string representations of models."""
        self.assertEqual(str(self.category), "Test Projects")
        self.assertEqual(str(self.content_item), "Test Project (Test Projects)")
        self.assertEqual(str(self.personal_info), "Test User")