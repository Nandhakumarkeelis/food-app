from django.urls import path
from .views import CategoriesView, ProductsView

urlpatterns = [
    path('categories/', CategoriesView.as_view(), name='category'),
    path('products/', ProductsView.as_view(), name='products'),
]
