from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from thread.models import *
from thread.serializers import *


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 10000


class CategoryView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ThreadView(ModelViewSet):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['category', 'author']
    ordering_fields = ['name', 'id']
    search_fields = ['name', 'id']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AnswerView(ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['text']

    def get_queryset(self):
        sorted_queryset = sorted(self.queryset, key=sort_func, reverse=True)
        return sorted_queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(methods=['POST'], detail=True)
    def like(self, request, pk, *args, **kwargs):
        try:
            like_object, _ = Like.objects.get_or_create(owner=request.user, answer_id=pk)
            like_object.like = not like_object.like
            like_object.save()
            status = 'Лайк поставлен'
            if like_object.like:
                return Response({'status': status})
            status = 'Лайк убран'
            return Response({'status': status})
        except:
            return Response('Нет такого продукта')

    @action(methods=['POST'], detail=True)
    def rating(self, request, pk, *args, **kwargs):
        serializers = RatingSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        obj, _ = Rating.objects.get_or_create(answer_id=pk, owner=request.user)
        obj.rating = request.data['rating']
        obj.save()
        return Response(request.data, status=201)

    @action(methods=['POST'], detail=True)
    def favorite(self, request, pk, *args, **kwargs):
        try:
            favorite, availability = Favourite.objects.get_or_create(owner=request.user, answer_id=pk)

            if not availability:
                favorite.delete()
                return Response('Удалено из избранного')
            else:
                favorite.save()
                return Response('Добавлено в избранное')
        except:
            return Response('Нет такого "ответа"!')


class CommentView(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class AwarenessView(mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = Awareness.objects.all()
    serializer_class = AwarenessSerializer
