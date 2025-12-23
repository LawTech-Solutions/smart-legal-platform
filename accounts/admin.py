from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # الأعمدة التي ستظهر في الجدول الرئيسي
    list_display = ['user', 'display_name', 'get_updates', 'get_advice']
    # إمكانية البحث بالاسم أو اسم المستخدم
    search_fields = ['user__username', 'display_name']