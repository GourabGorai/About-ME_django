from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    """Contact form for the website."""
    
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your name...',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email...',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number...'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your message here...',
                'rows': 6,
                'maxlength': 1200,
                'required': True
            })
        }

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if message and len(message.split()) > 200:
            raise forms.ValidationError("Message cannot exceed 200 words.")
        return message