from django.urls import path
from posts.views import (
    PostDetailView, 
    PostManageView,
    PostListView,
    PostView,
    SearchView,
    CommentView
)


urlpatterns = [
    path('/post/<int:post_id>', PostDetailView.as_view()),
    path('/main', PostListView.as_view()),
    path('/newpost', PostView.as_view()),
    path('/post/manage/<int:post_id>', PostManageView.as_view()),
    path('/post/search', SearchView.as_view()),
    path('/<int:post_id>/comment',CommentView.as_view()),
    path('/comment/<comment_id>',CommentView.as_view()),

]