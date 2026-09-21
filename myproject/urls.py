from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from invoices import views

urlpatterns = [

    path('admin/', admin.site.urls),

    path('', views.home, name='home'),

    path('register/', views.register, name='register'),

    path('job/<int:id>/', views.job_detail, name='job_detail'),

    path('job/<int:id>/apply/', views.apply_job, name='apply_job'),

    path(
        'application-success/<int:id>/',
        views.application_success,
        name='application_success'
    ),

    path('login/', views.user_login, name='login'),

    path('logout/', views.user_logout, name='logout'),

    path('jobs/', views.jobs, name='jobs'),

    path('companies/', views.companies, name='companies'),

    path('about/', views.about, name='about'),

  
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)