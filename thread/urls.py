from django.urls import include, path
from rest_framework.routers import DefaultRouter

from thread.views import CategoryView, ThreadView, AnswerView, CommentView, AwarenessView

router = DefaultRouter()
router.register('category', CategoryView)
router.register('answer', AnswerView)
router.register('comment', CommentView)
router.register('awareness', AwarenessView)
router.register('thread', ThreadView)

urlpatterns = [
    path('', include(router.urls)),
]
