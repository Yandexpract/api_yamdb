from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from users.models import User


def send_confirmation_code(request):
    """Отправляет сгенерированный confirmation_code пользователю."""
    user = get_object_or_404(User, username=request.data.get('username'),)
    confirmation_code = default_token_generator.make_token(user)
    user.save()
    message = f'Ваш код подтверждения - {confirmation_code}'
    from_email = "example@email.com"
    subject = 'Код подтверждения',
    send_mail(subject,
              message=message,
              from_email=from_email,
              recipient_list=[request.data.get('email')])
