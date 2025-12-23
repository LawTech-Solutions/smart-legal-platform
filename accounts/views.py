import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Contract
from .services import extract_text_from_file, analyze_contract_logic


@login_required
def dashboard(request):
    """لوحة التحكم: عرض العقود والمستندات الخاصة بالشركة/المستقل"""
    contracts = Contract.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'contracts/dashboard.html', {'contracts': contracts})


@login_required
def upload_contract(request):
    """معالجة رفع الملفات (سواء عبر النموذج التقليدي أو السحب والإفلات)"""
    if request.method == 'POST':
        # استقبال الملف والبيانات
        file = request.FILES.get('file')
        title = request.POST.get('title') or (file.name if file else "عقد غير مسمى")

        contract = Contract.objects.create(
            user=request.user,
            title=title,
            original_file=file,
            order_notes=request.POST.get('notes', ''),
            status='processing'
        )

        # 1. استخراج النص فوراً
        if contract.original_file:
            try:
                contract.extracted_text = extract_text_from_file(contract.original_file.path)
                contract.save()
            except Exception as e:
                print(f"Extraction Error: {e}")

        # التوجه للدفع (أو التحليل مباشرة إذا كانت الخدمة مجانية للشركات الناشئة)
        return redirect('payment_success', pk=contract.pk)

    return render(request, 'contracts/upload.html')


@login_required
def payment_success(request, pk):
    """محرك التحليل: يتم استدعاؤه بعد التأكد من الدفع"""
    contract = get_object_or_404(Contract, pk=pk, user=request.user)
    contract.is_paid = True
    contract.status = 'analyzing'
    contract.save()

    try:
        # 2. استدعاء ذكاء "عقدك" الاصطناعي
        # نتوقع أن تعيد هذه الدالة قاموساً يحتوي على (risk_score, issues, summary)
        analysis_data = analyze_contract_logic(contract.extracted_text, contract.order_notes)

        # 3. تخزين النتائج في الحقول المخصصة
        contract.analysis_report = analysis_data  # JSONField
        contract.risk_score = analysis_data.get('risk_score', 0)
        contract.status = 'completed'
        contract.save()
    except Exception as e:
        contract.status = 'error'
        contract.save()
        print(f"AI Analysis Error: {e}")

    # التوجه لصفحة الرادار (النتائج)
    return redirect('contract_detail', pk=contract.pk)


@login_required
def contract_detail(request, pk):
    """رادار النتائج: الصفحة التي تعرض الثغرات والتحليل النهائي للعميل"""
    contract = get_object_or_404(Contract, pk=pk, user=request.user)

    # استخراج التصنيفات من التقرير لتسهيل عرضها في القالب
    report = contract.analysis_report or {}
    issues = report.get('issues', [])

    # تقسيم المشاكل حسب الخطورة لسهولة العرض في الـ Template
    context = {
        'contract': contract,
        'risk_score': contract.risk_score,
        'summary': report.get('summary', 'لا يوجد ملخص متاح حالياً.'),
        'high_risks': [i for i in issues if i.get('level') == 'high'],
        'medium_risks': [i for i in issues if i.get('level') == 'medium'],
        'safe_points': [i for i in issues if i.get('level') == 'safe'],
        'total_findings': len(issues),
    }

    return render(request, 'contracts/detail.html', context)