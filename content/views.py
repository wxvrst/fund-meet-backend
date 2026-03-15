from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework import generics, filters, viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from content.models import PublicationModel, PublicationTagModel, PublicationContentModel, PublicationCommentModel
from content.serializers import PublicationSerializer, PublicationTagSerializer, PublicationContentSerializer, \
    PublicationCommentSerializer


class PublicationViewSet(viewsets.ModelViewSet):
    queryset = PublicationModel.objects.all()
    serializer_class = PublicationSerializer
    filter = [DjangoFilterBackend]

    filterset_fields = {
        'author__username': ['icontains'],
        'tags': ['exact'],
    }


class TagViewSet(viewsets.ModelViewSet):
    queryset = PublicationTagModel.objects.all()
    serializer_class = PublicationTagSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = PublicationCommentModel.objects.all()
    serializer_class = PublicationCommentSerializer


    def perform_create(self, serializer):
        serializer.save(autor=self.request.user)

    @action(detail=False, methods=['get'], url_path='by_publication/(?P<publication_id>\d+)')
    def list_by_publication(self, request, publication_id=None):
        publication = get_object_or_404(PublicationModel, id=publication_id)

        comments = self.get_queryset().filter(publication_id=publication_id)


        serializer = self.get_serializer(comments, many=True)
        return Response({
            'publication': {
                'id': publication.id,
                'header': publication.header,
            },
            'comments': serializer.data,
            'count': comments.count()
        })

    @action(detail=False, methods=['post'], url_path='by-publication/(?P<publication_id>\d+)')
    def create_by_publication(self, request, publication_id=None):
        publication = get_object_or_404(PublicationModel, id=publication_id)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(autor=request.user, publication=publication)

        return Response({
            'message': f'Комментарий создан для публикации "{publication.header}"',
            'publication_id': publication.id,
            'comment': serializer.data
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['put', 'patch'],
            url_path='by-publication/(?P<publication_id>\d+)/(?P<comment_id>\d+)')
    def update_by_publication(self, request, publication_id=None, comment_id=None):
        publication = get_object_or_404(PublicationModel, id=publication_id)
        comment = get_object_or_404(PublicationCommentModel, id=comment_id)

        if comment.publication.id != publication_id:
            return Response(
                {'error': 'Комментарий не принадлежит указанной публикации'},
                status=status.HTTP_400_BAD_REQUEST
            )

        partial = request.method == 'PATCH'
        serializer = self.get_serializer(comment, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'message': f'Комментарий обновлен в публикации "{publication.header}"',
            'publication_id': publication.id,
            'comment': serializer.data
        })

    @action(detail=True, methods=['post'])
    def reply(self, request, pk=None):
        parent_comment = self.get_object()

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(
                autor=request.user,
                parent_comment=parent_comment,
                publications=parent_comment.publications.first()
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'],
            url_path='delete-by-publication/(?P<publication_id>\d+)/(?P<comment_id>\d+)')
    def delete_by_publication(self, request, publication_id=None, comment_id=None):
        """
        Удаляет комментарий, проверяя принадлежность указанной публикации.
        Права: автор комментария, автор публикации или администратор.
        """
        publication = get_object_or_404(PublicationModel, id=publication_id)
        comment = get_object_or_404(PublicationCommentModel, id=comment_id)

        # Проверяем, что комментарий действительно относится к данной публикации
        if comment.publication.id != publication.id:
            return Response(
                {'error': 'Комментарий не принадлежит указанной публикации'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Проверка прав на удаление
        user = request.user
        if user != comment.autor and user != publication.author and not user.is_staff:
            return Response(
                {'error': 'У вас нет прав на удаление этого комментария'},
                status=status.HTTP_403_FORBIDDEN
            )

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PublicationContentCreateView(generics.CreateAPIView):
    serializer_class = PublicationContentSerializer

class PublicationContentUpdateView(generics.UpdateAPIView):
    serializer_class = PublicationContentSerializer

    def get_object(self):
        publication_id = self.kwargs.get('publication_id')
        publication = get_object_or_404(PublicationModel, id=publication_id)

        return publication.content


    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            'message': 'Контент обновлен',
            'publication_id': instance.publication.id,
            'content': serializer.data
        })


class PublicationContentList(generics.ListAPIView):
    """
    Возвращает список всех объектов контента.
    Поддерживает фильтрацию по полю publication (если нужно).
    """
    queryset = PublicationContentModel.objects.all()
    serializer_class = PublicationContentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['publication']


class PublicationContentGetById(generics.RetrieveAPIView):
    """
    Возвращает один объект контента по его первичному ключу (id).
    """
    queryset = PublicationContentModel.objects.all()
    serializer_class = PublicationContentSerializer


class PublicationContentDeleteByPublicationId(APIView):
    """
    Удаляет контент, связанный с публикацией, по идентификатору публикации.
    Предполагается, что связь OneToOne (publication.content).
    """
    def delete(self, request, publication_id):
        publication = get_object_or_404(PublicationModel, id=publication_id)
        content = getattr(publication, 'content', None)
        if content is None:
            return Response(
                {'error': 'У данной публикации нет контента'},
                status=status.HTTP_404_NOT_FOUND
            )
        content.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


