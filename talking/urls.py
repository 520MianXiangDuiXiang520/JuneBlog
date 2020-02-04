from django.urls import path
from .views import TalkingView

urlpatterns = [
    path('', TalkingView.as_view())
]