from rest_framework import serializers

from account.models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации новых пользователей.

    Параметры:
        email (str): Электронный адрес пользователя.
        password (str): Пароль пользователя.

    Методы:
        create(self, validated_data): Создает нового пользователя с указанными данными.

    """

    class Meta:
        model = CustomUser
        fields = ('email', 'password')

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')

        user = CustomUser.objects.create_user(email=email, password=password, is_active=True)
        return user


class LoginSerializer(serializers.Serializer):
    """
    Сериализатор для аутентификации пользователей.

    Параметры:
        email (str): Электронный адрес пользователя.
        password (str): Пароль пользователя.
    """
    email = serializers.EmailField()
    password = serializers.CharField()


class RegisterConfirmSerializer(serializers.ModelSerializer):
    """
    Сериализатор для подтверждения регистрации пользователей.

    Параметры:
        email (str): Электронный адрес пользователя.
        password (str): Пароль пользователя (минимальная длина - 6 символов).

    Методы:
        create(self, validated_data):
        Создает нового пользователя с заданными данными и отправляет письмо с кодом активации на указанный email.

    """
    password = serializers.CharField(min_length=6, write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password')

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        send_activation_code = self.context.get('send_activation_code')
        user = CustomUser.objects.create_user(email=email, password=password)

        activation_url = f'http://localhost:2222/api/accounts/register/activate/{user.activation_code}'
        send_activation_code.delay(email=user.email, activation_url=activation_url)
        return user
