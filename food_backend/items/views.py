from rest_framework.views import APIView
from .serializers import CategoriesSerializers, ProductsSerializers
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from items.models import Categories, Products
# Create your views here.

class CategoriesView(APIView):
    permission_classes= [IsAuthenticated]
    authentication_classes= [JWTAuthentication]

    def get(self, request):
        category_pk= request.data.get('category_pk')
        if category_pk:
            try:
                category = Categories.objects.get(id=category_pk)
                serializer = CategoriesSerializers(category)
                return Response({
                    'data':serializer.data, 
                    'success':True,
                    'error':False}, status= status.HTTP_200_OK)
            
            except Categories.DoesNotExist:
                return Response({
                    "error": "Category not found",
                    'success':False,
                    'error': True
                    }, status=status.HTTP_404_NOT_FOUND)
        else:
            category=Categories.objects.all()
            serializer = CategoriesSerializers(category, many= True)
            return Response({
                    'data':serializer.data,
                    'success':True,
                    'error':False}, status= status.HTTP_200_OK)
        
    def post(self, request):
        serializer= CategoriesSerializers(data= request.data)
        serializer.is_valid(raise_exception=True)

        category_id=serializer.validated_data['category_id']
        description=serializer.validated_data['description']
        category_name=serializer.validated_data['category_name']
        logo= serializer.validated_data['logo']
        tenant= serializer.validated_data['tenant']


        catogory= Categories.objects.create(
            category_id= category_id,
            category_name= category_name,
            description= description,
            logo= logo,
            tenant= tenant
        )

        catogory.save()
        return Response({
            'message': 'Category Created Successfully.',
            'success':True,
            'error': False,
            'data': serializer.data
        }, status= status.HTTP_200_OK)
    
    def put(self, request):
        category_pk= request.data.get('category_pk')
        category_id= request.data.get('category_id')
        category_name= request.data.get('category_name')
        is_avaliable= request.data.get('is_avaliable')
        description= request.data.get('description')
        logo= request.data.get('logo')
        
        category= Categories.objects.get(id= category_pk)
        category.category_id= category_id
        category.category_name= category_name
        category.is_avaliable= is_avaliable
        category.description= description
        category.logo= logo
        category.save()

        serializer= CategoriesSerializers(category)
        return Response({
            'message': 'Category Updated Successfully.',
            'success':True,
            'error': False,
            'data': serializer.data
        }, status= status.HTTP_200_OK)
    
    def delete(self, request):
        category_pk= request.data.get('category_pk')
        if category_pk:
            category= Categories.objects.filter(id= category_pk)
            category.delete()
            return Response({
                'message': 'Category Delete Successfully.',
                'success':True,
                'error': False,
            }, status= status.HTTP_200_OK)
        
        else:
            return Response({
                'message': 'Invalid Category',
                'success':False,
                'error': True,
            }, status= status.HTTP_404_NOT_FOUND)
        
class ProductsView(APIView):
    permission_classes= [IsAuthenticated]
    authentication_classes= [JWTAuthentication]

    def get(self, request):
        product_pk= request.data.get('product_pk')
        if product_pk:
            try:
                productlist = Products.objects.get(id=product_pk)
                
                serializer = ProductsSerializers(productlist)
                return Response({
                    'data':serializer.data,
                    'success':True, 
                    'error':False}, status= status.HTTP_200_OK)
            
            except Products.DoesNotExist:
                return Response({
                    "error": "Product not found",
                    'success':False,
                    'error': True
                    }, status=status.HTTP_404_NOT_FOUND)
        else:
            product=Products.objects.all()
            serializer = ProductsSerializers(product, many= True)
            return Response({
                    'data':serializer.data,
                    'success':True,
                    'error':False}, status= status.HTTP_200_OK)
        

    def post(self, request):
        serializer= ProductsSerializers(data= request.data)
        serializer.is_valid(raise_exception=True)

        product_id= serializer.validated_data['product_id']
        description= serializer.validated_data['description']
        product_name= serializer.validated_data['product_name']
        categories= serializer.validated_data['category']
        tenant= serializer.validated_data['tenant']
        logo= serializer.validated_data['logo']

        product= Products.objects.create(
            product_id= product_id,
            product_name= product_name,
            description= description,
            category= categories,
            tenant= tenant,
            logo= logo
        )

        product.save()
        response_serializer = ProductsSerializers(product)
        return Response({
            'message': 'Product Created Successfully.',
            'success':True,
            'error': False,
            'data': response_serializer.data
        }, status= status.HTTP_200_OK)
    
    def put(self, request):
        product_pk= request.data.get('product_pk')
        product_id= request.data.get('product_id')
        product_name= request.data.get('product_name')
        is_available= request.data.get('is_available')
        description= request.data.get('description')
        logo= request.data.get('logo')
        
        product= Products.objects.get(id= product_pk)
        
        product.product_id= product_id
        product.product_name= product_name
        product.is_available= is_available
        product.description= description
        product.logo= logo
        product.save()

        serializer= ProductsSerializers(product)
        return Response({
            'message': 'Product Updated Successfully.',
            'success':True,
            'error': False,
            'data': serializer.data
        }, status= status.HTTP_200_OK)
    
    def delete(self, request):
        product_pk= request.data.get('product_pk')
        if product_pk:
            products= Products.objects.filter(id= product_pk)
            products.delete()
            return Response({
                'message': 'Product Delete Successfully.',
                'success':True,
                'error': False,
            }, status= status.HTTP_200_OK)
        
        else:
            return Response({
                'message': 'Invalid Products',
                'success':False,
                'error': True,
            }, status= status.HTTP_404_NOT_FOUND)
        
# class ProductDetails(APIView):
#     def get(self, request):
#         category_pk= request.data.get('category_pk')
#         canteen_pk= request.data.get('canteen_pk')

#         if category_pk:
#             try:
#                 products= Products.objects.filter(category= category_pk)
#                 serializer= ProductsSerializers(products)
#                 return Response({
#                     'data':serializer.data,
#                     'success':True, 
#                     'error':False}, status= status.HTTP_200_OK)
            
#             except Products.DoesNotExist:
#                 return Response({
#                     "error": "Category is Empty",
#                     'success':False,
#                     'error': True
#                     }, status=status.HTTP_404_NOT_FOUND)
        
#         elif canteen_pk:
#             try:
#                 products= Products.objects.filter(canteen= canteen_pk)
#                 serializer= ProductsSerializers(products)
#                 return Response({
#                     'data':serializer.data,
#                     'success':True, 
#                     'error':False}, status= status.HTTP_200_OK)
            
#             except Products.DoesNotExist:
#                 return Response({
#                     "error": "Canteen as No Empty",
#                     'success':False,
#                     'error': True
#                     }, status=status.HTTP_404_NOT_FOUND)


# class DaliyProductView(APIView):
#     def post(self, request):
#         project_id= request.data.get('project_id')
#         product_price= request.data.get('product_price')
#         canteen_id= request.data.get('canteen_id')
#         total_quantity= request.data.get('total_quantity')

