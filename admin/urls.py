from django.urls import path
from .views import ArticleManage, TagManageView, LoginView


urlpatterns = [
    path('articleManager/'.lower(), ArticleManage.as_view()),
    path('TagManage/'.lower(), TagManageView.as_view()),
    path('adminLogin/'.lower(), LoginView.as_view())
]