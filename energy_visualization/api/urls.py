from django.urls import path
from .views import RegisterView, LoginView, UserEnergyDataView, FilterEnergyDataView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),  # Ensure trailing slash
    path('login', LoginView.as_view(), name='login'),
    path('energy/user', UserEnergyDataView.as_view(), name='user-energy-data'),
    path('energy/filter', FilterEnergyDataView.as_view(), name='filter-energy-data'),
]