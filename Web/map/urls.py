#COMP90024_Team_20

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('wrath', views.wrath, name='wrath'),
    path('hashtags', views.hashtags, name='hashtags'),
    path('api/v1/sentiment_by_suburbs', views.sentiment_by_suburbs, name='sentiment_by_suburbs'),
    path('api/v1/sentiment_by_weekdays', views.sentiment_by_weekdays, name='sentiment_by_weekdays'),
    path('api/v1/sentiment_by_hours', views.sentiment_by_hours, name='sentiment_by_hours'),
    path('api/v1/word_cloud', views.word_cloud, name='word_cloud'),
    path('pride', views.pride, name='pride'),
    path('aurin', views.aurin, name='aurin'),
    path('aboutUs', views.aboutUs, name='aboutUs'),
    path('report', views.report, name='report'),
]
