from django.core.management.base import BaseCommand
from django.utils.text import slugify
from main.models import Category, ContentItem, PersonalInfo


class Command(BaseCommand):
    help = 'Populate initial data for the portfolio'

    def handle(self, *args, **options):
        self.stdout.write('Populating initial data...')

        # Create Personal Info
        personal_info, created = PersonalInfo.objects.get_or_create(
            defaults={
                'name': 'Gourab Gorai',
                'title': '',
                'location': 'WEST BENGAL, INDIA',
                'email': 'gourabg30march@gmail.com',
                'bio': '''I am Gourab Gorai, a driven and innovative computer science enthusiast with a strong foundation in programming and machine learning. I have completed Bachelor of Computer Application (BCA) from Dr. B.C. Roy Academy of Professional Courses, graduate in 2025. I completed my higher-secondary education in Commerce from Bidhan Chandra Institution in 2022 and my secondary education from Durgapur Ispat Vidyalaya in 2020. As a scholar of the Reliance Foundation Scholarships, 2022, I am committed to leveraging technology to solve real-world problems. My technical skills include proficiency in Python, Java, Machine Learning, DBMS, HTML, CSS, and JavaScript. I have earned certifications in Machine Learning using Python from the National Institute for Industrial Training and Front-End Web Development from the Reliance Foundation Skill Academy. I also completed an internship in AI with TechSaksham, under the guidance of Microsoft, SAP, AICTE, and Edunet Foundation. Some of my projects include an Image Recognition System using Logistic Regression, Crypto Prediction using Linear Regression, and Stock Price Prediction using Random Forest, all of which showcase my expertise in machine learning. In my free time, I enjoy watching movies, web series, and staying updated with the latest tech news.''',
                'linkedin_url': 'https://www.linkedin.com/in/gourab-gorai-4a51541ba',
                'github_url': 'https://github.com/GourabGorai',
                'facebook_url': 'https://www.facebook.com/gourab.gorai.986',
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created personal info'))

        # Create Categories
        categories_data = [
            {'name': 'Projects', 'icon': 'fas fa-code', 'order': 1, 'slug': 'experience'},
            {'name': 'Education', 'icon': 'fas fa-graduation-cap', 'order': 2, 'slug': 'education'},
            {'name': 'Skills', 'icon': 'fas fa-cogs', 'order': 3, 'slug': 'skills'},
            {'name': 'Hobbies', 'icon': 'fas fa-heart', 'order': 4, 'slug': 'interests'},
            {'name': 'Internships', 'icon': 'fas fa-briefcase', 'order': 5, 'slug': 'internships'},
            {'name': 'Gallery', 'icon': 'fas fa-images', 'order': 6, 'slug': 'gallery'},
            {'name': 'Certifications', 'icon': 'fas fa-certificate', 'order': 7, 'slug': 'certifications'},
            {'name': 'Hackathons', 'icon': 'fas fa-trophy', 'order': 8, 'slug': 'hackathons'},
        ]

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'slug': cat_data['slug'],
                    'icon': cat_data['icon'],
                    'order': cat_data['order'],
                    'description': f'Explore my {cat_data["name"].lower()}',
                }
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create sample content items
        projects_category = Category.objects.get(name='Projects')
        
        projects_data = [
            {
                'title': 'Image Recognition System',
                'content_type': 'project',
                'description': 'An advanced image recognition system built using logistic regression and machine learning techniques. The system can classify and identify various objects in images with high accuracy.',
                'short_description': 'Logistic Regression, Machine Learning',
                'technologies': 'Python, Scikit-learn, OpenCV, NumPy, Pandas',
                'is_featured': True,
            },
            {
                'title': 'Crypto Prediction',
                'content_type': 'project',
                'description': 'A cryptocurrency price prediction model using linear regression to forecast market trends and price movements.',
                'short_description': 'Linear Regression, Machine Learning',
                'technologies': 'Python, Pandas, Matplotlib, Scikit-learn',
                'is_featured': True,
            },
            {
                'title': 'Stock Price Prediction',
                'content_type': 'project',
                'description': 'A comprehensive stock price prediction system using Random Forest algorithm to analyze market data and predict future stock prices.',
                'short_description': 'Random Forest, Machine Learning',
                'technologies': 'Python, Random Forest, Pandas, NumPy',
                'is_featured': True,
            },
            {
                'title': 'Salary Prediction',
                'content_type': 'project',
                'description': 'An employee salary prediction model using Random Forest to estimate salaries based on various factors like experience, education, and location.',
                'short_description': 'Random Forest, Machine Learning',
                'technologies': 'Python, Random Forest, Data Analysis',
                'is_featured': False,
            },
        ]

        for project_data in projects_data:
            content_item, created = ContentItem.objects.get_or_create(
                title=project_data['title'],
                category=projects_category,
                defaults={
                    'slug': slugify(project_data['title']),
                    'content_type': project_data['content_type'],
                    'description': project_data['description'],
                    'short_description': project_data['short_description'],
                    'technologies': project_data['technologies'],
                    'is_featured': project_data['is_featured'],
                }
            )
            if created:
                self.stdout.write(f'Created project: {content_item.title}')

        # Create Education items
        education_category = Category.objects.get(name='Education')
        
        education_data = [
            {
                'title': 'DR. B.C. Roy Academy of Professional Courses',
                'description': 'Bachelor of Computer Application (BCA) - Comprehensive study of computer science fundamentals, programming languages, and software development.',
                'short_description': 'Bachelor of Computer Application (BCA)',
                'start_date': '2022-01-01',
                'end_date': '2025-01-01',
            },
            {
                'title': 'Bidhan Chandra Institution',
                'description': 'Higher Secondary Education in Commerce - Focused on business studies, economics, and mathematics.',
                'short_description': 'Higher Secondary Education - Commerce',
                'end_date': '2022-01-01',
            },
            {
                'title': 'Durgapur Ispat Vidyalaya',
                'description': 'Secondary Education - Foundation in science, mathematics, and general studies.',
                'short_description': 'Secondary Education',
                'end_date': '2020-01-01',
            },
        ]

        for edu_data in education_data:
            from datetime import datetime
            start_date = datetime.strptime(edu_data.get('start_date', '2020-01-01'), '%Y-%m-%d').date() if edu_data.get('start_date') else None
            end_date = datetime.strptime(edu_data['end_date'], '%Y-%m-%d').date()
            
            content_item, created = ContentItem.objects.get_or_create(
                title=edu_data['title'],
                category=education_category,
                defaults={
                    'slug': slugify(edu_data['title']),
                    'content_type': 'education',
                    'description': edu_data['description'],
                    'short_description': edu_data['short_description'],
                    'start_date': start_date,
                    'end_date': end_date,
                }
            )
            if created:
                self.stdout.write(f'Created education: {content_item.title}')

        # Create Skills
        skills_category = Category.objects.get(name='Skills')
        
        skills_data = [
            {'title': 'Python (Intermediate)', 'description': 'Intermediate level proficiency in Python programming'},
            {'title': 'Java (Beginner)', 'description': 'Beginner level knowledge of Java programming'},
            {'title': 'Machine Learning', 'description': 'Experience with ML algorithms and frameworks'},
            {'title': 'DBMS (Beginner)', 'description': 'Database management and SQL'},
            {'title': 'HTML (Intermediate)', 'description': 'Web markup and structure'},
            {'title': 'CSS (Beginner)', 'description': 'Styling and responsive design'},
            {'title': 'JavaScript (Beginner)', 'description': 'Client-side scripting and interactivity'},
        ]

        for skill_data in skills_data:
            content_item, created = ContentItem.objects.get_or_create(
                title=skill_data['title'],
                category=skills_category,
                defaults={
                    'slug': slugify(skill_data['title']),
                    'content_type': 'skill',
                    'description': skill_data['description'],
                }
            )
            if created:
                self.stdout.write(f'Created skill: {content_item.title}')

        # Create Hobbies
        hobbies_category = Category.objects.get(name='Hobbies')
        
        hobbies_item, created = ContentItem.objects.get_or_create(
            title='Hobbies & Interests',
            category=hobbies_category,
            defaults={
                'slug': 'hobbies-interests',
                'content_type': 'other',
                'description': 'Watching movies and web series, tech news enthusiast.',
            }
        )
        if created:
            self.stdout.write(f'Created hobby: {hobbies_item.title}')

        # Create Internships
        internships_category = Category.objects.get(name='Internships')
        
        internships_data = [
            {
                'title': 'Internship at Techsaksham (a joint CSR initiative of Microsoft & SAP)',
                'description': 'This internship focused on advanced Machine Learning and AI. Project Topic: Implementation of ML model for image classification. Verification Link: https://techsaksham.org/verify-aicte-certificate/TSPIN24_601881',
                'short_description': 'AI & Machine Learning Internship',
            },
            {
                'title': 'Internship at Deloitte and Forage',
                'description': 'Deloitte Australia Technology Job Simulation on Forage - March 2025. Completed a job simulation involving development and coding. Wrote a proposal for creating a dashboard',
                'short_description': 'Technology Job Simulation',
            },
            {
                'title': 'Internship at Edunet Foundation in collaboration with IBM SkillBuild',
                'description': 'This internship focused on advanced Machine Learning and AI. Project Topic: Employee Salary Prediction.',
                'short_description': 'AI & Machine Learning Internship',
            },
        ]

        for internship_data in internships_data:
            content_item, created = ContentItem.objects.get_or_create(
                title=internship_data['title'],
                category=internships_category,
                defaults={
                    'slug': slugify(internship_data['title']),
                    'content_type': 'experience',
                    'description': internship_data['description'],
                    'short_description': internship_data['short_description'],
                }
            )
            if created:
                self.stdout.write(f'Created internship: {content_item.title}')

        # Create Gallery Items
        gallery_category = Category.objects.get(name='Gallery')
        
        gallery_data = [
            {'title': 'Scholar Merchandise', 'description': 'Reliance Foundation Scholarship merchandise'},
            {'title': 'NIIT Industrial Training Batch 2024', 'description': 'Group photo from NIIT Industrial Training'},
            {'title': 'Anti-Ragging Ceremony', 'description': 'College anti-ragging ceremony participation'},
            {'title': 'Selection Letter of RF Scholarship', 'description': 'Official selection letter for Reliance Foundation Scholarship'},
            {'title': 'BCA 2022-2025 BATCH', 'description': 'BCA batch group photo'},
        ]

        for gallery_data_item in gallery_data:
            content_item, created = ContentItem.objects.get_or_create(
                title=gallery_data_item['title'],
                category=gallery_category,
                defaults={
                    'slug': slugify(gallery_data_item['title']),
                    'content_type': 'gallery',
                    'description': gallery_data_item['description'],
                }
            )
            if created:
                self.stdout.write(f'Created gallery item: {content_item.title}')

        # Create Certifications
        certifications_category = Category.objects.get(name='Certifications')
        
        certifications_data = [
            {'title': 'INDUSTRIAL TRAINING ON MACHINE LEARNING', 'description': 'This certification demonstrates completion of an industrial training program focused on Machine Learning. It covers foundational techniques and tools essential for ML development.'},
            {'title': 'APPLIED ML COURSE', 'description': 'This certificate was awarded for completing an Applied Machine Learning course offered by Reliance Foundation Skilling Academy. It includes hands-on projects and practical ML applications.'},
            {'title': 'FRONT-END WEB DEVELOPMENT', 'description': 'This certificate from Reliance Foundation Skilling Academy reflects skills in Front-End Web Development, including HTML, CSS, and JavaScript fundamentals.'},
            {'title': 'NAUKRI CAMPUS YOUNG TURKS MERIT CERTIFICATE', 'description': 'This certificate of merit was awarded as part of the Naukri Campus Young Turks program, recognizing excellence in specific technical and career-related skills.'},
            {'title': 'BASICS OF PYTHON', 'description': 'This certification from Infosys Springboard demonstrates foundational Python skills, covering essential programming concepts and problem-solving techniques.'},
            {'title': 'CYBER SECURITY', 'description': 'This certification from RELIANCE FOUNDATION demonstrates foundational CYBER SECURITY CONCEPTS.'},
            {'title': 'Project Manager ROLE, LinkedIn', 'description': 'LinkedIn certification for Project Manager role'},
            {'title': 'Python Foundation Certification', 'description': 'Foundation level Python programming certification'},
            {'title': 'Artificial Intelligence Fundamentals', 'description': 'Basic concepts and fundamentals of Artificial Intelligence'},
            {'title': 'ServiceNow IT Leadership', 'description': 'IT Leadership certification from ServiceNow'},
        ]

        for cert_data in certifications_data:
            content_item, created = ContentItem.objects.get_or_create(
                title=cert_data['title'],
                category=certifications_category,
                defaults={
                    'slug': slugify(cert_data['title']),
                    'content_type': 'certification',
                    'description': cert_data['description'],
                }
            )
            if created:
                self.stdout.write(f'Created certification: {content_item.title}')

        # Create Hackathons
        hackathons_category = Category.objects.get(name='Hackathons')
        
        hackathons_data = [
            {'title': 'Hackathon 1', 'description': 'No Details Available.'},
            {'title': 'Google Solution Challenge 2025', 'description': 'The Google Solution Challenge 2025 is an annual global competition organized by Google Developer Student Clubs (GDSC), inviting university students to develop innovative solutions to real-world problems using Google technologies. The primary mission is to address one or more of the United Nations\' 17 Sustainable Development Goals (SDGs), which range from ending poverty and ensuring quality education to promoting climate action and gender equality.'},
        ]

        for hackathon_data in hackathons_data:
            content_item, created = ContentItem.objects.get_or_create(
                title=hackathon_data['title'],
                category=hackathons_category,
                defaults={
                    'slug': slugify(hackathon_data['title']),
                    'content_type': 'other',
                    'description': hackathon_data['description'],
                }
            )
            if created:
                self.stdout.write(f'Created hackathon: {content_item.title}')

        self.stdout.write(self.style.SUCCESS('Successfully populated initial data!'))