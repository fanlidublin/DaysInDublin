# _*_ encoding:utf-8 _*_
import xadmin
from xadmin import views
from xadmin.plugins.auth import UserAdmin
from .models import EmailVerifyRecord, Banner, UserProfile

__author__ = 'lifan'
__date__ = '2017/2/27 下午7:17'


class UserProfileAdmin(UserAdmin):
    pass


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSeeting(object):
    site_title = "LF-Learning后台管理"
    site_footer = "设计: Fan Li"
    menu_style = "accordion"


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


# from django.contrib.auth.models import User
# xadmin.site.unregister(User)
# xadmin.site.register(UserProfile, UserProfileAdmin)
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSeeting)
