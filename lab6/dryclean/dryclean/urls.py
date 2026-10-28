from django.contrib import admin
from django.urls import path
from orders import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.archive, name='archive'),
    path('contract/new/', views.create_contract, name='create_contract'),
    path('contract/<int:contract_id>/', views.get_contract, name='get_contract'),
    path('branch/<int:branch_id>/', views.branch_stats, name='branch_stats'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
