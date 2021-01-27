from django.shortcuts import render

def home_view(request, *args, **kwargs):
    return render(request, 'home.html')

def about_view(request, *args, **kwargs):
    my_context = {
        'my_text': 'This is about us',
        'my_number': 123,
        'my_list': [456,789,102]
    }
    return render(request, 'about.html', my_context)

def contact_view(request, *args, **kwargs):
    return render(request, 'contact.html')

def social_view(request, *args, **kwargs):
    return render(request, 'social.html')
