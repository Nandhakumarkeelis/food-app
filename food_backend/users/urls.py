from django.urls import path
from users.views import (AdminRegisterView, AdminLoginView, 
                         StudentRegisterView, StudentLoginView, StudentSetPasswordView,
                         CanteenRegisterView, CanteenWorkersView, CanteenWorkerLoginView, staffSetPasswordView)

urlpatterns = [
    path('admin-register/',AdminRegisterView.as_view(), name="admin-register"),
    path('admin-login/',AdminLoginView.as_view(), name='admin-login'),
    path('student-register/',StudentRegisterView.as_view(), name="student-register"),
    path('student-login/',StudentLoginView.as_view(), name="student-login"),
    path('student-setpassword/',StudentSetPasswordView.as_view(), name="student-setpassword"),
    path('canteen-register/',CanteenRegisterView.as_view(), name="canteen-register"),
    path('canteenworker-register/',CanteenWorkersView.as_view(), name="canteenworker-register"),
    path('canteenworker-login/',CanteenWorkerLoginView.as_view(), name="canteenworker-login"),
    path('canteenworker-setpasswordlogin/',staffSetPasswordView.as_view(), name="canteenworker-setpasswordlogin"),

]
