# _*_ encoding:utf-8 _*_
__author__ = 'lifan'
__date__ = '2017/3/24 下午2:29'

from django.conf.urls import url
from .views import UserInfoView, ImageUploadView, UpdatePwdView, MyCourseView
from .views import MyFavOrgView, MyFavTeacherView, MyFavCourseView

urlpatterns = [
    url(r'^info/$', UserInfoView.as_view(), name="user_info"),
    # 头像
    url(r'^image/upload/$', ImageUploadView.as_view(), name="image_upload"),
    url(r'^update/password/$', UpdatePwdView.as_view(), name="update_pwd"),
    url(r'^my_course/$', MyCourseView.as_view(), name="my_course"),
    url(r'^fav_org/$', MyFavOrgView.as_view(), name="fav_org"),
    url(r'^fav_teacher/$', MyFavTeacherView.as_view(), name="fav_teacher"),
    url(r'^fav_course/$', MyFavCourseView.as_view(), name="fav_course"),
]
