from django.core import exceptions

from django.contrib.auth import authenticate
from django.shortcuts import redirect

from rest_framework import exceptions, status
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from account.models import CustomUser
from account.serializers import RegisterSerializer, LoginSerializer, RegisterConfirmSerializer
from account.tasks import send_activation_code


class RegisterView(GenericAPIView):
    """
    Представление для регистрации новых пользователей.

    Методы:
        post
    """

    serializer_class = RegisterSerializer

    def post(self, request):
        """
        Регистрирует нового пользователя с указанными данными.

        Параметры:
            request (Request): Запрос, содержащий данные о новом пользователе.

        Возвращаемое значение:
            Response: Ответ с сообщением о успешной регистрации или сообщением об ошибке.
        """

        data = request.data
        serializer = RegisterSerializer(data=data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Вы успешно зарегистрировались!', status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """
    Представление для аутентификации пользователей.

    Методы:
        post
    """

    def post(self, request, *args, **kwargs):
        """
        Проверяет данные пользователя и создает токен для аутентифицированного пользователя.

        Параметры:
            request (Request): Запрос, содержащий данные пользователя для аутентификации.

        Возвращаемое значение:
            Response: Ответ с токеном и данными пользователя или сообщением об ошибке аутентификации.
        """

        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(email=serializer.validated_data['email'], password=serializer.validated_data['password'])
        if not user:
            raise exceptions.AuthenticationFailed('Логин или пароль введен неверно. Попробуйте снова')

        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'is_active': user.is_active,
        })


class RegisterConfirmView(GenericAPIView):
    """
    Представление для подтверждения регистрации пользователей.

    Методы:
        post
    """

    serializer_class = RegisterConfirmSerializer

    def post(self, request):
        """
        Проверяет данные о пользователе и отправляет письмо для активации аккаунта.

        Параметры:
            request (Request): Запрос, содержащий данные о пользователе для регистрации.

        Возвращаемое значение:
            Response: Ответ с сообщением о успешной регистрации или сообщением об ошибке.
        """

        data = request.data
        serializer = RegisterConfirmSerializer(data=data, context={'request': request,
                                                                   'send_activation_code': send_activation_code})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response_data = {
                "message": "Регистрация прошла успешно. На вашу почту отправлена ссылка для активации аккаунта."
            }
            return Response(response_data, status=status.HTTP_201_CREATED)


class ActivateView(APIView):
    """
    Представление для активации учетной записи пользователя.

    Методы:
        get(self, request, activation_code): Активирует учетную запись пользователя по коду активации.
    """

    def get(self, request, activation_code):
        """
        Активирует учетную запись пользователя по коду активации.

        Параметры:
            request (Request): Запрос.
            activation_code (str): Код активации учетной записи пользователя.

        Возвращаемое значение:
            HttpResponseRedirect: Перенаправляет пользователя на страницу входа после успешной активации.
        """

        user = get_object_or_404(CustomUser, activation_code=activation_code)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return redirect(request.build_absolute_uri('/api/accounts/login'))
