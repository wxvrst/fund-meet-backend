from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from drf_yasg.utils import swagger_auto_schema


from core.models import UserModel
from django.contrib.auth import login, logout
from core.serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
)


class RegisterView(generics.CreateAPIView):
    queryset = UserModel.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token.key,
            "message": "User created successfully"
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token, created = Token.objects.get_or_create(user=user)

            login(request, user)

            return Response({
                "user": UserSerializer(user).data,
                "token": token.key
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            request.user.auth_token.delete()
        except:
            pass

        logout(request)

        return Response({"message": "Successfully logged out"},
                        status=status.HTTP_200_OK)



class UserListView(generics.ListAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = UserModel.objects.all()
    lookup_field = 'id'


class UpdateUserView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class CurrentUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response({
            'user': serializer.data,
            'is_authenticated': user.is_authenticated,
            'email': user.email,
        })

