from django.urls import path
from . import views

urlpatterns = [
    # 1. الصفحة الرئيسية ولوحة التحكم
    path('', views.dashboard, name='dashboard'),

    # 2. نظام طلب الخدمات الموحد (تحليل، صياغة، تحكيم، بيانات)
    path('request/<str:service>/', views.create_request, name='create_request'),

    # 3. عرض تفاصيل الطلب والتقرير القانوني
    path('contract/<int:pk>/', views.contract_detail, name='contract_detail'),

    # 4. ميزة تحميل أرشيف الملفات (ZIP) الجديدة
    path('download-archive/', views.download_all_zip, name='download_all_zip'),

    # 5. رابط تحميل الـ PDF أو الملف الأصلي
    path('contract/<int:contract_id>/pdf/', views.download_contract_pdf, name='contract_pdf'),

    # 6. حذف الطلب
    path('contract/<int:pk>/delete/', views.delete_contract, name='delete_contract'),

    # 7. رابط الرفع القديم (للتوافق ولتجنب الأخطاء)
    path('upload/', views.upload_contract, name='upload_contract'),
    ]