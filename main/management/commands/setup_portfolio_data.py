from django.core.management.base import BaseCommand
from django.utils.text import slugify
from main.models import Category, ContentItem, PersonalInfo


class Command(BaseCommand):
    help = 'Setup initial portfolio data with categories and sample content'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Reset all data before creating new data',
        )
        parser.add_argument(
            '--sample-only',
            action='store_true',
            help='Only create sample data, skip categories setup',
        )

    def handle(self, *args, **options):
        if options['reset']:
            self.stdout.write('Resetting all portfolio data...')
            ContentItem.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Data reset complete.'))

        if not options['sample_only']:
            self.create_categories()
        
        self.create_sample_content()
        self.create_personal_info()
        
        self.stdout.write(self.style.SUCCESS('Portfolio setup complete!'))

    def create_categories(self):
        """Create the main portfolio categories."""
        categories_data = [
            {
                'name': 'Skills',
                'slug': 'skills',
                'description': 'Technical skills and competencies',
                'icon': 'fas fa-code',
                'order': 1
            },
            {
                'name': 'Experience',
                'slug': 'experience',
                'description': 'Professional work experience and projects',
                'icon': 'fas fa-briefcase',
                'order': 2
            },
            {
                'name': 'Projects',
                'slug': 'projects',
                'description': 'Personal and professional projects',
                'icon': 'fas fa-laptop-code',
                'order': 3
            },
            {
                'name': 'Education',
                'slug': 'education',
                'description': 'Educational background and qualifications',
                'icon': 'fas fa-graduation-cap',
                'order': 4
            },
            {
                'name': 'Certifications',
                'slug': 'certifications',
                'description': 'Professional certifications and achievements',
                'icon': 'fas fa-certificate',
                'order': 5
            },
            {
                'name': 'Internships',
                'slug': 'internships',
                'description': 'Internship experiences and learning opportunities',
                'icon': 'fas fa-user-tie',
                'order': 6
            },
            {
                'name': 'Hackathons',
                'slug': 'hackathons',
                'description': 'Hackathon participations and achievements',
                'icon': 'fas fa-trophy',
                'order': 7
            },
            {
                'name': 'Gallery',
                'slug': 'gallery',
                'description': 'Photos and memorable moments',
                'icon': 'fas fa-images',
                'order': 8
            },
            {
                'name': 'Interests',
                'slug': 'interests',
                'description': 'Personal interests and hobbies',
                'icon': 'fas fa-heart',
                'order': 9
            }
        ]

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')
            else:
                self.stdout.write(f'Category already exists: {category.name}')

    def create_sample_content(self):
        """Create sample content items for demonstration."""
        
        # Get or create categories
        skills_cat, _ = Category.objects.get_or_create(slug='skills', defaults={'name': 'Skills'})
        projects_cat, _ = Category.objects.get_or_create(slug='projects', defaults={'name': 'Projects'})
        experience_cat, _ = Category.objects.get_or_create(slug='experience', defaults={'name': 'Experience'})
        
        # Sample skills
        skills_data = [
            {
                'title': 'Python Programming',
                'description': 'Advanced proficiency in Python for web development, data analysis, and machine learning.',
                'technologies': 'Python, Django, Flask, FastAPI, NumPy, Pandas',
                'content_type': 'skill'
            },
            {
                'title': 'Web Development',
                'description': 'Full-stack web development using modern frameworks and technologies.',
                'technologies': 'HTML5, CSS3, JavaScript, React, Vue.js, Django, Node.js',
                'content_type': 'skill'
            },
            {
                'title': 'Machine Learning',
                'description': 'Experience with machine learning algorithms and deep learning frameworks.',
                'technologies': 'TensorFlow, PyTorch, Scikit-learn, Keras, OpenCV',
                'content_type': 'skill'
            },
            {
                'title': 'Database Management',
                'description': 'Design and management of relational and NoSQL databases.',
                'technologies': 'PostgreSQL, MySQL, MongoDB, Redis, SQLite',
                'content_type': 'skill'
            }
        ]

        for skill_data in skills_data:
            skill_data['category'] = skills_cat
            skill_data['slug'] = slugify(skill_data['title'])
            ContentItem.objects.get_or_create(
                slug=skill_data['slug'],
                defaults=skill_data
            )

        # Sample projects
        projects_data = [
            {
                'title': 'E-commerce Platform',
                'short_description': 'Full-featured e-commerce platform with payment integration',
                'description': 'A comprehensive e-commerce platform built with Django and React. Features include user authentication, product catalog, shopping cart, payment processing, and admin dashboard.',
                'technologies': 'Django, React, PostgreSQL, Stripe API, Redis',
                'content_type': 'project',
                'is_featured': True,
                'github_url': 'https://github.com/example/ecommerce',
                'demo_url': 'https://demo-ecommerce.example.com'
            },
            {
                'title': 'Task Management App',
                'short_description': 'Collaborative task management application',
                'description': 'A collaborative task management application with real-time updates, team collaboration features, and project tracking capabilities.',
                'technologies': 'Vue.js, Node.js, Socket.io, MongoDB',
                'content_type': 'project',
                'github_url': 'https://github.com/example/taskmanager'
            },
            {
                'title': 'Data Visualization Dashboard',
                'short_description': 'Interactive dashboard for business analytics',
                'description': 'An interactive dashboard for visualizing business data with charts, graphs, and real-time analytics. Built with modern web technologies.',
                'technologies': 'React, D3.js, Python, FastAPI, PostgreSQL',
                'content_type': 'project',
                'is_featured': True
            }
        ]

        for project_data in projects_data:
            project_data['category'] = projects_cat
            project_data['slug'] = slugify(project_data['title'])
            ContentItem.objects.get_or_create(
                slug=project_data['slug'],
                defaults=project_data
            )

        self.stdout.write(self.style.SUCCESS('Sample content created successfully!'))

    def create_personal_info(self):
        """Create or update personal information."""
        personal_info, created = PersonalInfo.objects.get_or_create(
            id=1,
            defaults={
                'name': 'Your Name',
                'title': 'Full Stack Developer',
                'location': 'Your City, Country',
                'email': 'your.email@example.com',
                'phone': '+1234567890',
                'bio': 'Passionate full-stack developer with expertise in modern web technologies. I love creating innovative solutions and learning new technologies.',
                'linkedin_url': 'https://linkedin.com/in/yourprofile',
                'github_url': 'https://github.com/yourprofile',
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('Personal information created. Please update it in the admin panel.'))
        else:
            self.stdout.write('Personal information already exists.')