from django.urls import path
from blog import views

POST_PATH = '<int:year>/<int:month>/<int:day>/<slug:slug>/'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path(POST_PATH,
         views.post_detail, name='post_detail'),
    path('<int:id>/share/', views.post_share, name='post_share'),
]
