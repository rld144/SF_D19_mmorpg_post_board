from .models import Post, Reply
from .forms import PostForm, ReplyForm
from django.views.generic import ListView, DetailView, CreateView, View, DeleteView
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.dispatch import receiver
from django.core.mail import send_mail
from django.db.models.signals import post_save
from mmorpg_post_board.settings import DEFAULT_FROM_EMAIL
from django.shortcuts import redirect
from .filters import ReplyFilter


@receiver(post_save, sender=Reply)
def notify_reply_on_post(sender, instance, created, **kwargs):
    if created:
        print('Сообщение о том что написан ОТКЛИК под постом отправляется')
        send_mail(
            subject=f"Оставлен отклик под постом '{instance.post.header}'",
            message=f"Отклик: {instance.text}; user:{instance.user.username}; http://127.0.0.1:8000/posts/{instance.post.pk}",
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[instance.post.author.email, ]
        )
        print('ОТКЛИК передан на почту автора поста')

@receiver(post_save, sender=Reply)
def notify_reply_on_post(sender, instance, created, **kwargs):
    if instance.accept:
        print('Сообщение об ПРИНЯТИИ ОТКЛИКА отправляется')
        send_mail(
            subject=f"Отклик под постом '{instance.post.header}' принят",
            message=f"Отклик: {instance.text}; был принят автором поста '{instance.post.author.username}'; http://127.0.0.1:8000/posts/{instance.post.pk}",
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[instance.user.email, ]
        )
        print('ПРИНЯТ ОТКЛИК отправлен')


class PostsList(ListView):
    model = Post
    ordering = '-date'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 30


class PostDetail(LoginRequiredMixin, DetailView, FormMixin):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    form_class = ReplyForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['replies'] = Reply.objects.filter(post=self.object)
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        reply = form.save(commit=False)
        reply.user = self.request.user
        reply.post = self.get_object()
        reply.save()
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy('post_detail', kwargs={'pk':self.get_object().id})


class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        return super().form_valid(form)


class ReplyList(LoginRequiredMixin, ListView):
    template_name = 'replies.html'
    ordering = '-date'

    def get_queryset(self):
        self.queryset = Reply.objects.filter(post__author=self.request.user)
        return self.queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['replies'] = self.queryset
        return context


def accept_reply(request, oid):
    reply = Reply.objects.get(pk=oid)
    reply.accept = 1
    reply.save()
    return redirect('/replies/')


class ReplyFilterList(LoginRequiredMixin, ListView):
    template_name = 'replies_filter.html'
    ordering = '-date'

    def get_queryset(self):
        self.queryset = Reply.objects.filter(post__author=self.request.user)
        self.filterset = ReplyFilter(self.request.GET, self.queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['replies'] = self.filterset
        return context


class ReplyDelete(DeleteView):
    model = Reply
    template_name = 'reply_delete.html'
    success_url = reverse_lazy('replies')
    # permission_required = ('newsportal.delete_post',)






