from django.urls import path

from account.views import RegisterView, LoginView, ActivateView, RegisterConfirmView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view(), name='login'),
    path('register-confirm/', RegisterConfirmView.as_view()),
    path('register/activate/<str:activation_code>/', ActivateView.as_view()),
]