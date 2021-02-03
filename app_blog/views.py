from _csv import reader
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import Blog, Files
from .forms import MultiFileForm, FileUpdateBlogsForm


class MainPageView(View):
    def get(self, request):
        blogs = Blog.objects.order_by('-created_at')
        return render(request, 'blog/main_page.html', {'blogs': blogs})


def add_blog(request):
    if request.method == 'POST':
        form = MultiFileForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            blog = Blog.objects.create(
                topic=data.get('topic'),
                description=data.get('description'),
                author=request.user,
            )
            files = request.FILES.getlist('file_field')
            for f in files:
                instance = Files(file=f, blog=blog)
                instance.save()
            return redirect('/')
    else:
        form = MultiFileForm()

    context = {
        'form': form
    }
    return render(request, 'blog/add_blog.html', context)


class BlogDetailView(View):
    def get(self, request, pk):
        blog = Blog.objects.get(id=pk)
        files = Files.objects.filter(blog=blog)
        return render(request, 'blog/blog_detail.html', {'blog': blog, 'files': files})


class UpdateBlogsView(View):
    def post(self, request):
        upload_file_form = FileUpdateBlogsForm(request.POST, request.FILES)
        if upload_file_form.is_valid():
            price_file = upload_file_form.cleaned_data['file_field'].read()
            price_str = price_file.decode('utf-8').split('\n')
            csv_reader = reader(price_str, delimiter=',', quotechar='"')
            for row in csv_reader:  # формат csv файла: | id | description | dd-mm-YY HH:MM:SS |
                if row:
                    try:
                        date_time = datetime.strptime(row[2], '%d-%m-%Y %H:%M:%S')
                    except ValueError:
                        return HttpResponse(
                            content=f'Неверный формат даты!\nСМ: | id | description | dd-mm-YY HH:MM:SS |', status=200)
                    Blog.objects.filter(id=row[0]).update(description=row[1], created_at=date_time)
            return HttpResponse(content=f'Блоги были успешно обновлены', status=200)
        context = {
            'form': upload_file_form
        }
        return render(request, 'blog/file_form_upload.html', context)

    def get(self, request):
        upload_file_form = FileUpdateBlogsForm()
        context = {
            'form': upload_file_form
        }
        return render(request, 'blog/file_form_upload.html', context)
