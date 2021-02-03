from django.urls import path
from .views import MainPageView, add_blog, BlogDetailView, UpdateBlogsView

urlpatterns = [
    path('', MainPageView.as_view(), name='main_page'),
    path('add_blog', add_blog, name='add_blog'),
    path('blog/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('update_blogs/', UpdateBlogsView.as_view(), name='update_blogs'),
]
