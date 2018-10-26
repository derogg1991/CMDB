from django.urls import path
from . import views

app_name = 'file'
urlpatterns = [
    path('<page_type>/upload/', views.upload_file, name='file'),
    path('<page_type>/download_templates/', views.down_template, name='down_template'),
    path('<page_type>/export/', views.export, name='export'),
]
