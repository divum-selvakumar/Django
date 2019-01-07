from django.conf.urls import url
from django.contrib import admin

from CRUD_OPERATIONS import views

urlpatterns = [
    url(r'^user?(?:/(?P<pk>.*))?', views.user, name='CRUD url with pk'),
    url(r'^admin/', admin.site.urls),
]
