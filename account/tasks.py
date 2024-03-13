from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_activation_code(email, activation_url):
    """
    Отправляет электронное письмо с кодом активации для подтверждения регистрации.

    Параметры:
        email (str): Электронный адрес получателя письма.
        activation_url (str): URL-адрес для активации учетной записи.
    """
    message = f"""
        Спасибо за регистрацию.
        Активируйте вашу учетную запись.
        Ссылка для активации: {activation_url}
        """
    send_mail(
        'Активируйте вашу учетную запись',
        message,
        'press.kenesh@gmail.com',
        [email, ],
        fail_silently=False
    )
