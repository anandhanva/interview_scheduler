import logging
import random

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.viewsets import ViewSet
from django.db import IntegrityError
from .models import UserDetails
from .serializers import UserDetailsSerializer
from .services.commonServices import CommonServiceImpl

from datetime import datetime, date, timedelta

logger = logging.getLogger(__name__)

# Create your views here.

class TestViewService(ViewSet):

    # for connectivity check
    @action(detail=False, methods=['get'])
    def test_service(self, request):
        return Response({"message": "This is a test GET request"}, status=status.HTTP_200_OK)

class InterviewService(ViewSet):

    @action(detail=False, methods=['post'])
    def register_time_slot(self, request):

        class_name = InterviewService.__name__
        common_service = CommonServiceImpl()
        request_id = "REQ-"+str(random.randint(100,9999999))
        try:
            
            request_data = request.data
            logger.info("Request Check"+str(request_data),extra={"request_id":request_id,"class_name":class_name})

            required_fields = ['name', 'type', 'email','date','hrs_from', 'hrs_to']
            for field in required_fields:
                if field not in request.data:
                    return Response({"error": f"{field.capitalize()} is required", "request_id": request_id}, status=status.HTTP_400_BAD_REQUEST)
            
            type = "I"
            if request_data['type'] == 'candidate':
                type = "C"
            
            gen_user_id = common_service.generate_unique_id(UserDetails,'user_id',type)

            request_data['hrs_from'] = datetime.strptime(request_data['hrs_from'], '%I %p').strftime('%H')
            request_data['hrs_to'] = datetime.strptime(request_data['hrs_to'], '%I %p').strftime('%H')

            data = {
                'user_id':gen_user_id,
                'user_name':request_data['name'],
                "user_type":request_data['type'],
                "user_mail":request_data['email'],
                "slot_date":request_data['date'],
                "time_slot_from":request_data['hrs_from'],
                "time_slot_to":request_data['hrs_to']
                }
            logger.info("Serializer Check "+str(data), extra={"request_id": request_id, "class_name": class_name})

            if UserDetails.objects.filter(user_mail=request_data['email']).exists():
                logger.info("Email already exists.",extra={"request_id":request_id,"class_name":class_name})
                return Response({"error": "Email already exists.","request_id":request_id}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = UserDetailsSerializer(data=data)
            if serializer.is_valid():
                if int(request_data['hrs_from']) < 9 or int(request_data['hrs_from']) > 18:
                    return Response({"error": "Hrs From should be between 9 and 18","request_id":request_id}, status=status.HTTP_400_BAD_REQUEST)
                
                if int(request_data['hrs_to']) < int(request_data['hrs_from']):
                    return Response({"error": "Hrs To should be greater than Hrs From","request_id":request_id}, status=status.HTTP_400_BAD_REQUEST)
                
                if int(request_data['hrs_to']) > 18 or int(request_data['hrs_to']) < 9:
                    return Response({"error": "Hrs To should be between 9 and 18","request_id":request_id}, status=status.HTTP_400_BAD_REQUEST)
                
                request_date = datetime.strptime(request_data['date'], '%Y-%m-%d').date()
                if request_date < date.today():
                    return Response({"error": "Previous date not available","request_id":request_id}, status=status.HTTP_400_BAD_REQUEST)
                
                try:
                    # saving the validated data to the database
                    serializer.save()
                    logger.info("User registration successful", extra={"request_id": request_id, "class_name": class_name})
                    return Response({"message": "User Registration Success", "request_id": request_id,'user_id':gen_user_id}, status=status.HTTP_200_OK)
                
                except IntegrityError as db_error:
                    logger.error(f"Integrity Error: {db_error}", extra={"request_id": request_id, "class_name": class_name})
                    return Response({"error": "Database Integrity Error", "request_id": request_id}, status=status.HTTP_400_BAD_REQUEST)
                
                except Exception as error:
                    logger.error(f"Exception Error: {error}", extra={"request_id": request_id, "class_name": class_name})
                    return Response({"error": "Data Insertion Failed", "request_id": request_id}, status=status.HTTP_400_BAD_REQUEST)
            
            else:
                logger.error(f"Invalid data: {serializer.errors}", extra={"request_id": request_id, "class_name": class_name})
                return Response({"error": "Invalid data", "errors": serializer.errors, "request_id": request_id}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as view_error:
            logger.error("Process Error Occurred: %s", str(view_error), extra={"request_id": request_id, "class_name": class_name})
            return Response({"error": "Process Failed", "request_id": request_id}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def fetch_time_slot(self, request):

        class_name = InterviewService.__name__
        request_id = "REQ-"+str(random.randint(100,9999999))
        try:

            request_data = request.data
            logger.info("Request Check"+str(request_data),extra={"request_id":request_id,"class_name":class_name})

            required_fields = ['candidate_id', 'interviewer_id']
            for field in required_fields:
                if field not in request.data:
                    return Response({"error": f"{field.capitalize()} is required", "request_id": request_id}, status=status.HTTP_400_BAD_REQUEST)
                
            # fetch candidate registration details
            candidate_id = request_data['candidate_id']
            candidate_user_data = UserDetails.objects.filter(user_id=candidate_id)
            serializer = UserDetailsSerializer(candidate_user_data, many=True)
            candidate_data = serializer.data
            logger.info("Candidate User Data "+str(candidate_data),extra={"request_id":request_id,"class_name":class_name})

            # fetch interviewer registration details
            interviewer_id = request_data['interviewer_id']
            interviewer_user_data = UserDetails.objects.filter(user_id=interviewer_id)
            serializer = UserDetailsSerializer(interviewer_user_data, many=True)
            interviewer_data = serializer.data
            logger.info("Interviewer User Data "+str(interviewer_data),extra={"request_id":request_id,"class_name":class_name})

            overlap_start = max(candidate_data[0]['time_slot_from'], interviewer_data[0]['time_slot_from'])
            overlap_end = min(candidate_data[0]['time_slot_to'], interviewer_data[0]['time_slot_to'])

            if overlap_start >= overlap_end:
                return Response({"message": "No overlapping time slots available.","request_id":request_id}, status=status.HTTP_200_OK)
            
            if interviewer_data[0]['slot_date'] != candidate_data[0]['slot_date']:
                return Response({"message": "No overlapping date available .","request_id":request_id}, status=status.HTTP_200_OK)
            
            date_slot = interviewer_data[0]['slot_date']
            time_slots = []
            current_time = overlap_start
            while current_time < overlap_end:
                start_time = datetime.strptime(f"{current_time}:00", "%H:%M")
                end_time = start_time + timedelta(hours=1)
                time_slots.append((start_time.strftime("%I:%M %p"), end_time.strftime("%I:%M %p")))
                current_time += 1
            
            return Response({"available_time_slots": time_slots,"message": "Slots are available .",
                            "request_id":request_id,"date":date_slot}, status=status.HTTP_200_OK)

        except Exception as view_error:
            logger.error("Error : Process Error Occurred "+str(view_error),extra={"request_id":request_id,"class_name":class_name})
            return Response({"Error": "Process Failed","request_id":request_id}, status=status.HTTP_400_BAD_REQUEST)