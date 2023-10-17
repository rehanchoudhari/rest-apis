from django.contrib.auth.models import User
from rest_framework import viewsets, mixins
from .serializers import UserSerializer, ProfileSerializer
from .permissions import IsUserOwnerOrGetAndPostOnly, IsProfileOwnerOrGetAndPostOnly
from .models import Profile

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsUserOwnerOrGetAndPostOnly,]
    queryset = User.objects.all()
    serializer_class = UserSerializer

# we can also also add some functionality like delete and create using below mixins
# ---------------------------mixin.CreateModelMixin, mixin.DestoryModelMixin-------------------------------------------#
class ProfileViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
# class ProfileViewSet(viewsets.ModelViewSet): ModelViewSet provide all the functionality of the api.
    permission_classes = [IsProfileOwnerOrGetAndPostOnly,]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
