from django.contrib import admin
from .models import Contract


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    # الحقول التي تظهر في الجدول الرئيسي للأدمن
    list_display = ('title', 'user', 'service_type', 'status', 'risk_score', 'created_at')

    # الفلاتر الجانبية
    list_filter = ('service_type', 'status', 'created_at')

    # البحث
    search_fields = ('title', 'user__username')

    # ترتيب الحقول داخل صفحة تعديل العقد
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('معلومات العميل والعقد', {
            'fields': ('user', 'title', 'service_type', 'file', 'user_notes')
        }),
        ('نتائج التحليل الذكي', {
            'fields': ('status', 'risk_score', 'analysis_report')
        }),
        ('التوقيت', {
            'fields': ('created_at', 'updated_at'),
        }),
    )

    # تخصيص عرض الـ JSON بشكل أوضح في الأدمن (اختياري)
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form