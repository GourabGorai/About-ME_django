from .models import Category, ContentItem, ContactMessage


def admin_stats(request):
    """Context processor to provide admin dashboard statistics."""
    if request.path.startswith('/admin/'):
        return {
            'total_categories': Category.objects.filter(is_active=True).count(),
            'total_content_items': ContentItem.objects.filter(is_active=True).count(),
            'featured_items': ContentItem.objects.filter(is_featured=True, is_active=True).count(),
            'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
        }
    return {}