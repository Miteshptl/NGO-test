from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('our-work/', views.our_work, name='our_work'),
    path('projects/', views.projects, name='projects'),
    path('media/', views.media, name='media'),
    path('get-involved/', views.get_involved, name='get_involved'),
    path('blog/', views.blog, name='blog'),
    path('contact/', views.contact, name='contact'),
    path('donate/', views.donate, name='donate'),
    path('signin/',views.signin, name='signin'),
    path('signup/',views.signup, name='signup'),
]
