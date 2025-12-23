from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# تخصيص مظهر لوحة الإدارة (Admin Interface)
admin.site.site_header = "منصة عـقـدك - الإدارة"
admin.site.site_title = "لوحة تحكم المحامي الذكي"
admin.site.index_title = "مرحباً بك في وحدة تحكم المنصة القانونية"

urlpatterns = [
    # 1. لوحة الإدارة الرئيسية
    path('admin/', admin.site.urls),

    # 2. روابط تطبيق العقود والخدمات القانونية
    path('', include('contracts.urls')),

    # 3. روابط نظام تسجيل الدخول والحسابات
    path('accounts/', include('django.contrib.auth.urls')),

    # تم حذف سطر الـ PDF من هنا لأنه يجب أن يكون داخل contracts/urls.py
]

# تفعيل عرض الملفات المرفوعة أثناء التطوير
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)