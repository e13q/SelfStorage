
from django.urls import path
from .views import index,boxes,rent

app_name = 'app'
urlpatterns = [
    path('', index, name='index' ),
    path('boxes/',boxes,name='boxes'),
    path('rent/',rent,name='rent')

]