"""ZoomInDev URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import include
from django.conf.urls import url

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token

from ZoomInDev.settings import MEDIA_ROOT
from django.views.static import serve

from users.views import UserViewset
from user_operation.views import UserTaskViewset
from tasks import urls as tasks

router = DefaultRouter()

router.register(r'users', UserViewset, base_name="users")
router.register(r'usertask', UserTaskViewset, base_name="usertask")

urlpatterns = [
    url(r'^upload/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^task', include(tasks)),

    url(r'^', include(router.urls)),

#drf自带的token认证模式
    url(r'^api-token-auth/', views.obtain_auth_token),

    #jwt的认证接口
    url(r'^login/', obtain_jwt_token),

]
