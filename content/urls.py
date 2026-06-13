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
    path('content/content_list/', views.PublicationContentList.as_view(), name='content_list'),
    path('content/content/<int:pk>/', views.PublicationContentGetById.as_view(), name='content_detail'),
    path('content/delete_by_publication/<int:publication_id>', views.PublicationContentDeleteByPublicationId.as_view(), name='content_delete_by_publication'),
]
