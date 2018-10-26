from django.urls import path
from . import views

app_name = 'cmdb_info'
urlpatterns = [
    path('', views.index, name='index'),
    # nat页
    path('nat/', views.nat_list, name='nat'),
    path('/admin', views.to_admin, name='to_admin'),
    path('cloud/', views.cloud, name='cloud'),
    # 报废接口
    path('<page_type>/scrap/<int:pk>/', views.scrap, name='scrap'),
    path('<page_type>/callback/<int:pk>/', views.callback, name='callback'),
    # 基础信息页
    path('pc/info/', views.info, name='pc_info'),
    path('server/info/', views.info, name='server_info'),
    path('network/info/', views.info, name='network_info'),
    # 详情页
    path('<page_type>/<int:pk>/detail/', views.detail, name='detail'),
]
