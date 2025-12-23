from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail
from .models import Contract
import stripe

# إعداد مفتاح Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

def create_request(request, service):
    services_map = {
        'analyze': 'تحليل العقود وكشف الثغرات',
        'generate': 'توليد العقود الآمنة',
        'arbitration': 'التحكيم التجاري',
        'pricing': 'طلب تسعير خاص'
    }
    service_name = services_map.get(service, 'خدمة قانونية')

    if request.method == 'POST':
        title = request.POST.get('title')
        user_notes = request.POST.get('user_notes')
        file = request.FILES.get('file')

        if not file:
            return JsonResponse({'error': 'يرجى تحميل ملف العقد أولاً'}, status=400)

        try:
            # حفظ الطلب في قاعدة البيانات
            contract_obj = Contract.objects.create(
                user=request.user,
                title=title,
                service_type=service,
                user_notes=user_notes,
                file=file
            )

            # إنشاء جلسة دفع Stripe
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {'name': f"خدمة: {service_name}"},
                        'unit_amount': 5000, # 50.00 USD
                    },
                    'quantity': 1,
                }],
                mode='payment',
                # تأكد أن هذه الروابط معرفة في urls.py
                success_url=request.build_absolute_uri('/contracts/success/'),
                cancel_url=request.build_absolute_uri('/contracts/cancel/'),
                metadata={'contract_id': contract_obj.id}
            )

            return JsonResponse({'id': checkout_session.id})

        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'error': str(e)}, status=500)

    # --- لاحظ هنا: تم إخراج هذا الجزء ليكون موازياً لـ if request.method ---
    context = {
        'service_name': service_name,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    }
    return render(request, 'contracts/request_form.html', context)