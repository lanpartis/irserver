from django.conf.urls import url

from views import show_lib

urlpatterns = [
    url(r'', show_lib),  
]
