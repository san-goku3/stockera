from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('sign_in/', views.sign_in, name='sign_in'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('create_account/', views.create_account, name='create_account'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('get_ipo_data/<int:ipo_id>/', views.get_ipo_data, name='get_ipo_data'),
    path('delete-ipo/<int:ipo_id>/', views.delete_ipo, name='delete_ipo'),
    #path('register-ipo/', register_ipo, name='register_ipo'),
]