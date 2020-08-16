from datetime import datetime
import hashlib

from twilio.rest import Client
import pyexcel
import xlrd
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.shortcuts import render

from django.contrib import admin
from django.urls import path
# from chartjs import views

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser

from .models import CustomToken, Mobilizer, OperationManager, Event, Students
from .serializers import (
    MobilizerSerializer, OperationManagerSerializer, CustomTokenSerializer, EventSerializer, StudentsSerializer)
from .helper_functions import get_object, get_token


# Ping Server
class PingView(APIView):

    def get(self, request):
        return Response({"message": "OK"}, status=status.HTTP_200_OK)


###############################################################################################################
# Mobilizer

class MobilizerSignupView(APIView):

    # Sigup user (create new object)
    def post(self, request):

        user_data = {}
        user_data['username'] = request.data.get("username", None)
        user_data['phone_no'] = request.data.get("phone_no", None)
        user_data['om_id'] = request.data.get("om_id", None)
        user_data['password'] = request.data.get("password", None)
        if len(user_data['password']) < 6:
            return Response({"Invalid Password"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = MobilizerSerializer(data=user_data)

        if serializer.is_valid():
            serializer.save()

            user = list(Mobilizer.objects.filter(
                phone_no=user_data['phone_no']))[0]

            token = get_token(user.id, 1)
            user_data['token'] = token
            del user_data['password']
            try:
                usertoken = CustomToken.objects.get(
                    object_id=user.id, user_type=1)
                return Response({"message": "User Already Logged in", "Mobilizer": user_data}, status=status.HTTP_400_BAD_REQUEST)
            except CustomToken.DoesNotExist:
                CustomToken.objects.create(
                    user_type=1,
                    object_id=user.id,
                    token=token
                )
                return Response({"message": "User Signed up successfully", "Mobilizer": user_data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# View for user login
class MobilizerLoginView(APIView):

    def post(self, request):
        req_data = request.data
        try:
            user = list(Mobilizer.objects.filter(
                phone_no=req_data['phone_no']))[0]
        except Mobilizer.DoesNotExist:
            return Response({"message": "Invalid Phone Number"}, status=status.HTTP_400_BAD_REQUEST)

        m = hashlib.md5()
        m.update(req_data['password'].encode("utf-8"))
        if user.password == str(m.digest()):
            token = get_token(user.id, 1)
            try:
                usertoken = CustomToken.objects.get(
                    object_id=user.id, user_type=1)
                token = usertoken.token
            except CustomToken.DoesNotExist:
                CustomToken.objects.create(
                    user_type=1,
                    object_id=user.id,
                    token=token
                )
            return Response({"message": "User Logged in",
                             "User": {
                                 "id": user.id,
                                 "username": user.username,
                                 "phone_no": user.phone_no,
                                 "token": token
                             }
                             })
        else:
            return Response({"message": "Invalid Password"}, status=status.HTTP_403_FORBIDDEN)


# Signout new user
class MobilizerLogoutView(APIView):

    def get(self, request, format=None):

        # Get User and delete the token
        token = request.headers.get('Authorization', None)
        if token is None or token == "":
            return Response({"message": "Authorization credentials missing"}, status=status.HTTP_403_FORBIDDEN)

        user = get_object(token)
        if user is None:
            return Response({"message": "User Already Logged Out"}, status=status.HTTP_403_FORBIDDEN)

        response = {
            "message": "User logged out",
            "Details": {
                "id": user.id,
                "username": user.username,
                "phone_no": user.phone_no,
                "om_id": user.om_id.id
            }}

        usertoken = CustomToken.objects.get(object_id=user.id, user_type=1)
        usertoken.delete()
        return Response(response, status=status.HTTP_200_OK)


class MobilizerDetailsView(APIView):

    def get(self, request):
        token = request.headers.get('Authorization', None)
        if token is None or token == "":
            return Response({"message": "Authorization credentials missing"}, status=status.HTTP_403_FORBIDDEN)

        user = get_object(token)
        if user is None:
            return Response({"message": "User Not Found"}, status=status.HTTP_403_FORBIDDEN)
        response = {
            "message": "User details",
            "User": {
                "id": user.id,
                "username": user.username,
                "phone_no": user.phone_no,
                "om_id": user.om_id.id
            }}
        return Response(response, status=status.HTTP_200_OK)


###############################################################################################################
# Operation Manager

class OperationManagerSignupView(APIView):

    # Sigup user (create new object)
    def post(self, request):

        user_data = {}
        user_data['username'] = request.data.get("username", None)
        user_data['phone_no'] = request.data.get("phone_no", None)
        user_data['password'] = request.data.get("password", None)
        if len(user_data['password']) < 6:
            return Response({"Invalid Password"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = OperationManagerSerializer(data=user_data)

        if serializer.is_valid():
            serializer.save()

            user = list(OperationManager.objects.filter(
                phone_no=user_data['phone_no']))[0]

            token = get_token(user.id, 0)
            user_data['token'] = token
            del user_data['password']
            try:
                usertoken = CustomToken.objects.get(
                    object_id=user.id, user_type=0)
                return Response({"message": "User Already Logged in", "OperationManager": user_data}, status=status.HTTP_400_BAD_REQUEST)
            except CustomToken.DoesNotExist:
                CustomToken.objects.create(
                    user_type=0,
                    object_id=user.id,
                    token=token
                )
                return Response({"message": "User Signed up successfully", "OperationManager": user_data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# View for user login
class OperationManagerLoginView(APIView):

    def post(self, request):
        req_data = request.data
        try:
            user = list(OperationManager.objects.filter(
                phone_no=req_data['phone_no']))[0]
        except OperationManager.DoesNotExist:
            return Response({"message": "Invalid Phone Number"}, status=status.HTTP_400_BAD_REQUEST)

        m = hashlib.md5()
        m.update(req_data['password'].encode("utf-8"))
        if user.password == str(m.digest()):
            token = get_token(user.id, 0)
            try:
                usertoken = CustomToken.objects.get(
                    object_id=user.id, user_type=1)
                token = usertoken.token
            except CustomToken.DoesNotExist:
                CustomToken.objects.create(
                    user_type=0,
                    object_id=user.id,
                    token=token
                )
            return Response({"message": "User Logged in",
                             "User": {
                                 "id": user.id,
                                 "username": user.username,
                                 "phone_no": user.phone_no,
                                 "token": token
                             }
                             })
        else:
            return Response({"message": "Invalid Password"}, status=status.HTTP_403_FORBIDDEN)


# Signout new user
class OperationManagerLogoutView(APIView):

    def get(self, request, format=None):

        # Get User and delete the token
        token = request.headers.get('Authorization', None)
        if token is None or token == "":
            return Response({"message": "Authorization credentials missing"}, status=status.HTTP_403_FORBIDDEN)

        user = get_object(token)
        if user is None:
            return Response({"message": "User Already Logged Out"}, status=status.HTTP_403_FORBIDDEN)

        response = {
            "message": "User logged out",
            "Details": {
                "id": user.id,
                "username": user.username,
                "phone_no": user.phone_no
            }}

        usertoken = CustomToken.objects.get(object_id=user.id, user_type=1)
        usertoken.delete()
        return Response(response, status=status.HTTP_200_OK)


class OperationManagerDetailsView(APIView):

    def get(self, request):
        token = request.headers.get('Authorization', None)
        if token is None or token == "":
            return Response({"message": "Authorization credentials missing"}, status=status.HTTP_403_FORBIDDEN)

        user = get_object(token)
        if user is None:
            return Response({"message": "User Not Found"}, status=status.HTTP_403_FORBIDDEN)
        response = {
            "message": "User details",
            "User": {
                "id": user.id,
                "username": user.username,
                "phone_no": user.phone_no
            }}
        return Response(response, status=status.HTTP_200_OK)


##########################################################################
class GetMobilizerView(APIView):

    def get(self, request):
        token = request.headers.get('Authorization', None)
        if token is None or token == "":
            return Response({"message": "Authorization credentials missing"}, status=status.HTTP_403_FORBIDDEN)

        user = get_object(token)
        if user is None:
            return Response({"message": "User Not Found"}, status=status.HTTP_403_FORBIDDEN)

        mobilizers = Mobilizer.objects.filter(om_id=user.id)
        serializer = MobilizerSerializer(mobilizers, many=True)
        return Response({"Mobilizers": serializer.data}, status=200)


######################################################
class EventView(APIView):

    def post(self, request):
        token = request.headers.get('Authorization', None)
        if token is None or token == "":
            return Response({"message": "Authorization credentials missing"}, status=status.HTTP_403_FORBIDDEN)

        user = get_object(token)
        if user is None:
            return Response({"message": "User Not Found"}, status=status.HTTP_403_FORBIDDEN)

        request.data['mobiliser_id'] = user.id
        data = EventSerializer(data=request.data)
        if data.is_valid():
            data.save()

            return Response({"message": data.data}, status=200)

        return Response({"message": data.error_messages}, status=400)

    def patch(self, request):
        token = request.headers.get('Authorization', None)
        if token is None or token == "":
            return Response({"message": "Authorization credentials missing"}, status=status.HTTP_403_FORBIDDEN)

        user = get_object(token)
        if user is None:
            return Response({"message": "User Not Found"}, status=status.HTTP_403_FORBIDDEN)

        comment = request.data.get('comments', None)
        participants = request.data.get('participants', None)
        status = request.data.get('status', False)
        event_id = request.data.get('id', None)

        event = list(Event.objects.filter(id=event_id))[0]
        event.comments = comment
        event.participants = participants
        event.status = status
        event.save()

        return Response({"message": "Event Updated"}, status=200)

    def get(self, request, pk):
        events = Event.objects.filter(mobiliser_id=pk)
        serializer = EventSerializer(events, many=True)
        return Response({"Events": serializer.data}, status=200)


########################################################################################################
# class MobilizerChartData(APIView):
#     authentication_classes = []
#     permission_classes = []

#     def get(self, request, format = None):
#         labels = list(Mobilizer.objects.values_list('username'))
#         chartLabel = "Mobilizer-Graph"
#         chartdata = list(Mobilizer.objects.values_list('score'))
#         data ={
#                      "labels":labels,
#                      "chartLabel":chartLabel,
#                      "chartdata":chartdata,
#              }
#         return Response(data)

#################################################################################

class StudentsDetails(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request):
        token = request.headers.get('Authorization', None)
        if token is None or token == "":
            return Response({"message": "Authorization credentials missing"}, status=status.HTTP_403_FORBIDDEN)

        user = get_object(token)
        if user is None:
            return Response({"message": "User Not Found"}, status=status.HTTP_403_FORBIDDEN)

        file = request.data['file']
        extension = file.name.split('.')[-1]
        if extension not in ['csv', 'xls', 'xlsx']:
            return Response({"message": "Invalid File Format"}, status=status.HTTP_400_BAD_REQUEST)

        content = file.read()
        records = pyexcel.iget_records(
            file_type=extension, file_content=content)
        response = []
        print("____________________________________________________________________")
        for record in records:
            student = {
                "username": record.get('name', None),
                "phone_no": record.get('phone_no', None),
                "event_id": int(record.get('event_id', None)),
                "mobiliser_id": user.id
            }

            ser = StudentsSerializer(data=student)
            if ser.is_valid():
                ser.save()
                response.append(student)
            else:
                print(ser.errors)

        return Response({"students": response}, status=200)

    def get(self, request):
        token = request.headers.get('Authorization', None)
        if token is None or token == "":
            return Response({"message": "Authorization credentials missing"}, status=status.HTTP_403_FORBIDDEN)

        user = get_object(token)
        if user is None:
            return Response({"message": "User Not Found"}, status=status.HTTP_403_FORBIDDEN)

        students = (Students.objects.filter(mobiliser_id=user.id))
        ser = StudentsSerializer(students)
        return Response({"Students": ser.data}, status=200)


###############################################################################


class WhatsappStudentsDetails(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request):
        print(request.data)
        whatsapp = request.data.get("From", None)[0]  # whatsapp:+919421014582
        number = whatsapp[12:]
        url = request.data.get("MediaUrl0", None)[0]
        print(url)
        mobilizer = list(Mobilizer.objects.filter(phone_no=number))[0]
        events = Event.objects.filter(mobiliser_id=mobilizer.id)
        for eve in events:
            eve.filename = url
            eve.save()
        account_sid = 'ACdebef1d5250611c5f3038a415613dacb'

        auth_token = '080729e2c815327e765b4b783261198c'
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body='We have recieved your file',
            to='whatsapp:+919421014582'  # change this number  # to whoever is demonstrating
        )
        return Response({"students": "Done"}, status=200)


#################################################################################


class GetDataMobiliser(APIView):

    def get(self, request, pk):
        events = list(Event.objects.filter(mobiliser_id=pk))
        eventsDone = list(Event.objects.filter(
            mobiliser_id=pk, status="Completed"))
        students = list(Students.objects.filter(mobiliser_id=pk))
        studentsDone = list(Students.objects.filter(
            mobiliser_id=pk, is_converted=True))

        data = {
            "total_event": len(events),
            "events_done": len(eventsDone),
            "total_students": len(students),
            "converted_leads": len(studentsDone)
        }

        return Response({"data": data}, status=200)
