from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from uploads.core.forms import DocumentForm
from uploads.core.models import Document


def home(request):
    documents = Document.objects.all()
    return render(request, 'core/home.html', {'documents': documents})

@csrf_exempt
def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'core/simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'core/simple_upload.html')

@csrf_exempt
def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'core/model_form_upload.html', {
        'form': form
    })

@csrf_exempt
def json_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url =  fs.url(filename)
        protocol = getattr(settings, "PROTOCOL", "http")
        domain = request.META['HTTP_HOST']
        return JsonResponse({'status':'success',
                             'image_url':"%s://%s%s" % (protocol, domain, uploaded_file_url)})
    return JsonResponse({'status':'error'})

@csrf_exempt
def json_upload_model(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            model = form.save()
            protocol = getattr(settings, "PROTOCOL", "http")
            domain = request.META['HTTP_HOST']
            return JsonResponse({'status': 'success',
                                 'image_url': "%s://%s%s" % (protocol, domain, model.document.url)})

    return JsonResponse({'status': 'error'})
