from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, View, FormView
from .models import SignupOtc
from django.core.mail import send_mail
from .forms import SignupOtcForm, OtcForm
from random import randint
from mmorpg_post_board.settings import DEFAULT_FROM_EMAIL
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError


@receiver(post_save, sender=SignupOtc)
def notify_one_time_code(sender, instance, created, **kwargs):
    if created:
        print('сообщение про КОД ПОДТВЕРЖДЕНИЯ отправляется')
        send_mail(
            subject="Код подтверждения для регистрации на сайт по мморпг MMORPG-Post-Board",
            message=f"Код подтверждения - {instance.otc}, http://127.0.0.1:8000/sign/signup/?pk_otc={instance.pk}",
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email, ]
        )
        print('КОД ПОДТВЕРЖДЕНИЯ отправлен на почту')


@receiver(post_save, sender=SignupOtc)
def delete_user_otc(sender, instance, created, **kwargs):
    if instance.its_confirmed == 1:
        instance.delete()


class SignupOtcView(CreateView):
    model = SignupOtc
    form_class = SignupOtcForm
    template_name = 'sign/signupotc.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.otc = randint(1000, 9999)
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.object.id
        self.success_url = f'/sign/signup?pk_otc={pk}'
        return self.success_url


class BaseRegisterView(FormView):
    template_name = 'sign/signup.html'
    form_class = OtcForm
    success_url = '/'

    def form_valid(self, form):
        ot_code = form.cleaned_data['ot_code']
        path = self.request.get_full_path()
        pk = path.split('=')[-1]
        if '?pk_otc' in path and pk.isdigit():
            pk = int(pk)
            user_otc = SignupOtc.objects.get(pk=pk)
            if user_otc.otc != ot_code:
                raise ValidationError({
                    "One-time code": "код подтверждения неверен"
                })
            else:
                user = User.objects.create_user(user_otc.username, user_otc.email, user_otc.password1)
                user.save()
                user_otc.its_confirmed = 1
                user_otc.save()

        return super().form_valid(form)

