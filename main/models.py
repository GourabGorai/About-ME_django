from django.db import models
from django.urls import reverse


class Category(models.Model):
    """Model for content categories like Projects, Skills, etc."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="FontAwesome icon class (e.g., fas fa-code)")
    order = models.PositiveIntegerField(default=0, help_text="Display order")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class ContentItem(models.Model):
    """Model for individual content items within categories."""
    CONTENT_TYPES = [
        ('project', 'Project'),
        ('skill', 'Skill'),
        ('education', 'Education'),
        ('experience', 'Experience'),
        ('certification', 'Certification'),
        ('internship', 'Internship'),
        ('hackathon', 'Hackathon'),
        ('gallery', 'Gallery Item'),
        ('other', 'Other'),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES, default='other')
    description = models.TextField(help_text="Full description of the content item")
    short_description = models.CharField(max_length=300, blank=True, help_text="Brief description for cards and previews")
    
    # Media fields
    image = models.ImageField(upload_to='content_images/', blank=True, null=True, help_text="Main image for this content")
    video = models.FileField(upload_to='content_videos/', blank=True, null=True, help_text="Demo or presentation video")
    pdf_file = models.FileField(upload_to='content_pdfs/', blank=True, null=True, help_text="Certificate, document, or detailed PDF")
    detail_html_file = models.FileField(upload_to='content_html/', blank=True, null=True, help_text="Custom HTML file for detailed project pages")
    
    # Project/Work specific fields
    technologies = models.CharField(max_length=500, blank=True, help_text="Comma-separated list of technologies used")
    github_url = models.URLField(blank=True, verbose_name="GitHub URL", help_text="Link to GitHub repository")
    demo_url = models.URLField(blank=True, verbose_name="Demo URL", help_text="Link to live demo or project")
    
    # Date fields
    start_date = models.DateField(blank=True, null=True, help_text="When this project/work started")
    end_date = models.DateField(blank=True, null=True, help_text="When this project/work ended (leave blank if ongoing)")
    
    # Display options
    is_featured = models.BooleanField(default=False, help_text="Show this item in the featured section")
    is_active = models.BooleanField(default=True, help_text="Display this item on the website")
    order = models.PositiveIntegerField(default=0, help_text="Display order (lower numbers appear first)")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Content Item"
        verbose_name_plural = "Content Items"

    def __str__(self):
        return f"{self.title} ({self.category.name})"

    def get_absolute_url(self):
        return reverse('content_detail', kwargs={'slug': self.slug})

    def get_technologies_list(self):
        """Return technologies as a list."""
        if self.technologies:
            return [tech.strip() for tech in self.technologies.split(',') if tech.strip()]
        return []

    def get_duration(self):
        """Return a formatted duration string."""
        if self.start_date and self.end_date:
            return f"{self.start_date.strftime('%b %Y')} - {self.end_date.strftime('%b %Y')}"
        elif self.start_date:
            return f"{self.start_date.strftime('%b %Y')} - Present"
        return ""

    def has_media(self):
        """Check if this item has any media files."""
        return bool(self.image or self.video or self.pdf_file or self.detail_html_file)

    def get_media_count(self):
        """Return the number of media files attached."""
        count = 0
        if self.image: count += 1
        if self.video: count += 1
        if self.pdf_file: count += 1
        if self.detail_html_file: count += 1
        return count

    @property
    def is_project(self):
        """Check if this is a project-type content."""
        return self.content_type == 'project'

    @property
    def display_title(self):
        """Return title with category for admin display."""
        return f"{self.title} [{self.category.name}]"


class PersonalInfo(models.Model):
    """Model for personal information displayed on the site."""
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField()
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True)
    resume_pdf = models.FileField(upload_to='resume/', blank=True, null=True)
    
    # Social links
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Personal Information"
        verbose_name_plural = "Personal Information"

    def __str__(self):
        return self.name


class ContactMessage(models.Model):
    """Model for storing contact form submissions."""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name} - {self.created_at.strftime('%Y-%m-%d')}"