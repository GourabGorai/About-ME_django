# 🎨 Django Portfolio Website

A modern, responsive portfolio website built with Django, featuring a comprehensive admin panel for dynamic content management. Perfect for developers, designers, and professionals who want to showcase their work with a professional online presence.

## ✨ Features

### 🎯 **Dynamic Content Management**
- **Admin Panel**: Professional interface for managing all content
- **Categories**: Organize content into Skills, Projects, Certifications, etc.
- **Media Upload**: Support for images, videos, PDFs, and HTML files
- **Bulk Operations**: Efficiently manage multiple items at once
- **Real-time Statistics**: Dashboard with content metrics

### 🎨 **Modern Design**
- **Responsive Layout**: Mobile-first design that works on all devices
- **Professional UI**: Clean, modern interface with smooth animations
- **Interactive Elements**: Video players, image galleries, modal popups
- **SEO Optimized**: Clean URLs, meta tags, and structured data

### 🚀 **Advanced Features**
- **Contact Form**: Built-in contact form with message management
- **Featured Content**: Highlight your best work on the homepage
- **Search & Filter**: Easy content discovery and organization
- **Custom HTML Pages**: Upload custom project detail pages
- **Social Integration**: Links to your social media profiles

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/GourabGorai/About-ME_django.git
   cd About-ME_django
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Setup database**
   ```bash
   python manage.py migrate
   python manage.py setup_portfolio_data
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - **Website**: http://127.0.0.1:8000/
   - **Admin Panel**: http://127.0.0.1:8000/admin/

## 🌐 Deployment

### Render (Recommended)
This project is optimized for Render deployment with automatic setup:

1. **Fork this repository**
2. **Connect to Render**
3. **Deploy with one click**

See [RENDER_DEPLOYMENT_GUIDE.md](RENDER_DEPLOYMENT_GUIDE.md) for detailed instructions.

### Other Platforms
- **Heroku**: Use the included `Procfile`
- **Railway**: Automatic deployment from GitHub
- **DigitalOcean**: App Platform compatible
- **AWS**: Elastic Beanstalk ready

## 📊 Project Structure

```
portfolio/
├── main/                          # Main Django app
│   ├── management/commands/       # Custom management commands
│   ├── migrations/               # Database migrations
│   ├── templates/               # HTML templates
│   ├── admin.py                # Admin configuration
│   ├── models.py               # Database models
│   ├── views.py                # View functions
│   └── urls.py                 # URL routing
├── portfolio/                   # Django project settings
├── static/                     # Static files (CSS, JS, images)
├── templates/                  # Global templates
├── media/                      # User uploaded files
├── requirements.txt            # Python dependencies
├── build.sh                   # Render build script
├── render.yaml                # Render configuration
└── manage.py                  # Django management script
```

## 🛠️ Management Commands

### Setup Commands
```bash
# Setup initial categories and sample data
python manage.py setup_portfolio_data

# Migrate existing hardcoded content to database
python manage.py migrate_hardcoded_content

# Create superuser with environment variables
python manage.py create_superuser
```

### Maintenance Commands
```bash
# Collect static files
python manage.py collectstatic

# Run database migrations
python manage.py migrate

# Create database backup
python manage.py dumpdata > backup.json
```

## 📚 Documentation

- **[Admin Panel Guide](ADMIN_PANEL_ENHANCED_GUIDE.md)** - Complete admin interface guide
- **[Deployment Guide](RENDER_DEPLOYMENT_GUIDE.md)** - Render deployment instructions
- **[Media Fix Guide](PROJECT_MEDIA_FIX_GUIDE.md)** - Troubleshooting media files
- **[Setup Instructions](SETUP_INSTRUCTIONS.md)** - Detailed setup guide

## 🎯 Key Components

### Models
- **Category**: Portfolio sections (Skills, Projects, etc.)
- **ContentItem**: Individual portfolio items
- **PersonalInfo**: Your personal information and bio
- **ContactMessage**: Contact form submissions

### Admin Features
- **Enhanced Dashboard**: Statistics and quick actions
- **Media Management**: Visual indicators for uploaded files
- **Bulk Operations**: Efficient content management
- **Inline Editing**: Edit content within categories

### Templates
- **Responsive Design**: Mobile-first approach
- **Dynamic Content**: Database-driven content display
- **Interactive Elements**: Modals, video players, galleries
- **SEO Optimized**: Proper meta tags and structure

## 🔧 Configuration

### Environment Variables
```bash
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=postgresql://...
SECURE_SSL_REDIRECT=True
```

### Database
- **Development**: SQLite (default)
- **Production**: PostgreSQL (recommended)
- **Migrations**: Automatic with deployment

### Static Files
- **Development**: Django dev server
- **Production**: WhiteNoise with compression

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **Django**: The web framework for perfectionists with deadlines
- **Bootstrap**: For responsive design components
- **FontAwesome**: For beautiful icons
- **AOS**: For smooth animations
- **Render**: For easy deployment

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/GourabGorai/About-ME_django/issues)
- **Documentation**: See the docs folder
- **Email**: Contact through the portfolio contact form

---

## 🎉 Ready to Showcase Your Work?

This portfolio website provides everything you need to create a professional online presence. With its powerful admin panel, you can easily manage your content and keep your portfolio up-to-date as your career progresses.

**[🚀 Deploy Now](RENDER_DEPLOYMENT_GUIDE.md)** | **[📖 Read the Docs](ADMIN_PANEL_ENHANCED_GUIDE.md)** | **[⭐ Star on GitHub](https://github.com/GourabGorai/About-ME_django)**