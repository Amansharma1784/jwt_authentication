from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Student
from .serializers import UserSerializer

class StudentModelViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]        # 👈 JWT authentication
    permission_classes = [IsAuthenticated]              # 👈 Only authenticated users allowed
