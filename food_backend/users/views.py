from rest_framework.views import APIView
from .serializers import (AdminRegisterSerializers, AdminLoginSerializers, 
                          StudentRegisterSerializers, StudentLoginSerializers,
                          CanteenSerializers, CanteenWorkersSerializers)
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password, make_password
from users.models import AdminDetails, StudentDetails, CanteenDetails, canteenWorkers
from administration.models import Tenant

# Create your views here.
class AdminRegisterView(APIView):
    def post(self, request):
        serializer= AdminRegisterSerializers(data= request.data)
        
        serializer.is_valid(raise_exception= True)
        username= serializer.validated_data['username']
        email= serializer.validated_data['email']
        password= serializer.validated_data['password']
        tenant= serializer.validated_data['tenant']
        logo= serializer.validated_data['logo']

        admin= AdminDetails.objects.create(
            username= username,
            email= email,
            password= make_password(password),
            tenant= tenant,
            logo= logo
        )
        admin.save()

        return Response({
            'message':'Account Created Successfully',
            'success': True,
            'error': False,
            'data': serializer.data
            }, status= status.HTTP_200_OK)

class AdminLoginView(APIView):
    
    def post(self, request):
        serializer= AdminLoginSerializers(data= request.data)
        
        serializer.is_valid(raise_exception= True)
        email= serializer.validated_data['email']
        password= serializer.validated_data['password']

        admin= AdminDetails.objects.get(email= email)
        Tokens= RefreshToken.for_user(admin)
        admin_serializer = AdminLoginSerializers(admin)

        if check_password(password, admin.password):
            return Response(
                {
                    'message': 'Login Successfully',
                    'Refresh': str(Tokens),
                    'Access': str(Tokens.access_token),
                    'data': admin_serializer.data,
                    'success': True,
                    'error': False
                }, status= status.HTTP_200_OK
            )
            
        else:
            return Response(
                {
                    "message": "Please Check Your Password",
                    'success': False,
                    'error': True
                }, status= status.HTTP_400_BAD_REQUEST
            )           
        
class StudentRegisterView(APIView):
    permission_classes= [IsAuthenticated]
    authentication_classes= [JWTAuthentication]

    def get(self, request):
        student_pk= request.data.get('student_pk')
        if student_pk:
            try:
                category = StudentDetails.objects.get(id=student_pk)
                serializer = StudentRegisterSerializers(category)
                return Response({
                    'data':serializer.data, 
                    'success':True,
                    'error':False}, status= status.HTTP_200_OK)
            
            except StudentDetails.DoesNotExist:
                return Response({
                    "error": "Student not found",
                    'success':False,
                    'error': True
                    }, status=status.HTTP_404_NOT_FOUND)
        else:
            category=StudentDetails.objects.all()
            serializer = StudentRegisterSerializers(category, many= True)
            return Response({
                    'data':serializer.data,
                    'success':True,
                    'error':False}, status= status.HTTP_200_OK)

    def post(self, request):
        serializer= StudentRegisterSerializers(data= request.data)
        
        serializer.is_valid(raise_exception= True)
        first_name= serializer.validated_data['first_name']
        last_name= serializer.validated_data['last_name']
        email= serializer.validated_data['email']
        contact_number= serializer.validated_data['contact_number']
        student_id= serializer.validated_data['student_id']
        date_of_birth= serializer.validated_data['date_of_birth']
        tenant= serializer.validated_data['tenant']
        logo= serializer.validated_data['logo']

        student= StudentDetails.objects.create(
            first_name= first_name,
            last_name= last_name,
            email= email,
            contact_number= contact_number,
            student_id= student_id,
            date_of_birth= date_of_birth,
            tenant= tenant,
            logo= logo
        )
        student.save()

        return Response({
            'message':'Account Created Successfully',
            'error': False,
            'success': True,
            'data': serializer.data
            }, status= status.HTTP_200_OK
            )
    
