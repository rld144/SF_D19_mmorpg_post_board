from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.urls import reverse


tank = 'танк'
heal = 'хил'
dd = 'дд'
merchant = 'торговец'
guild_master = 'гильдмастер'
quest_giver = 'квестгивер'
farrier = 'кузнец'
tanner = 'кожевник'
potion_maker = 'зельевар'
spell_master = 'мастер заклинаний'
CATEGORIES = [
    (tank, 'танк'), (heal, 'хил'), (dd, 'дд'), (merchant, 'торговец'),
    (guild_master, 'гильдмастер'), (quest_giver, 'квестгивер'), (farrier, 'кузнец'),
    (tanner, 'кожевник'), (potion_maker, 'зельевар'), (spell_master, 'мастер заклинаней'),
]


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    header = models.CharField(max_length=255)
    content = RichTextUploadingField()
    category = models.CharField(choices=CATEGORIES, default=merchant, max_length=50)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.header.title()}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class Reply(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Reply')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    accept = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.text[:30]}'


