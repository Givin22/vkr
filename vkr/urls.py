"""
URL configuration for vkr project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.views.generic.base import TemplateView

from vkr import settings
from django.conf.urls.static import static

from api import class_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include("django.contrib.auth.urls")),
    path('', class_views.Home.as_view(), name="root_home"),
    path('home/', class_views.Home.as_view(), name='home'),
    path('faq/', TemplateView.as_view(template_name="views/faq.html"), name="faq"),
    path('duty_list/', class_views.DutyList.as_view(), name='duty_list'),
    path('residentes/', class_views.ResidentsList.as_view(), name='residents'),
    path('documents', class_views.Documents.as_view(), name="documents"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)