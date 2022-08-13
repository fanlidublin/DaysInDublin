# _*_ encoding:utf-8 _*_
__author__ = 'lifan'
__date__ = '2017/3/13 下午8:55'

from django.conf.urls import url
from organization.views import OrgView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView
from organization.views import AddFavView
from organization.views import TeacherListView, TeacherDetailView

urlpatterns = [
    # 所有机构
    url(r'^list/$', OrgView.as_view(), name="org_list"),
    # 机构模块
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name="org_home"),
    url(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name="org_course"),
    url(r'^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name="org_desc"),
    url(r'^org_teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name="org_teacher"),
    # 收藏功能
    url(r'^org_fav/$', AddFavView.as_view(), name="add_fav"),
    # 教师相关模块
    url(r'^teacher/list/$', TeacherListView.as_view(), name="teacher_list"),
    url(r'^teacher/detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name="teacher_detail"),
]
