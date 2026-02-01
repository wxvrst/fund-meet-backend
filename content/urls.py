from rest_framework.routers import DefaultRouter
from django.urls import path, include

from content import views
from content.views import PublicationViewSet, TagViewSet, CommentViewSet

app_name = 'content'

router = DefaultRouter()
router.register(r'publications', PublicationViewSet, basename='publication')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'comments', CommentViewSet, basename='comments')


urlpatterns = [
    path('', include(router.urls)),
    path('content/create/', views.PublicationContentCreateView.as_view(), name='publication_create'),
    path('content/update/<int:publication_id>/<int:id>/', views.PublicationContentUpdateView.as_view(), name='publication_detail'),
]
