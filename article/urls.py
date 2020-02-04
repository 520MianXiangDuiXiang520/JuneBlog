from django.conf.urls import url
from django.urls import path
from .views import ArticlesListView, DetailView, TagsView

urlpatterns = [
    path('', ArticlesListView.as_view()),
    url(r'detail/(?P<detail>\d+)$', DetailView.as_view(), name='detail'),
    path('tags/', TagsView.as_view())
]
