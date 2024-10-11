from django.db import models
from administration.models import Tenant

# Create your models here.
# categories is used to store category details
class Categories(models.Model):
    category_id= models.CharField(max_length=50, blank=True, null= True)
    category_name= models.CharField(max_length=254, blank=True, null= True)
    is_avaliable= models.BooleanField(default=True)
    description= models.TextField(blank=True, null= True)
    logo= models.ImageField(upload_to='image/', blank=True, null=True)

    # Tenant details
    tenant= models.ForeignKey(Tenant, on_delete= models.SET_NULL, null= True, blank=True)

    # Track record of creation and last update
    created_at= models.DateTimeField(auto_now_add=True)
    lastUpdate= models.DateTimeField(auto_now=True)

    class Meta:
        db_table= 'categories'

    def __str__(self):
        return f'{self.category_id} - {self.category_name}'

class Products(models.Model):
    product_id= models.CharField(max_length=50, null=True, blank=True)
    product_name= models.CharField(max_length=254, null=True, blank=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    is_available= models.BooleanField(default=True)
    description= models.TextField(blank=True, null= True)
    logo= models.ImageField(upload_to='image/', blank=True, null=True)

    # Tenant details
    tenant= models.ForeignKey(Tenant, on_delete= models.SET_NULL, null= True, blank=True)

    # Track record of creation and last update
    created_at= models.DateTimeField(auto_now_add=True)
    lastUpdate= models.DateTimeField(auto_now=True)

    class Meta:
        db_table= 'products'

    def __str__(self):
        return f'{self.product_id} - {self.product_name}'

# class DailyProduct(models.Model):
#     product= models.ForeignKey(Products, on_delete=models.SET_NULL, null= True)
#     category = models.ForeignKey(Categories, on_delete=models.CASCADE)
#     product_price= models.CharField(max_length= 254, blank=True, null=True)
#     canteen_id= models.CharField(max_length= 50, blank=True, null=True)
#     total_quantity= models.CharField(max_length= 10, blank=True, null=True)

#     # Tenant details
#     tenant= models.ForeignKey(Tenant, on_delete= models.SET_NULL, null= True, blank=True)

#     # Track record of creation and last update
#     created_at= models.DateTimeField(auto_now_add=True)
#     lastUpdate= models.DateTimeField(auto_now=True)

#     class Meta:
#         db_table= 'daily_products'

#     def __str__(self):
#         return f'{self.product} - {self.product_price} - {self.total_quantity} form {self.category}'