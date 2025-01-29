from django.urls import path, include

app_name = 'users'

urlpatterns = [
    path('api/', include('apps.users.api.urls', namespace='api')),
]