class StudentLoginView(APIView):
    def get(self, request, *args, **kwargs):
        student_id= request.data.get('student_id')
        student= StudentDetails.objects.filter(student_id= student_id).first()
        serializer= StudentLoginSerializers(student)
        if student:
            return Response(
                 {
                      'message': 'Valid Student ID',
                      'success': True,
                      'error': False,
                      'data': serializer.data
                      
                 }, status= status.HTTP_200_OK
            )
        else:
            return Response(
                 {
                    "message": "Invalid Student ID",
                    'success': False,
                    'error': True
                }, status= status.HTTP_401_UNAUTHORIZED
            )
        
    def post(self, request, *args, **kwargs):
        student_id= request.data.get('student_id')
        password= request.data.get('password')
        
        student= StudentDetails.objects.get(student_id= student_id)
        serializer= StudentLoginSerializers(student)
        if student.is_active == True:
            Tokens= RefreshToken.for_user(student)
            if check_password(password, student.password):
                return Response(
                    {
                        'message': 'Login Successfully',
                        'Refresh': str(Tokens),
                        'Access': str(Tokens.access_token),
                        'data': serializer.data,
                        'success': True,
                        'error': False
                        
                    }, status= status.HTTP_200_OK
                )
            
            else:
                return Response(
                    {
                        "message": "Please Check Your Password",
                        'success': False,
                        'error': True
                    }, status= status.HTTP_400_BAD_REQUEST
                )
        
        else:
             return Response(
                 {
                    "message": "Inactive Student",
                    'data': serializer.data,
                    'success': True,
                    'error': False
                }, status= status.HTTP_400_BAD_REQUEST
            )
        
class StudentSetPasswordView(APIView):
     def post(self, request, *args, **kwargs):
        student_id= request.data.get('student_id')
        new_password= request.data.get('new_password')

        if not StudentDetails.objects.filter(student_id= student_id).exists():
                return Response(
                    {
                    'message':'Invalid Student Id',
                    'success': False,
                    'error': True
                    }
                )

        if not new_password:
             return Response(
                  {
                       'message': "Password is required",
                       'success': False,
                       'error': True
                  }, status= status.HTTP_400_BAD_REQUEST
             )
        
        student= get_object_or_404(StudentDetails, student_id= student_id)
        student.password= make_password(new_password)
        student.is_active= True
        student.save()
        return Response(
                {
                    "message": "Password set successfully.",
                    'success': True,
                    'error': False
                }, status=status.HTTP_200_OK
            )

class CanteenRegisterView(APIView):
    permission_classes= [IsAuthenticated]
    authentication_classes= [JWTAuthentication]

    def get(self, request):
        canteen_pk= request.data.get('canteen_pk')
        if canteen_pk:
            try:
                category = CanteenDetails.objects.get(id=canteen_pk)
                serializer = CanteenSerializers(category)
                return Response({
                    'data':serializer.data, 
                    'success':True,
                    'error':False}, status= status.HTTP_200_OK)
            
            except CanteenDetails.DoesNotExist:
                return Response({
                    "error": "Canteen not found",
                    'success':False,
                    'error': True
                    }, status=status.HTTP_404_NOT_FOUND)
        else:
            category=CanteenDetails.objects.all()
            serializer = CanteenSerializers(category, many= True)
            return Response({
                    'data':serializer.data,
                    'success':True,
                    'error':False}, status= status.HTTP_200_OK)

    def post(self, request):
        serializer= CanteenSerializers(data= request.data)
        serializer.is_valid(raise_exception= True)

        canteen= serializer.validated_data['canteen']
        canteen_name= serializer.validated_data['canteen_name']
        opening_time= serializer.validated_data['opening_time']
        closing_time= serializer.validated_data['closing_time']
        is_available= serializer.validated_data['is_available']
        is_active= serializer.validated_data['is_active']
        tenant= serializer.validated_data['tenant']
        logo= serializer.validated_data['logo']

        canteen= CanteenDetails.objects.create(
            canteen_id= canteen,
            canteen_name= canteen_name,
            opening_time= opening_time,
            closing_time= closing_time,
            is_available= is_available,
            is_active= is_active,
            tenant= tenant,
            logo= logo
        )
        canteen.save()
        return Response({
            'message':'Canteen Created Successfully',
            'error': False,
            'success': True,
            'data': serializer.data
            }, status= status.HTTP_200_OK
        )

