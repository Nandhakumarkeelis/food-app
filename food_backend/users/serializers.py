from rest_framework import serializers
from .models import AdminDetails, StudentDetails, CanteenDetails, canteenWorkers
from administration.models import Tenant

class Tenantserializers(serializers.ModelSerializer):
    class Meta:
        model= Tenant
        fields='__all__'

class AdminRegisterSerializers(serializers.ModelSerializer):
    tenant = serializers.PrimaryKeyRelatedField(queryset=Tenant.objects.all(), write_only=True)
    tenant_detail= Tenantserializers(source= 'tenant', read_only= True)
    
    class Meta:
        model= AdminDetails
        fields= '__all__' 
    
    username= serializers.CharField(required= True)
    first_name = serializers.CharField(required= False)
    last_name = serializers.CharField(required= False)
    password= serializers.CharField(required= True, write_only=True)
    contact_number= serializers.CharField(required= False)
    email= serializers.EmailField(required= True)
    logo= serializers.CharField(required= False)

    def validate(self, data):
        if data['username']:
            if AdminDetails.objects.filter(username= data['username']).exists():
                raise serializers.ValidationError(
                    {
                    'message':'Username is Already Taken',
                    'success':False,
                    'error': True
                    }
                )
            
        if data['email']:
            if AdminDetails.objects.filter(email= data['email']).exists():
                raise serializers.ValidationError(
                    {
                    'message':'Email is Already Taken',
                    'success':False,
                    'error': True
                    }
                )
            
        return data

class AdminLoginSerializers(serializers.ModelSerializer):
    tenant= Tenantserializers(required= False)
    
    class Meta:
        model= AdminDetails
        fields= '__all__' 

    email= serializers.EmailField(required= True)
    password= serializers.CharField(required= True, write_only=True)

    def validate(self, data):
        if data['email']:
            if not AdminDetails.objects.filter(email= data['email']):
                raise serializers.ValidationError(
                {
                    'message':"Admin with this email does not exist.",
                    'success':False,
                    'error': True
                })
            
        return data

class StudentRegisterSerializers(serializers.ModelSerializer):
    tenant = serializers.PrimaryKeyRelatedField(queryset=Tenant.objects.all(), write_only=True)
    tenant_detail= Tenantserializers(source= 'tenant', read_only= True)

    class Meta:
        model= StudentDetails
        fields= '__all__'

    first_name= serializers.CharField(required= True)
    last_name= serializers.CharField(required= False)
    email= serializers.EmailField(required= True)
    contact_number= serializers.CharField(required= True)
    student_id= serializers.CharField(required= True)
    date_of_birth= serializers.DateField(required= True)
    is_active= serializers.BooleanField(required= False)
    logo= serializers.CharField(required= False)

    def validate(self, data):
        if data['email']:
            if StudentDetails.objects.filter(email= data['email']).exists():
                raise serializers.ValidationError(
                    {
                    'message':'Email is Already Taken',
                    'success':False,
                    'error': True
                    }
                )
            
        if data['email']:
            if AdminDetails.objects.filter(email= data['email']).exists():
                raise serializers.ValidationError(
                    {
                    'message':'Email is Already Taken',
                    'success':False,
                    'error': True
                    }
                )
            
        if data['student_id']:
            if StudentDetails.objects.filter(student_id= data['student_id']).exists():
                raise serializers.ValidationError(
                    {
                    'message':'Student Id is Already Taken',
                    'success':False,
                    'error': True
                    }
                )
            
        return data
    
class StudentLoginSerializers(serializers.ModelSerializer):
    tenant= Tenantserializers(required= False)

    class Meta:
        model= StudentDetails
        fields= '__all__'

class CanteenSerializers(serializers.ModelSerializer):
    tenant = serializers.PrimaryKeyRelatedField(queryset=Tenant.objects.all(), write_only=True)
    tenant_detail= Tenantserializers(source= 'tenant', read_only= True)

    class Meta:
        model= CanteenDetails
        fields= '__all__'

    canteen_id= serializers.CharField(required= True)
    canteen_name= serializers.CharField(required= True)
    opening_time= serializers.DateTimeField(required= True)
    closing_time= serializers.DateTimeField(required= True)
    is_available= serializers.BooleanField(required= True)
    is_active= serializers.BooleanField(required= True)
    logo= serializers.CharField(required= False)

    def validate(self, data):
        if data['canteen_id']:
            if CanteenDetails.objects.filter(canteen_name= data['canteen_id']).exists():
                raise serializers.ValidationError(
                    {
                    'message':'Canteen Id is Already Taken',
                    'success':False,
                    'error': True
                    }
                )

        if data['canteen_name']:
            if CanteenDetails.objects.filter(canteen_name= data['canteen_name']).exists():
                raise serializers.ValidationError(
                    {
                    'message':'Canteen Name is Already Taken',
                    'success':False,
                    'error': True
                    }
                )
            
        return data
    
class CanteenWorkersSerializers(serializers.ModelSerializer):
    tenant = serializers.PrimaryKeyRelatedField(queryset=Tenant.objects.all(), write_only=True)
    tenant_detail= Tenantserializers(source= 'tenant', read_only= True)

    canteen = serializers.PrimaryKeyRelatedField(queryset=CanteenDetails.objects.all(), write_only=True)
    canteen_detail= CanteenSerializers(source= 'canteen', read_only= True)

    class Meta:
        model= canteenWorkers
        fields= '__all__'

    staff_id= serializers.CharField(required= True)
    first_name= serializers.CharField(required= True)
    last_name= serializers.CharField(required= False)
    email= serializers.EmailField(required= True)
    password= serializers.CharField(required= True)
    contact_number= serializers.CharField(required= True)
    logo= serializers.CharField(required= False)

    def validate(self, data):
        
        # if data['canteen']:
        #     if not CanteenDetails.objects.filter(pk= data['canteen']).first():
        #         raise serializers.ValidationError(
        #         {
        #             'message':"Canteen with this id does not exist.",
        #             'success':False,
        #             'error': True
        #         })

        if data['staff_id']:
            if canteenWorkers.objects.filter(staff_id= data['staff_id']).exists():
                raise serializers.ValidationError(
                    {
                    'message':'Staff Id is Already Taken',
                    'success':False,
                    'error': True
                    }
                )
        
        if data['email']:
            if AdminDetails.objects.filter(email= data['email']).exists() or StudentDetails.objects.filter(email= data['email']).exists() or canteenWorkers.objects.filter(email= data['email']).exists():
                raise serializers.ValidationError(
                    {
                    'message':'Email is Already Taken',
                    'success':False,
                    'error': True
                    }
                )
            
        return data
    
class CanteenWorkerLoginSerializers(serializers.ModelSerializer):
    canteen= CanteenSerializers(required=False)
    tenant= Tenantserializers(required= False)

    class Meta:
        model= canteenWorkers
        fields= '__all__'


