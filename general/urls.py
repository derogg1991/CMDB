from django.urls import path
from . import views

app_name = 'general'
urlpatterns = [
    # 空闲ip页
    path('ipinfree/', views.ip_in_free, name='ipinfree'),
    ]