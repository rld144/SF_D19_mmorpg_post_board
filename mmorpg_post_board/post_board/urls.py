from django.urls import path
from .views import PostsList, PostDetail, PostCreate, ReplyList, accept_reply, ReplyFilterList, ReplyDelete


urlpatterns = [
   path('', PostsList.as_view(), name='posts_list'),
   path('posts/<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('create/', PostCreate.as_view(), name='post_create'),
   path('replies/', ReplyList.as_view(), name='replies'),
   path('replies/<int:oid>', accept_reply, name='accept_reply'),
   path('replies/filter/', ReplyFilterList.as_view(), name='replies_filter'),
   path('replies/<int:pk>/delete/', ReplyDelete.as_view(), name='reply_delete'),
]