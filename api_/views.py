from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, template_name='api/index.html', context={})

def musics(request, music: str=''):
    context = {
        'musics': (music, 'Lamia', 'Time Table', 'Space Dye-Vest', 'Kaleidoscope')
    }
    return render(request=request, template_name='api/musics_like.html', context=context)