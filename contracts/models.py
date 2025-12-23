from django.db import models
from django.contrib.auth.models import User


class Contract(models.Model):
    SERVICE_CHOICES = [
        ('analyze', 'تحليل العقود (AI)'),
        ('generate', 'صياغة العقود'),
        ('arbitration', 'التحكيم التجاري'),
        ('data_analytics', 'تحليل البيانات'),
    ]

    STATUS_CHOICES = [
        ('pending', 'قيد الانتظار'),
        ('paid', 'تم الدفع / جاري المعالجة'),
        ('completed', 'تم الانتهاء'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name="عنوان العقد")
    service_type = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    file = models.FileField(upload_to='contracts/originals/')
    user_notes = models.TextField(blank=True, null=True, verbose_name="ملاحظات العميل")

    # --- الحقول الجديدة لدعم التصميم الاحترافي ---
    risk_score = models.IntegerField(default=0, verbose_name="مؤشر المخاطرة")
    # نستخدم JSONField لتخزين الثغرات والتوصيات بشكل منظم
    analysis_report = models.JSONField(default=dict, blank=True, null=True, verbose_name="تقرير التحليل المفصل")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title