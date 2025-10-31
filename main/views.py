from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse, HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.decorators.clickjacking import xframe_options_exempt
from .models import Category, ContentItem, PersonalInfo, ContactMessage
from .forms import ContactForm
import os


def home(request):
    """Home page view with all portfolio content."""
    try:
        personal_info = PersonalInfo.objects.first()
    except PersonalInfo.DoesNotExist:
        personal_info = None
    
    # Get all active categories with their items
    categories = Category.objects.filter(is_active=True).prefetch_related(
        'items__category'
    )
    
    # Get featured items
    featured_items = ContentItem.objects.filter(
        is_featured=True, 
        is_active=True,
        category__is_active=True
    ).select_related('category')[:6]
    
    # Handle contact form
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Thank you! Your message has been sent.'})
            else:
                messages.success(request, 'Thank you! Your message has been sent.')
                return redirect('home')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ContactForm()
    
    context = {
        'personal_info': personal_info,
        'categories': categories,
        'featured_items': featured_items,
        'form': form,
    }
    
    return render(request, 'main/home.html', context)


def category_detail(request, slug):
    """Category detail view."""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    items = ContentItem.objects.filter(
        category=category,
        is_active=True
    ).order_by('order', '-created_at')
    
    context = {
        'category': category,
        'items': items,
    }
    
    return render(request, 'main/category_detail.html', context)


def content_detail(request, slug):
    """Content item detail view."""
    item = get_object_or_404(
        ContentItem, 
        slug=slug, 
        is_active=True,
        category__is_active=True
    )
    
    # Get related items from the same category
    related_items = ContentItem.objects.filter(
        category=item.category,
        is_active=True
    ).exclude(id=item.id)[:3]
    
    context = {
        'item': item,
        'related_items': related_items,
    }
    
    return render(request, 'main/content_detail.html', context)


@require_http_methods(["GET", "POST"])
def contact(request):
    """Contact form view."""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save the contact message
            ContactMessage.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data.get('phone', ''),
                message=form.cleaned_data['message']
            )
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Thank you! Your message has been sent.'})
            else:
                messages.success(request, 'Thank you! Your message has been sent.')
                return redirect('home')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors})
            else:
                messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()
    
    context = {'form': form}
    return render(request, 'main/contact.html', context)


@xframe_options_exempt
def project_detail_html(request, slug):
    """Serve HTML file for project details in iframe."""
    item = get_object_or_404(
        ContentItem, 
        slug=slug, 
        is_active=True,
        category__is_active=True
    )
    
    # If HTML file is uploaded, serve it
    if item.detail_html_file:
        try:
            with open(item.detail_html_file.path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            return HttpResponse(html_content, content_type='text/html')
        except FileNotFoundError:
            pass
    
    # Fallback to Django template
    context = {
        'item': item,
    }
    return render(request, 'main/project_detail_iframe.html', context)