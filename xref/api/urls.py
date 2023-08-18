"""
URL configuration for music_controller project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from . import views
from api.views import post_view


router = routers.DefaultRouter()
router.register(r'person', views.PersonViewSet)
router.register(r'grade', views.CsvRowViewSet)
router.register(r'course', views.CsvFileViewSet)

router.register(r'search', views.KeywordSearchViewSet, basename='search')
router.register(r'list_csv', views.CsvFileViewSet, basename='list_csv')
router.register(r'user', views.UserViewSet, basename='user')

router.register(r'detail', views.JoinViewSet, basename='person_detail')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('upload_csv/', views.CSVUploadView.as_view(), name='upload_csv'),
    path('api-person/', post_view, name='post'),
    # path('course_grade', GradeView.as_view(), name='course-grade'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('user', views.UserView.as_view(), name='user'),
    path('person/<int:people_id>/detail/', views.JoinViewSet.as_view({'get': 'list_by_person'}), name='person-grade'),
]