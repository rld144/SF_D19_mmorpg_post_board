from django_filters import *
from .models import Reply, Post


class ReplyFilter(FilterSet):
    post = ModelMultipleChoiceFilter(
        queryset=Post.objects.all()
    )

    class Meta:
        model = Reply
        fields = {
            'user__username': ['icontains'],
            'text': ['icontains'],
            'date': ['date__gt'],
            'post__category': ['exact'],
            'post': ['exact']
        }

