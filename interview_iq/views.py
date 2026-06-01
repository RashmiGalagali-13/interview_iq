from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from accounts.models import ContactMessage

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()
        
        # Simple server-side validation (complements JS)
        if name and email and message:
            # Save contact message to database
            ContactMessage.objects.create(
                name=name,
                email=email,
                message=message
            )
            messages.success(request, "Thank you for your message! We'll get back to you within 24 hours.")
        else:
            messages.error(request, 'Please fill in all fields correctly.')
        
        return HttpResponseRedirect(reverse('contact'))
    
    return render(request, 'contact.html')
