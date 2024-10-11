from rest_framework import serializers
from .models import Categories,Products
from users.serializers import Tenantserializers
from administration.models import Tenant

class CategoriesSerializers(serializers.ModelSerializer):
    tenant = serializers.PrimaryKeyRelatedField(queryset=Tenant.objects.all(), write_only=True)
    tenant_detail= Tenantserializers(source= 'tenant', read_only= True)

    class Meta:
        model= Categories
        fields= '__all__'

    category_id= serializers.CharField(required= True)
    category_name= serializers.CharField(required= True)
    description= serializers.CharField(required= False, allow_blank=True)
    logo= serializers.CharField(required= False)
    is_available= serializers.BooleanField(required=False)

    def validate(self, data):
        if data['category_id']:
            if Categories.objects.filter(category_id= data['category_id']).exists():
                raise serializers.ValidationError(
                    {
                    'message':'Category Id is Already Taken',
                    'success':False,
                    'error': True
                    }
                )
            
        if data['category_name']:
            if Categories.objects.filter(category_name= data['category_name']).exists():
                raise serializers.ValidationError(
                    {
                    'message':'Category Name is Already Taken',
                    'success':False,
                    'error': True
                    }
                )
            
        return data

class ProductsSerializers(serializers.ModelSerializer):
     # Use PrimaryKeyRelatedField for write operations (create/update)
    category = serializers.PrimaryKeyRelatedField(queryset=Categories.objects.all(), write_only=True)
    tenant = serializers.PrimaryKeyRelatedField(queryset=Tenant.objects.all(), write_only=True)
    
    # Use for read operations (fetching product details)
    category_detail = CategoriesSerializers(source='category', read_only=True)
    tenant_detail= Tenantserializers(source= 'tenant', read_only= True)

    class Meta:
        model= Products
        fields= '__all__'

    product_id= serializers.CharField(required= True)
    product_name= serializers.CharField(required= True)
    description= serializers.CharField(required= False, allow_blank=True)
    logo= serializers.CharField(required= False)

    def validate(self, data):
        if data['product_id']:
            if Products .objects.filter(product_id= data['product_id']).exists():
                raise serializers.ValidationError(
                    {
                    'message':'Product Id is Already Taken',
                    'success':False,
                    'error': True
                    }
                )
            
        if data['product_name']:
            if Products.objects.filter(product_name= data['product_name']).exists():
                raise serializers.ValidationError(
                    {
                    'message':'Product Name is Already Taken',
                    'success':False,
                    'error': True
                    }
                )
            
        return data
    
# class DaliyProductSerializers(serializers.ModelSerializer):

#     class Meta:
#         model= DailyProduct
#         fields= '__all__'