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

from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token

from ZoomInDev.settings import MEDIA_ROOT
from django.views.static import serve

from users.views import UserViewset
from tasks.views import TaskViewset, DataSetViewset, ChartViewset, DelValue
from data_mining.views import RegressionViewSet, ClusteringViewSet
from user_operation.views import UserTaskViewset, PublishViewset, publish
from tasks import urls as tasks
from user_operation import urls as user_operation

router = DefaultRouter()

router.register(r'users', UserViewset, base_name="users")
router.register(r'usertask', UserTaskViewset, base_name="usertask")
router.register(r'taskinfo', TaskViewset, base_name="task")
# router.register(r'publish', publish, base_name="publish")
router.register(r'dataSet', DataSetViewset, base_name="dataSet")
router.register(r'chart', ChartViewset, base_name="chart")
router.register(r'dataMining/regression', RegressionViewSet, base_name="regression")
router.register(r'dataMining/clustering', ClusteringViewSet, base_name="clustering")
router.register(r'shared', PublishViewset, base_name="shared")



urlpatterns = [
    url(r'^home/ZoomInDataSet/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    url(r'^publish/', publish, name="publish"),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^task/', include(tasks)),
    url(r'^user_operation/', include(user_operation)),
    url(r'^', include(router.urls)),

    # 这里有坑，$符号不能出现
    url(r'docs/', include_docs_urls(title="ZoomIn文档系统")),


    # drf自带的token认证模式
    url(r'^api-token-auth/', views.obtain_auth_token),

    # jwt的认证接口
    url(r'^login/', obtain_jwt_token),

    # 数据处理API_views
    url(r'^task/dataProcessing/drop/', DelValue.as_view(), name="drop"),

    # 数据挖掘API_views



]
