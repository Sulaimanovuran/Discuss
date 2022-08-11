from django.urls import include, path
from rest_framework.routers import DefaultRouter

from thread.views import CategoryView, ThreadView, AnswerView, CommentView

router = DefaultRouter()
router.register('category', CategoryView)
router.register('thread', ThreadView)
router.register('answer', AnswerView)
router.register('comment', CommentView)

urlpatterns = [
    path('', include(router.urls)),
]
