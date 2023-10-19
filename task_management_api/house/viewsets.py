from rest_framework import viewsets, status
from .models import House
from .serializers import HouseSerializer
from .permissions import IsHouseManagerOrNone
from rest_framework.decorators import action
from rest_framework.response import Response

class HouseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsHouseManagerOrNone, ]
    queryset = House.objects.all()
    serializer_class = HouseSerializer

    @action(detail=True, methods=['post'], name='join')
    def join(self, request, pk=None):
        try:
            house = self.get_object()
            user_profile = request.user.profile
            if user_profile.house == None:
                user_profile.house = house
                user_profile.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            elif user_profile in house.members.all():
                return Response({'detail': 'Already a member in this house.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'detail': 'Already a member in other house'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(detail=True, methods=['post'], name='leave')
    def leave(self, request, pk=None):
        try:
            house = self.get_object()
            user_profile = request.user_profile
            if user_profile in house.members.all():
                user_profile.house = None
                user_profile.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'detail': 'User not a member in this house.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)