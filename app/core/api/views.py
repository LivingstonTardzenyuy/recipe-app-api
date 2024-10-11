from rest_framework import generics, authentication, permissions
from .serializers import (UserSerializer, AuthTokenSerializer,)
from .permissions import (UpdateYourProfile,)

from rest_framework.authtoken.views import ObtainAuthToken 
from rest_framework.settings import api_settings

class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """
        Create a new auth token for user
    """
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES        # output type: json, xml etc...
    
class ManageUserView(generics.RetrieveUpdateAPIView):
    """
        Manage the authenticated user
    """
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]   # descript the auth classes to use  for authentication  purposes 
    permission_classes = [permissions.IsAuthenticated, UpdateYourProfile]
    
    def get_queryset(self):
        return self.request.user 