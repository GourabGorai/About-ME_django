# Django Portfolio Application

A modern, responsive portfolio website built with Django, featuring an admin panel for easy content management.

## Features

- **Dynamic Content Management**: Add and manage categories, projects, skills, education, and more through Django admin
- **Responsive Design**: Beautiful, mobile-friendly interface with Bootstrap
- **Interactive Elements**: Particle backgrounds, animations, and smooth scrolling
- **Media Support**: Upload images, videos, and PDF files for your content
- **Contact Form**: Built-in contact form with message storage
- **Admin Dashboard**: Full-featured admin panel for content management

## Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd portfolio
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv portfolio_env
   
   # On Windows:
   portfolio_env\Scripts\activate
   
   # On Linux/Mac:
   source portfolio_env/bin/activate
   ```

3. **Run the setup script**
   ```bash
   python setup.py
   ```
   
   This will:
   - Install all required packages
   - Set up the database
   - Create initial data
   - Prompt you to create an admin user

4. **Start the development server**
   ```bash
   python manage.py runserver
   ```

5. **Open your browser**
   - Portfolio: http://127.0.0.1:8000
   - Admin Panel: http://127.0.0.1:8000/admin

## Manual Setup (Alternative)

If you prefer to set up manually:

```bash
# Install dependencies
pip install -r requirements.txt

# Create database
python manage.py makemigrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Load sample data
python manage.py populate_data

# Collect static files
python manage.py collectstatic

# Run server
python manage.py runserver
```

## Admin Panel Usage

### Adding Content

1. **Personal Information**
   - Go to Admin → Personal Information
   - Add your name, bio, contact details, and social links
   - Upload profile image and resume

2. **Categories**
   - Go to Admin → Categories
   - Create categories like "Projects", "Skills", "Education"
   - Set icons using FontAwesome classes (e.g., "fas fa-code")
   - Set display order

3. **Content Items**
   - Go to Admin → Content Items
   - Add projects, skills, education entries, etc.
   - Upload images, videos, or PDF files
   - Set technologies used, GitHub links, demo URLs
   - Mark items as featured to highlight them

4. **Contact Messages**
   - View messages submitted through the contact form
   - Mark messages as read/unread

### Content Types

- **Projects**: Showcase your work with descriptions, technologies, media
- **Skills**: List your technical skills and proficiency levels
- **Education**: Add your educational background
- **Experience**: Work experience and internships
- **Certifications**: Professional certifications and achievements
- **Gallery**: Photo galleries and visual content
- **Other**: Any other type of content

## Customization

### Styling
- Edit `static/css/styles.css` for custom styles
- Modify templates in `templates/main/` for layout changes

### Adding New Features
- Create new models in `main/models.py`
- Add corresponding admin configurations in `main/admin.py`
- Update templates and views as needed

## File Structure

```
portfolio/
├── main/                   # Main Django app
│   ├── models.py          # Database models
│   ├── admin.py           # Admin configurations
│   ├── views.py           # View functions
│   └── forms.py           # Form definitions
├── templates/             # HTML templates
├── static/               # Static files (CSS, JS, images)
├── media/                # User uploaded files
├── portfolio/            # Django project settings
└── manage.py             # Django management script
```

## Technologies Used

- **Backend**: Django 4.2+
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Database**: SQLite (default, easily changeable)
- **Media**: Pillow for image handling
- **Animations**: AOS (Animate On Scroll)
- **Particles**: tsParticles for background effects

## Deployment

For production deployment:

1. Set `DEBUG=False` in settings
2. Configure proper database (PostgreSQL recommended)
3. Set up static file serving
4. Configure media file handling
5. Use environment variables for sensitive settings

## Support

If you encounter any issues:

1. Check that all requirements are installed
2. Ensure you're in the correct virtual environment
3. Verify database migrations are applied
4. Check the Django debug output for specific errors

## License

This project is open source and available under the MIT License.
