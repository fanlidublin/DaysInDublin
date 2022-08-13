# _*_ encoding:utf-8 _*_
"""LfLearning URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
import xadmin
from django.views.static import serve

from users.views import LoginView, LogoutView
from users.views import RegisterView
from users.views import ActiveUserView
from users.views import ForgetPasswordView
from users.views import ResetView
from users.views import ModifyPwdView
from users.views import IndexView

from LfLearning.settings import MEDIA_ROOT

urlpatterns = [
    # 用户
    url(r'^xadmin/', xadmin.site.urls),
    url('^$', IndexView.as_view(), name="index"),
    url('^login/$', LoginView.as_view(), name="login"),
    url('^logout/$', LogoutView.as_view(), name="logout"),
    url('^register/$', RegisterView.as_view(), name="register"),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active"),
    url(r'^forget/$', ForgetPasswordView.as_view(), name="forget_pwd"),
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name="reset_pwd"),
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name="modify_pwd"),
    # 机构url配置
    url(r'^org/', include('organization.urls', namespace="org")),
    # 课程url配置
    url(r'^course/', include('courses.urls', namespace="course")),
    # 上传文件访问（图片）
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    # 用户个人中心
    url(r'^users/', include('users.urls', namespace="users")),
]


