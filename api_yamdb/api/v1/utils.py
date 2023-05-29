from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from users.models import User


def send_confirmation_code(request):
    """Отправляет сгенерированный confirmation_code пользователю."""
    user = User.objects.get(username=request.data.get('username'),
                            email=request.data.get('email'))
    confirmation_code = default_token_generator.make_token(user)
    user.save()
    send_mail(f'Ваш код подтверждения - {confirmation_code}',
              settings.SEND_EMAIL,
              [request.data.get('email')])
