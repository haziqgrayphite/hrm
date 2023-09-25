from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from .models import CustomUser
from .serializers import CustomUserSerializer


class UserApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        pk = pk
        if pk is not None:
            try:
                user = CustomUser.objects.get(pk=pk)
                serializer = CustomUserSerializer(user)
                return Response(serializer.data)

            except ObjectDoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        serializer = CustomUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'complete data updated'})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'partial data updated'})

        return Response(serializer.errors)

    def delete(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        user.delete()
        return Response({'msg': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class GoogleLoginView(SocialLoginView):
    authentication_classes = []
    adapter_class = GoogleOAuth2Adapter
    callback_url = 'http://localhost:3000/api/auth/callback/google'
    client_class = OAuth2Client

    def get_response(self):
        response = super().get_response()
        user = self.user  # Get the user from the response
        custom_user = CustomUser.objects.get(pk=user.pk)  # Adjust this to fetch your custom user
        response.data['gender'] = custom_user.gender
        response.data['role'] = custom_user.role

        return response




