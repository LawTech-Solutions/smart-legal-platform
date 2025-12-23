from django.db import models
from django.contrib.auth.models import User

class Contract(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="المحامي/المستخدم")
    title = models.CharField(max_length=255, verbose_name="عنوان العقد")
    file = models.FileField(upload_to='contracts/', verbose_name="ملف العقد")
    extracted_text = models.TextField(blank=True, null=True, verbose_name="النص المستخرج")
    user_notes = models.TextField(blank=True, null=True, verbose_name="ملاحظات المستخدم")
    analysis_report = models.TextField(blank=True, null=True, verbose_name="تقرير التحليل")
    risk_score = models.IntegerField(default=0, verbose_name="مؤشر المخاطرة")
    safe_version_text = models.TextField(blank=True, null=True, verbose_name="الصياغة الآمنة")
    is_paid = models.BooleanField(default=False, verbose_name="تم الدفع")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title