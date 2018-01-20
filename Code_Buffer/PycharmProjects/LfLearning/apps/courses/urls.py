# _*_ encoding:utf-8 _*_
__author__ = 'lifan'
__date__ = '2017/3/19 下午1:28'

from django.conf.urls import url
from .views import CourseListView, CourseDetailView, CourseChapterView, CourseCommentView, AddCommentView,ViewPlayView

urlpatterns = [
    url(r'^list/$', CourseListView.as_view(), name="course_list"),
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="course_detail"),
    url(r'^chapter/(?P<course_id>\d+)/$', CourseChapterView.as_view(), name="course_info"),
    url(r'^comment/(?P<course_id>\d+)/$', CourseCommentView.as_view(), name="course_comment"),
    url(r'^add_comment/$', AddCommentView.as_view(), name="add_comment"),
    url(r'^video_play/(?P<video_id>\d+)/$', ViewPlayView.as_view(), name="video_play"),
]
