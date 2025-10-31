from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Category, ContentItem, PersonalInfo, ContactMessage


class ContentItemInline(admin.TabularInline):
    """Inline admin for ContentItem within Category admin."""
    model = ContentItem
    extra = 0
    fields = ['title', 'content_type', 'is_featured', 'is_active', 'order']
    readonly_fields = ['title']
    show_change_link = True


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon_display', 'order', 'is_active', 'items_count', 'view_on_site']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['order', 'is_active']
    ordering = ['order', 'name']
    inlines = [ContentItemInline]
    actions = ['make_active', 'make_inactive', 'duplicate_category']

    def icon_display(self, obj):
        if obj.icon:
            return format_html('<i class="{}"></i> {}', obj.icon, obj.icon)
        return '-'
    icon_display.short_description = 'Icon'

    def items_count(self, obj):
        count = obj.items.count()
        active_count = obj.items.filter(is_active=True).count()
        return format_html('{} total ({} active)', count, active_count)
    items_count.short_description = 'Items Count'

    def view_on_site(self, obj):
        if obj.slug:
            url = reverse('category_detail', kwargs={'slug': obj.slug})
            return format_html('<a href="{}" target="_blank">View</a>', url)
        return '-'
    view_on_site.short_description = 'View on Site'

    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} categories were successfully activated.')
    make_active.short_description = "Mark selected categories as active"

    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} categories were successfully deactivated.')
    make_inactive.short_description = "Mark selected categories as inactive"

    def duplicate_category(self, request, queryset):
        for category in queryset:
            category.pk = None
            category.name = f"{category.name} (Copy)"
            category.slug = f"{category.slug}-copy"
            category.save()
        self.message_user(request, f'{queryset.count()} categories were successfully duplicated.')
    duplicate_category.short_description = "Duplicate selected categories"


@admin.register(ContentItem)
class ContentItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'content_type', 'is_featured', 'is_active', 'order', 'created_at', 'view_on_site']
    list_filter = ['category', 'content_type', 'is_featured', 'is_active', 'created_at', 'start_date']
    search_fields = ['title', 'description', 'technologies', 'short_description']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['order', 'is_featured', 'is_active']
    ordering = ['category', 'order', '-created_at']
    date_hierarchy = 'created_at'
    actions = ['make_featured', 'remove_featured', 'make_active', 'make_inactive', 'duplicate_items']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('category', 'title', 'slug', 'content_type', 'description', 'short_description')
        }),
        ('Media Files', {
            'fields': ('image', 'video', 'pdf_file', 'detail_html_file'),
            'classes': ('collapse',),
            'description': 'Upload media files for this content item'
        }),
        ('Project/Work Details', {
            'fields': ('technologies', 'github_url', 'demo_url', 'start_date', 'end_date'),
            'classes': ('collapse',),
            'description': 'Additional details for projects, work experience, etc.'
        }),
        ('Display & SEO Options', {
            'fields': ('is_featured', 'is_active', 'order'),
            'description': 'Control how and where this item appears on the site'
        })
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category')

    def view_on_site(self, obj):
        if obj.slug:
            url = reverse('content_detail', kwargs={'slug': obj.slug})
            return format_html('<a href="{}" target="_blank">View</a>', url)
        return '-'
    view_on_site.short_description = 'View on Site'

    def make_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} items were marked as featured.')
    make_featured.short_description = "Mark selected items as featured"

    def remove_featured(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} items were removed from featured.')
    remove_featured.short_description = "Remove featured status from selected items"

    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} items were successfully activated.')
    make_active.short_description = "Mark selected items as active"

    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} items were successfully deactivated.')
    make_inactive.short_description = "Mark selected items as inactive"

    def duplicate_items(self, request, queryset):
        for item in queryset:
            item.pk = None
            item.title = f"{item.title} (Copy)"
            item.slug = f"{item.slug}-copy"
            item.save()
        self.message_user(request, f'{queryset.count()} items were successfully duplicated.')
    duplicate_items.short_description = "Duplicate selected items"


@admin.register(PersonalInfo)
class PersonalInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'email', 'location', 'updated_at']
    search_fields = ['name', 'title', 'email']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'title', 'location', 'email', 'phone', 'bio'),
            'description': 'Your basic personal and professional information'
        }),
        ('Media Files', {
            'fields': ('profile_image', 'resume_pdf'),
            'description': 'Upload your profile photo and resume'
        }),
        ('Social Media Links', {
            'fields': ('linkedin_url', 'github_url', 'facebook_url', 'twitter_url'),
            'classes': ('collapse',),
            'description': 'Your social media and professional profiles'
        })
    )

    def has_add_permission(self, request):
        # Only allow one PersonalInfo instance
        return not PersonalInfo.objects.exists()

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save_and_add_another'] = False
        return super().changeform_view(request, object_id, form_url, extra_context)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'message_preview', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['name', 'email', 'phone', 'message', 'created_at']
    list_editable = ['is_read']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    actions = ['mark_as_read', 'mark_as_unread']

    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Message Preview'

    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} messages were marked as read.')
    mark_as_read.short_description = "Mark selected messages as read"

    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} messages were marked as unread.')
    mark_as_unread.short_description = "Mark selected messages as unread"

    def has_add_permission(self, request):
        return False  # Don't allow adding messages through admin

    def has_delete_permission(self, request, obj=None):
        return True  # Allow deleting messages

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        # Mark message as read when viewed
        if object_id:
            try:
                message = ContactMessage.objects.get(pk=object_id)
                if not message.is_read:
                    message.is_read = True
                    message.save()
            except ContactMessage.DoesNotExist:
                pass
        return super().changeform_view(request, object_id, form_url, extra_context)


# Customize admin site
admin.site.site_header = "Portfolio Admin Panel"
admin.site.site_title = "Portfolio Admin"
admin.site.index_title = "Welcome to Your Portfolio Administration"

# Add some custom CSS for better admin experience
admin.site.enable_nav_sidebar = True