"""visualanalyticsplatform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include, re_path

from core import views as core_views


urlpatterns = [ 
    path('admin/', admin.site.urls),
    path('', core_views.main, name='main'),
    path('v/', core_views.visualization_init, name='regular_visualization_init'),
    re_path('^v/(?P<maindatasetuid>[0-9]+.?[0-9]*)/(?P<groups>(g/[0-9]+/)*)(o/(?P<operationnumber>[0-9]+)/)?$', core_views.visualization_data, name='regular_visualization_data'),
    re_path('^v/(?P<maindatasetuid>[0-9]+.?[0-9]*)/(?P<groups>(g/[0-9]+/)*)o/(?P<operationnumber>[0-9]+)/$', core_views.visualization_data, name='regular_visualization_data_operation'),
    re_path('^v/(?P<maindatasetuid>[0-9]+.?[0-9]*)/(?P<groups>(g/[0-9]+/)*)g/NEWGROUPID/$', core_views.visualization_data, name='regular_visualization_data_new_group'),
    path('site2site', core_views.site_to_site, name='site_to_site'),
    path('test', core_views.performance_test, name='performance_test'),
    path('testframe', core_views.performance_test_frame, name='performance_test_frame'),
    path('testmodule/', include('core.testmodule.urls'))
]
