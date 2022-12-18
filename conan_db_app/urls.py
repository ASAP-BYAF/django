from django.urls import path

from . import views

app_name = 'conan_db_app'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('chara_list/', views.CharaListView.as_view(), name='list'),
    path('chara_detail/<int:pk>/<int:page>', views.chara_detail_func, name='detail'),
    path('case_list/', views.IndexView.as_view(), name='case'),
    path('wiseword_list/', views.IndexView.as_view(), name='wiseword'),
    path('question_create/', views.QuestionCreateView.as_view(), name='question_create'),
    # path('question_list/<int:page>/', views.QuestionListView.as_view(), name='question_list'),
    path('question_list/', views.QuestionListView.as_view(), name='question_list'),
]