class CanteenWorkersView(APIView):
    permission_classes= [IsAuthenticated]
    authentication_classes= [JWTAuthentication]

    def get(self, request):
        worker_pk= request.data.get('worker_pk')
        if worker_pk:
            try:
                category = canteenWorkers.objects.get(id=worker_pk)
                serializer = CanteenWorkersSerializers(category)
                return Response({
                    'data':serializer.data, 
                    'success':True,
                    'error':False}, status= status.HTTP_200_OK)
            
            except canteenWorkers.DoesNotExist:
                return Response({
                    "error": "Canteen Staff not found",
                    'success':False,
                    'error': True
                    }, status=status.HTTP_404_NOT_FOUND)
        else:
            category=canteenWorkers.objects.all()
            serializer = CanteenWorkersSerializers(category, many= True)
            return Response({
                    'data':serializer.data,
                    'success':True,
                    'error':False}, status= status.HTTP_200_OK)

    def post(self, request):
        serializer= CanteenWorkersSerializers(data= request.data)

        serializer.is_valid(raise_exception=True)

        canteen= serializer.validated_data['canteen']
        staff_id= serializer.validated_data['staff_id']
        first_name= serializer.validated_data['first_name']
        last_name= serializer.validated_data['last_name']
        email= serializer.validated_data['email']
        password= serializer.validated_data['password']
        contact_number= serializer.validated_data['contact_number']
        tenant= serializer.validated_data['tenant']   
        logo= serializer.validated_data['logo']      
        
        canteen_workers= canteenWorkers.objects.create(
            canteen= canteen,
            staff_id= staff_id,
            first_name= first_name,
            last_name= last_name,
            email= email,
            password= make_password(password),
            contact_number= contact_number,
            tenant= tenant,
            logo= logo
        )
        canteen_workers.save()

        return Response({
            'message':'Canteen Worker Created Successfully',
            'error': False,
            'success': True,
            'data': serializer.data
            }, status= status.HTTP_200_OK
        )

class CanteenWorkerLoginView(APIView):
    def get(self, request, *args, **kwargs):
        staff_id= request.data.get('staff_id')
        worker= canteenWorkers.objects.filter(staff_id= staff_id).first()
        serializer= CanteenWorkerLoginView(worker)
        if worker:
            return Response(
                 {
                      'message': 'Valid Staff ID',
                      'error': False,
                      'success': False,
                      'data': serializer.data
                      
                 }, status= status.HTTP_200_OK
            )
        else:
            return Response(
                 {
                    "message": "Invalid Staff ID",
                    'success': False,
                    'error': True
                }, status= status.HTTP_401_UNAUTHORIZED
            )
        
    def post(self, request, *args, **kwargs):
        staff_id= request.data.get('staff_id')
        password= request.data.get('password')
        
        worker= canteenWorkers.objects.get(staff_id= staff_id)
        serializer= CanteenWorkersSerializers(worker)
        if worker.is_active == True:
            Tokens= RefreshToken.for_user(worker)
            if check_password(password, worker.password):
                return Response(
                    {
                        'message': 'Login Successfully',
                        'Refresh': str(Tokens),
                        'Access': str(Tokens.access_token),
                        'data': serializer.data,
                        'success': True,
                        'error': False
                        
                    }, status= status.HTTP_200_OK
                )
            
            else:
                return Response(
                    {
                        "message": "Please Check Your Password",
                        'success': False,
                        'error': True
                    }, status= status.HTTP_400_BAD_REQUEST
                )
        
        else:
             return Response(
                 {
                    "message": "Inactive Student",
                    'data': serializer.data,
                    'success': True,
                    'error': False
                }, status= status.HTTP_400_BAD_REQUEST
            )
        
class staffSetPasswordView(APIView):
     def post(self, request, *args, **kwargs):
        staff_id= request.data.get('staff_id')
        new_password= request.data.get('new_password')

        if not canteenWorkers.objects.filter(staff_id= staff_id).exists():
                return Response(
                    {
                    'message':'Invalid Staff Id',
                    'success': False,
                    'error': True
                    }
                )

        if not new_password:
             return Response(
                  {
                       'message': "Password is required",
                       'success': False,
                       'error': True
                  }, status= status.HTTP_400_BAD_REQUEST
             )
        
        worker= get_object_or_404(canteenWorkers, staff_id= staff_id)
        worker.password= make_password(new_password)
        worker.is_active= True
        worker.save()
        return Response(
                {
                    "message": "Password set successfully.",
                    'success': True,
                    'error': False
                }, status=status.HTTP_200_OK
            )
