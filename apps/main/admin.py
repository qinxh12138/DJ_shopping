from django.contrib import admin

# Register your models here.
import xadmin

# 全局配置
from xadmin import views
# 开启主题修改
from apps.main.models import *


class BaseStyleSettings:
    enable_themes = True
    use_bootswatch = True


xadmin.site.register(views.BaseAdminView, BaseStyleSettings)


class GlobalSettings:
    site_title = '天猫后台管理系统'
    site_footer = '千锋互联科技有限公司'
    menu_style = 'accordion'  # 后台菜单样式修改


xadmin.site.register(views.CommAdminView, GlobalSettings)


class NavigationAdmin:
    # 后台界面要显示的字段
    list_display = ['nav_id', 'nav_name']
    # 搜索
    search_fields = ['nav_name']
    # 分页显示的条数
    list_per_page = 10


xadmin.site.register(Navigation, NavigationAdmin)


class ShopAdmin:
    # 默认情况下显示object对象
    list_display = ['shop_id', 'name', 'sub_title', 'create_date']
    # 修改分页的默认的条数
    list_per_page = 10
    # 搜索字段
    search_fields = ['name', 'sub_title']
    list_editor = []


xadmin.site.register(Shop, ShopAdmin)

# 自定义的admin
from xadmin.plugins import auth


# 显示自定义的方式
class UserAdmin(auth.UserAdmin):
    list_display = ['id', 'username', 'email', 'img_show']


# 先注销
xadmin.site.unregister(User)
# 在注册
xadmin.site.register(User, UserAdmin)


class PropertyValueAdmin:
    # 默认情况下显示object对象
    list_display = ['pro_value_id', 'shop', 'property', 'value']
    # 修改分页的默认的条数
    list_per_page = 10
    # 搜索字段
    search_fields = ['shop', 'value']
    list_editor = []


xadmin.site.register(PropertyValue, PropertyValueAdmin)
