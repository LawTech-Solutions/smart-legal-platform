import pandas as pd
import os
import PyPDF2
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Contract
import zipfile
from io import BytesIO
from django.http import HttpResponse

# --- 1. دالة استخراج النص من PDF ---
def extract_text_from_pdf(file_path):
    try:
        if not os.path.exists(file_path):
            return "الملف غير موجود"
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = "".join([page.extract_text() for page in reader.pages if page.extract_text()])
            return text if text else "لم يتم العثور على نص مكتوب"
    except Exception as e:
        return f"خطأ في استخراج النص: {str(e)}"


# --- 2. دالة تحليل البيانات الذكي (Pandas) ---
def perform_initial_data_analysis(contract):
    file_path = contract.file.path
    ext = os.path.splitext(file_path)[1].lower()

    try:
        # قراءة الملف بناءً على نوعه
        df = pd.read_csv(file_path) if ext == '.csv' else pd.read_excel(file_path)

        total_rows = len(df)
        missing_values = df.isnull().sum().sum()
        duplicate_rows = df.duplicated().sum()

        # حساب نسبة المخاطرة بناءً على جودة البيانات
        missing_pct = (missing_values / (df.size)) * 100 if df.size > 0 else 0
        risk = int(min(missing_pct + (duplicate_rows / total_rows * 100), 100))

        issues = []
        if missing_values > 0:
            issues.append({
                "title": "بيانات مفقودة (Missing Data)",
                "description": f"يوجد {missing_values} حقل فارغ في الملف المرفوع.",
                "recommendation": "يرجى مراجعة السجلات الناقصة لضمان دقة النتائج القانونية.",
                "severity": "High" if missing_pct > 20 else "Medium"
            })

        if duplicate_rows > 0:
            issues.append({
                "title": "تكرار في السجلات",
                "description": f"تم اكتشاف {duplicate_rows} صف مكرر بالكامل.",
                "recommendation": "قم بتنظيف البيانات من التكرار لتجنب الأخطاء الإحصائية.",
                "severity": "Medium"
            })

        if not issues:
            issues.append({
                "title": "جودة البيانات مثالية",
                "description": "الملف نظيف ولا يحتوي على فجوات بيانات واضحة.",
                "recommendation": "يمكنك الانتقال فوراً لتحليل الأنماط المالية أو القانونية.",
                "severity": "Low"
            })

        return {"risk_score": risk, "report": {"issues": issues}}
    except:
        return None


# --- 3. الدوال الأساسية للمنصة ---

@login_required
def dashboard(request):
    """عرض قائمة الطلبات الخاصة بالمستخدم"""
    contracts = Contract.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'contracts/dashboard.html', {'contracts': contracts})


@login_required
def create_request(request, service):
    """استقبال الطلبات وتجهيز التحليل الفوري"""
    services_map = {
        'analyze': 'تحليل العقود بالذكاء الاصطناعي',
        'generate': 'صياغة العقود القانونية',
        'arbitration': 'التحكيم التجاري',
        'data_analytics': 'تحليل البيانات القانونية'
    }
    service_name = services_map.get(service, 'خدمة قانونية')

    if request.method == 'POST':
        title = request.POST.get('title')
        user_notes = request.POST.get('user_notes', '')
        file = request.FILES.get('file')

        if not file:
            return JsonResponse({'error': 'يرجى رفع الملف المطلوب'}, status=400)

        try:
            # 1. حفظ الطلب في قاعدة البيانات بحالة مدفوع
            contract = Contract.objects.create(
                user=request.user,
                title=title or file.name,
                service_type=service,
                user_notes=user_notes,
                file=file,
                status='paid'
            )

            # 2. منطق التحليل بناءً على نوع الخدمة
            if service == 'analyze':
                extracted = extract_text_from_pdf(contract.file.path)
                contract.risk_score = 45  # قيمة افتراضية للتحليل القانوني حالياً
                contract.analysis_report = {
                    "issues": [
                        {
                            "title": "بند القوة القاهرة",
                            "description": "العقد لا يغطي المخاطر السيبرانية أو الأوبئة.",
                            "recommendation": "إضافة نص يشمل الظروف الطارئة التكنولوجية.",
                            "severity": "High"
                        },
                        {
                            "title": "الاختصاص القضائي",
                            "description": "هناك غموض في تحديد لغة التحكيم.",
                            "recommendation": "تحديد اللغة العربية كصيغة رسمية للتقاضي.",
                            "severity": "Medium"
                        }
                    ]
                }

            elif service == 'data_analytics':
                results = perform_initial_data_analysis(contract)
                if results:
                    contract.risk_score = results['risk_score']
                    contract.analysis_report = results['report']
                else:
                    contract.risk_score = 100
                    contract.analysis_report = {"issues": [
                        {"title": "خطأ في الملف", "description": "الملف تالف أو بصيغة غير مدعومة",
                         "recommendation": "ارفع ملف CSV أو Excel سليم", "severity": "High"}]}

            elif service in ['arbitration', 'generate']:
                contract.risk_score = 10  # مخاطرة منخفضة للطلبات الجديدة
                contract.analysis_report = {
                    "issues": [
                        {"title": "تم استلام الطلب", "description": "طلبك قيد المراجعة من قبل المستشار القانوني.",
                         "recommendation": "يرجى انتظار التحديث خلال 24 ساعة.", "severity": "Low"}]
                }

            contract.save()
            return JsonResponse({'status': 'success', 'id': contract.id})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    from django.conf import settings
    paypal_id = getattr(settings, 'PAYPAL_CLIENT_ID', 'sb')
    return render(request, 'contracts/request_form.html', {'service_name': service_name, 'PAYPAL_CLIENT_ID': paypal_id})


@login_required
def contract_detail(request, pk):
    """عرض تفاصيل العقد والتقرير الملون"""
    contract = get_object_or_404(Contract, pk=pk, user=request.user)
    return render(request, 'contracts/contract_detail.html', {'contract': contract})


@login_required
def delete_contract(request, pk):
    """حذف الطلب"""
    contract = get_object_or_404(Contract, pk=pk, user=request.user)
    if request.method == 'POST':
        contract.delete()
    return redirect('dashboard')


def download_contract_pdf(request, contract_id):
    """فتح نافذة طباعة التقرير"""
    contract = get_object_or_404(Contract, id=contract_id, user=request.user)
    # ملاحظة: سنعتمد حالياً على وظيفة الطباعة من المتصفح لضمان سلامة الخطوط العربية
    return render(request, 'contracts/contract_detail.html', {'contract': contract, 'print_mode': True})

@login_required
def upload_contract(request):
    """إعادة توجيه من الرابط القديم إلى نظام الخدمات الجديد"""
    return redirect('create_request', service='analyze')


@login_required
def download_all_zip(request):
    # جلب جميع عقود المستخدم الحالي فقط
    contracts = Contract.objects.filter(user=request.user)

    if not contracts.exists():
        return HttpResponse("لا توجد ملفات لتحميلها حالياً.")

    # إنشاء ملف ZIP في الذاكرة
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, 'w') as zip_file:
        for contract in contracts:
            if contract.file and os.path.exists(contract.file.path):
                # إضافة الملف إلى الـ ZIP باسمه الأصلي
                zip_file.write(contract.file.path, os.path.basename(contract.file.path))

    # إرسال الملف للمتصفح
    response = HttpResponse(buffer.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="Legal_Archive.zip"'
    return response