"""Store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from products.views import ProductView, ProductDetailView,CategoriesView,CreateProductView,MainView
from Store.settings import MEDIA_ROOT,MEDIA_URL
from django.conf.urls.static import static
from users.views import LoginView,LogoutView,RegisterView




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view(template_name=' layouts/index.html')),
    path('products/', ProductView.as_view(template_name='products/products.html')),
    path('products/<int:id>/', ProductDetailView.as_view(template_name='products/detail.html')),
    path('categories/', CategoriesView.as_view(template_name='categories/category.html')),
    path('products/create/', CreateProductView.as_view(template_name='products/create.html')),
    #users
    path('users/login/', LoginView.as_view(template_name='users/login.html')),
    path('users/logout/',LogoutView.as_view()),
    path('users/register/', RegisterView.as_view(template_name='users/register.html'))

]


urlpatterns+=static(MEDIA_URL,document_root=MEDIA_ROOT)