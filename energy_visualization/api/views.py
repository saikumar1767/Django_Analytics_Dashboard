from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, EnergyData
from .serializers import UserSerializer, EnergyDataSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponse
import datetime
from rest_framework import status

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': user.username,
            })
        return Response({"error": "Invalid username or password"}, status=400)

class UserEnergyDataView(generics.ListAPIView):
    serializer_class = EnergyDataSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return EnergyData.objects.filter(username=self.request.user.username)

class FilterEnergyDataView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        start_datetime = request.query_params.get('start_datetime')
        end_datetime = request.query_params.get('end_datetime')
        energy_source = request.query_params.get('energy_source')
        energy_data = EnergyData.objects.filter(username=request.user.username)

        if start_datetime and end_datetime:
            energy_data = energy_data.filter(timestamp__range=[start_datetime, end_datetime])
        if energy_source and energy_source != "all":
            energy_data = energy_data.filter(energy_source=energy_source)
        
        serializer = EnergyDataSerializer(energy_data, many=True)
        return Response(serializer.data)

def home_page(request):
    print(f"Home page accessed at {datetime.datetime.now()}")
    return HttpResponse("Server is Up and running!")
