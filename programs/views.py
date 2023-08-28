from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Medication, MedicationReminder
from .serializers import MedicationSerializer, MedicationReminderSerializer
from accounts.models import Patient  # Import the Patient model from the other microservice

class MedicationAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        medications = Medication.objects.filter(user=request.user)
        serializer = MedicationSerializer(medications, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        data = dict(request.data)  # Create a new dictionary with the data
        data['user'] = request.user.id
        patient_id = data.pop('patient', None)
        
        patient = None
        if patient_id:
            patient = Patient.objects.filter(id=patient_id).first()
            if not patient:
                return Response(
                    {'error': 'Patient with the provided ID does not exist.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        data['patient'] = patient.id if patient else None

        serializer = MedicationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class MedicationReminderAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        medicationReminders = MedicationReminder.objects.filter(user=request.user)
        serializer = MedicationReminderSerializer(medicationReminders, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        data = dict(request.data)
        data['user'] = request.user.id
        patient_id = data.pop('patient', None)
        
        patient = None
        if patient_id:
            patient = Patient.objects.filter(id=patient_id).first()
            if not patient:
                return Response(
                    {'error': 'Patient with the provided ID does not exist.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        data['patient'] = patient.id if patient else None
        
        serializer = MedicationReminderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

