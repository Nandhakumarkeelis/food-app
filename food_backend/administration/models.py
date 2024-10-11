from django.db import models

# Create your models here.
class Tenant(models.Model):
    tenantName= models.CharField(max_length=254, blank=True, null= True)
    shortName= models.CharField(max_length=254, blank=True, null= True)
    logo= models.ImageField(upload_to='image/', blank=True, null=True)
    phoneNumber= models.CharField(max_length=25,blank=True, null=True)
    email=models.EmailField(max_length=254, blank=True, null=True)
    address= models.TextField(blank=True, null=True)
    companyWebsite= models.URLField(blank=True, null=True)

    # Track record of creation and last update
    created_at= models.DateTimeField(auto_now_add=True)
    lastUpdate= models.DateTimeField(auto_now=True)

    class Meta:
        db_table='tenant'

    def __str__(self):
        return f'{self.tenantName}'