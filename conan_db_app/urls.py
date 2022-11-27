from django.urls import path

from . import views

app_name = 'conan_db_app'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('chara_list/', views.CharaListView.as_view(), name='list'),
    path('chara_detail/<int:pk>', views.chara_detail_func, name='detail'),
]