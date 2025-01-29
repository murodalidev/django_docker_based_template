from django.urls import path

from apps.users.api.v1.views import users

app_name = "v1"

urlpatterns = [
    path('hi/', users.hi)
]

