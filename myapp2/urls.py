from django.urls import path
from . import views

app_name = 'myapp2'
urlpatterns = [
	path('', views.index, name='index'),
	path('ajax_post/', views.ajax_post, name='ajax_post'),
	path('ajax_datatable/', views.ajax_datatable, name='ajax_datatable'),
]
