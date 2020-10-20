from .views import BlogViewSet, BlogCategoryView
from django.urls import path, include

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'posts', BlogViewSet)


urlpatterns = [

    path('', include(router.urls), name='blog-viewset'),
    path('categories/',
         BlogCategoryView.as_view(), name='blog-categories'),
]
