from django.core.management.base import BaseCommand
from django.utils.text import slugify
from main.models import Category, ContentItem
import os
from django.conf import settings


class Command(BaseCommand):
    help = 'Migrate hardcoded content from templates to database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be created without actually creating it',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No data will be created'))
        
        self.migrate_certifications(dry_run)
        self.migrate_internships(dry_run)
        self.migrate_hackathons(dry_run)
        self.migrate_gallery_items(dry_run)
        self.migrate_projects(dry_run)
        
        if not dry_run:
            self.stdout.write(self.style.SUCCESS('Migration complete!'))
        else:
            self.stdout.write(self.style.WARNING('DRY RUN complete - run without --dry-run to actually migrate'))

    def migrate_certifications(self, dry_run=False):
        """Migrate hardcoded certifications to database."""
        self.stdout.write('Migrating certifications...')
        
        # Get or create certifications category
        if not dry_run:
            cert_category, _ = Category.objects.get_or_create(
                slug='certifications',
                defaults={
                    'name': 'Certifications',
                    'description': 'Professional certifications and achievements',
                    'icon': 'fas fa-certificate',
                    'order': 5
                }
            )
        
        certifications = [
            {
                'title': 'Industrial Training on Machine Learning',
                'description': 'This certification demonstrates completion of an industrial training program focused on Machine Learning. It covers foundational techniques and tools essential for ML development.',
                'image_path': 'assets/img/cert1.jpg',
                'content_type': 'certification'
            },
            {
                'title': 'Applied ML Course',
                'description': 'This certificate was awarded for completing an Applied Machine Learning course offered by Reliance Foundation Skilling Academy. It includes hands-on projects and practical ML applications.',
                'image_path': 'assets/img/cert2.jpg',
                'content_type': 'certification'
            },
            {
                'title': 'Front-End Web Development',
                'description': 'This certificate from Reliance Foundation Skilling Academy reflects skills in Front-End Web Development, including HTML, CSS, and JavaScript fundamentals.',
                'image_path': 'assets/img/cert3.jpg',
                'content_type': 'certification'
            },
            {
                'title': 'Naukri Campus Young Turks Merit Certificate',
                'description': 'This certificate of merit was awarded as part of the Naukri Campus Young Turks program, recognizing excellence in specific technical and career-related skills.',
                'image_path': 'assets/img/cert4.png',
                'content_type': 'certification'
            },
            {
                'title': 'Basics of Python',
                'description': 'This certification from Infosys Springboard demonstrates foundational Python skills, covering essential programming concepts and problem-solving techniques.',
                'image_path': 'assets/img/cert5.jpg',
                'content_type': 'certification'
            },
            {
                'title': 'Cyber Security',
                'description': 'This certification from RELIANCE FOUNDATION demonstrates foundational CYBER SECURITY CONCEPTS.',
                'image_path': 'assets/img/cert6.jpg',
                'content_type': 'certification'
            },
            {
                'title': 'Project Manager Role, LinkedIn',
                'description': 'LinkedIn certification for Project Manager role and responsibilities.',
                'image_path': 'assets/img/cert7.jpg',
                'content_type': 'certification'
            },
            {
                'title': 'Python Foundation Certification',
                'description': 'Foundation level Python programming certification.',
                'image_path': 'assets/img/cert8.jpg',
                'content_type': 'certification'
            },
            {
                'title': 'Artificial Intelligence Fundamentals',
                'description': 'Certification covering fundamental concepts of Artificial Intelligence.',
                'image_path': 'assets/img/cert9.jpg',
                'content_type': 'certification'
            },
            {
                'title': 'ServiceNow IT Leadership',
                'description': 'ServiceNow certification for IT Leadership and management.',
                'image_path': 'assets/img/cert10.jpg',
                'content_type': 'certification'
            }
        ]
        
        for cert_data in certifications:
            slug = slugify(cert_data['title'])
            self.stdout.write(f'  - {cert_data["title"]} (slug: {slug})')
            
            if not dry_run:
                ContentItem.objects.get_or_create(
                    slug=slug,
                    defaults={
                        'category': cert_category,
                        'title': cert_data['title'],
                        'description': cert_data['description'],
                        'content_type': cert_data['content_type'],
                        'is_active': True,
                        'order': 0
                    }
                )

    def migrate_internships(self, dry_run=False):
        """Migrate hardcoded internships to database."""
        self.stdout.write('Migrating internships...')
        
        if not dry_run:
            intern_category, _ = Category.objects.get_or_create(
                slug='internships',
                defaults={
                    'name': 'Internships',
                    'description': 'Internship experiences and learning opportunities',
                    'icon': 'fas fa-user-tie',
                    'order': 6
                }
            )
        
        internships = [
            {
                'title': 'Internship at Techsaksham (a joint CSR initiative of Microsoft & SAP)',
                'description': 'This internship focused on advanced Machine Learning and AI. Project Topic: Implementation of ML model for image classification. Verification Link: https://techsaksham.org/verify-aicte-certificate/TSPIN24_601881',
                'image_path': 'assets/img/intern1.jpg',
                'pdf_path': 'assets/pdf/intern1.pdf',
                'content_type': 'internship'
            },
            {
                'title': 'Internship at Deloitte and Forage',
                'description': 'Deloitte Australia Technology Job Simulation on Forage - March 2025. Completed a job simulation involving development and coding. Wrote a proposal for creating a dashboard',
                'image_path': 'assets/img/intern2.jpg',
                'pdf_path': 'assets/pdf/intern2.pdf',
                'content_type': 'internship'
            },
            {
                'title': 'Internship at Edunet Foundation in collaboration with IBM SkillBuild',
                'description': 'This internship focused on advanced Machine Learning and AI. Project Topic: Employee Salary Prediction.',
                'image_path': 'assets/img/intern3.jpg',
                'pdf_path': 'assets/pdf/intern3.pdf',
                'content_type': 'internship'
            }
        ]
        
        for intern_data in internships:
            slug = slugify(intern_data['title'])
            self.stdout.write(f'  - {intern_data["title"]} (slug: {slug})')
            
            if not dry_run:
                ContentItem.objects.get_or_create(
                    slug=slug,
                    defaults={
                        'category': intern_category,
                        'title': intern_data['title'],
                        'description': intern_data['description'],
                        'content_type': intern_data['content_type'],
                        'is_active': True,
                        'order': 0
                    }
                )

    def migrate_hackathons(self, dry_run=False):
        """Migrate hardcoded hackathons to database."""
        self.stdout.write('Migrating hackathons...')
        
        if not dry_run:
            hack_category, _ = Category.objects.get_or_create(
                slug='hackathons',
                defaults={
                    'name': 'Hackathons',
                    'description': 'Hackathon participations and achievements',
                    'icon': 'fas fa-trophy',
                    'order': 7
                }
            )
        
        hackathons = [
            {
                'title': 'Hackathon 1',
                'description': 'No Details Available.',
                'image_path': 'assets/img/hack1.png',
                'content_type': 'hackathon'
            },
            {
                'title': 'Google Solution Challenge 2025',
                'description': 'The Google Solution Challenge 2025 is an annual global competition organized by Google Developer Student Clubs (GDSC), inviting university students to develop innovative solutions to real-world problems using Google technologies. The primary mission is to address one or more of the United Nations\' 17 Sustainable Development Goals (SDGs), which range from ending poverty and ensuring quality education to promoting climate action and gender equality.',
                'image_path': 'assets/img/image-7.png',
                'content_type': 'hackathon'
            }
        ]
        
        for hack_data in hackathons:
            slug = slugify(hack_data['title'])
            self.stdout.write(f'  - {hack_data["title"]} (slug: {slug})')
            
            if not dry_run:
                ContentItem.objects.get_or_create(
                    slug=slug,
                    defaults={
                        'category': hack_category,
                        'title': hack_data['title'],
                        'description': hack_data['description'],
                        'content_type': hack_data['content_type'],
                        'is_active': True,
                        'order': 0
                    }
                )

    def migrate_gallery_items(self, dry_run=False):
        """Migrate hardcoded gallery items to database."""
        self.stdout.write('Migrating gallery items...')
        
        if not dry_run:
            gallery_category, _ = Category.objects.get_or_create(
                slug='gallery',
                defaults={
                    'name': 'Gallery',
                    'description': 'Photos and memorable moments',
                    'icon': 'fas fa-images',
                    'order': 8
                }
            )
        
        gallery_items = [
            {
                'title': 'Scholar Merchandise',
                'description': 'Scholar merchandise and recognition items.',
                'image_path': 'assets/img/image1.jpg',
                'content_type': 'gallery'
            },
            {
                'title': 'NIIT Industrial Training Batch 2024',
                'description': 'Group photo from NIIT Industrial Training Batch 2024.',
                'image_path': 'assets/img/image2.jpg',
                'content_type': 'gallery'
            },
            {
                'title': 'Anti-Ragging Ceremony',
                'description': 'Participation in Anti-Ragging Ceremony.',
                'image_path': 'assets/img/image3.jpg',
                'content_type': 'gallery'
            },
            {
                'title': 'Selection Letter of RF Scholarship',
                'description': 'Selection letter for RF Scholarship program.',
                'image_path': 'assets/img/image4.jpg',
                'content_type': 'gallery'
            },
            {
                'title': 'BCA 2022-2025 BATCH',
                'description': 'BCA batch photo for 2022-2025 academic years.',
                'image_path': 'assets/img/image5.jpg',
                'content_type': 'gallery'
            }
        ]
        
        for gallery_data in gallery_items:
            slug = slugify(gallery_data['title'])
            self.stdout.write(f'  - {gallery_data["title"]} (slug: {slug})')
            
            if not dry_run:
                ContentItem.objects.get_or_create(
                    slug=slug,
                    defaults={
                        'category': gallery_category,
                        'title': gallery_data['title'],
                        'description': gallery_data['description'],
                        'content_type': gallery_data['content_type'],
                        'is_active': True,
                        'order': 0
                    }
                )

    def migrate_projects(self, dry_run=False):
        """Migrate hardcoded projects to database."""
        self.stdout.write('Migrating projects...')
        
        if not dry_run:
            project_category, _ = Category.objects.get_or_create(
                slug='experience',
                defaults={
                    'name': 'Experience',
                    'description': 'Professional work experience and projects',
                    'icon': 'fas fa-briefcase',
                    'order': 2
                }
            )
        
        projects = [
            {
                'title': 'Image Recognition System',
                'short_description': 'Advanced image recognition using machine learning',
                'description': 'An advanced image recognition system built using machine learning algorithms and computer vision techniques.',
                'technologies': 'Python, TensorFlow, OpenCV, Machine Learning',
                'content_type': 'project',
                'video_path': 'assets/videos/trial (2).mp4'
            },
            {
                'title': 'Crypto Prediction',
                'short_description': 'Cryptocurrency price prediction model',
                'description': 'A machine learning model for predicting cryptocurrency prices using historical data and market indicators.',
                'technologies': 'Python, Pandas, Scikit-learn, Financial APIs',
                'content_type': 'project',
                'video_path': 'assets/videos/crypto_prediction.mkv'
            },
            {
                'title': 'Stock Price Prediction',
                'short_description': 'Stock market prediction using AI',
                'description': 'An AI-powered system for predicting stock prices using various market indicators and historical data.',
                'technologies': 'Python, TensorFlow, Financial Data APIs, Time Series Analysis',
                'content_type': 'project',
                'video_path': 'assets/videos/stock_price_prediction.mkv'
            },
            {
                'title': 'Salary Prediction',
                'short_description': 'Employee salary prediction model',
                'description': 'A machine learning model that predicts employee salaries based on various factors like experience, education, and location.',
                'technologies': 'Python, Scikit-learn, Data Analysis, Regression Models',
                'content_type': 'project',
                'video_path': 'assets/videos/2025-08-01 20-02-16 (online-video-cutter.com) (1).mkv'
            }
        ]
        
        for project_data in projects:
            slug = slugify(project_data['title'])
            self.stdout.write(f'  - {project_data["title"]} (slug: {slug})')
            
            if not dry_run:
                ContentItem.objects.get_or_create(
                    slug=slug,
                    defaults={
                        'category': project_category,
                        'title': project_data['title'],
                        'short_description': project_data['short_description'],
                        'description': project_data['description'],
                        'technologies': project_data['technologies'],
                        'content_type': project_data['content_type'],
                        'is_active': True,
                        'is_featured': True,
                        'order': 0
                    }
                )