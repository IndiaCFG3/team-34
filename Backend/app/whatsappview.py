from rest_framework import status
from .models import CustomToken, Mobilizer, OperationManager, Event
from .serializers import (
    MobilizerSerializer, OperationManagerSerializer, CustomTokenSerializer, EventSerializer)
from .helper_functions import get_object, get_token
from rest_framework.response import Response


class whatsappMessage(APIView):
    def post(self, request):
        req_data = request.data
        try:
            user = Mobilizer.objects.get(phone_no=req_data['FROM'])
        except Mobilizer.DoesNotExist:
            return Response({"message": "Invalid Phone Number"}, status=status.HTTP_400_BAD_REQUEST)
        
        