from django.db import models
from administration.models import Tenant

# Create your models here.
# Admin Table to store admin details
class AdminDetails(models.Model):
    username= models.CharField(max_length=254, unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=254, blank=True, null=True)
    last_name = models.CharField(max_length=254, blank=True, null=True)
    password= models.CharField(max_length=254, blank=True, null=True)
    contact_number= models.CharField(max_length=15, blank=True, null=True)
    email= models.EmailField(unique=True, blank=True, null=True)
    logo= models.ImageField(upload_to='image/', blank=True, null=True)

    # Tenant details
    tenant= models.ForeignKey(Tenant, on_delete= models.SET_NULL, null= True, blank=True)

    # Track record of creation and last update
    created_at= models.DateTimeField(auto_now_add=True)
    lastUpdate= models.DateTimeField(auto_now=True)

    class Meta:
        db_table= 'admin_details'

    def __str__(self):
        return f'{self.username}'

# Student table to store Student details
class StudentDetails(models.Model):
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email= models.EmailField(unique=True, blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    student_id= models.CharField(unique=True, max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    password= models.CharField(max_length=254, blank=True, null=True)
    is_active=models.BooleanField(default=False)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    logo= models.ImageField(upload_to='image/', blank=True, null=True)

    # Tenant details
    tenant= models.ForeignKey(Tenant, on_delete= models.SET_NULL, null= True, blank=True)

    # Track record of creation and last update
    created_at= models.DateTimeField(auto_now_add=True)
    lastUpdate= models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.student_id} {self.is_active}"

    class Meta:
        db_table= 'student_details'

# Canteen table to store canteen details
class CanteenDetails(models.Model):
    canteen_id= models.CharField(max_length=50, blank=True, null=True)
    canteen_name= models.CharField(max_length=150, blank=True, null=True)
    opening_time= models.DateTimeField(blank=True, null=True)
    closing_time= models.DateTimeField(blank=True, null=True)
    is_available= models.BooleanField(default=True)
    is_active= models.BooleanField(blank=True, null=True, default=True)
    logo= models.ImageField(upload_to='image/', blank=True, null=True)

    
    # Tenant details
    tenant= models.ForeignKey(Tenant, on_delete= models.SET_NULL, null= True, blank=True)

    # Track record of creation and last update
    created_at= models.DateTimeField(auto_now_add=True)
    lastUpdate= models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.canteen_name} - {self.canteen_id}"

    class Meta:
        db_table= 'canteen_details'

# to Store Canteen workers details
class canteenWorkers(models.Model):
    canteen= models.ForeignKey(CanteenDetails, on_delete=models.SET_NULL, null= True)
    staff_id= models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email= models.EmailField( blank=True, null=True)
    password= models.CharField(max_length=100, blank=True, null=True)
    contact_number= models.CharField(max_length=100, blank=True, null=True)
    is_available= models.BooleanField(default=True)
    is_active= models.BooleanField(default=True)
    logo= models.ImageField(upload_to='image/', blank=True, null=True)


    # Tenant details
    tenant= models.ForeignKey(Tenant, on_delete= models.SET_NULL, null= True, blank=True)

    # Track record of creation and last update
    created_at= models.DateTimeField(auto_now_add=True)
    lastUpdate= models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.email} - {self.canteen}"

    class Meta:
        db_table= 'canteenWorker_details'