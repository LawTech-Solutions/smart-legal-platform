import pdfplumber
from docx import Document
import random

def extract_text_from_file(file_path):
    """استخراج النص باستخدام pdfplumber (أكثر استقراراً على ويندوز)"""
    ext = file_path.split('.')[-1].lower()
    text = ""
    try:
        if ext == 'pdf':
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    content = page.extract_text()
                    if content:
                        text += content + "\n"
        elif ext in ['docx', 'doc']:
            doc = Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        print(f"Error reading file: {e}")
        return "فشل استخراج النص من الملف."

def analyze_contract_logic(text, user_notes=""):
    """محرك المحاكاة للنتائج"""
    possible_issues = [
        {'title': 'غموض في بند التعويضات', 'description': 'لم يتم تحديد سقف أقصى للمسؤولية المالية في حالة الإخلال.', 'level': 'high'},
        {'title': 'شرط جزائي مبالغ فيه', 'description': 'قيمة الشرط الجزائي تتجاوز 50% من قيمة العقد، مما قد يجعله باطلاً قانونياً.', 'level': 'high'},
        {'title': 'الاختصاص القضائي', 'description': 'لم يتم تحديد مدينة التقاضي، يفضل تحديد المحاكم التجارية بالرياض.', 'level': 'medium'},
        {'title': 'فترة الإشعار بالإنهاء', 'description': 'فترة 15 يوماً قصيرة جداً لإنهاء عقد توريد خدمات برمجية.', 'level': 'medium'},
        {'title': 'الملكية الفكرية', 'description': 'بند الملكية الفكرية يحمي حقوق المبرمج بشكل ممتاز.', 'level': 'safe'},
        {'title': 'سرية المعلومات', 'description': 'تمت صياغة بند عدم الإفصاح (NDA) باحترافية عالية.', 'level': 'safe'},
    ]

    selected_issues = random.sample(possible_issues, k=random.randint(3, 5))
    high_count = len([i for i in selected_issues if i['level'] == 'high'])
    risk_score = 30 + (high_count * 20) + random.randint(0, 10)

    return {
        'risk_score': min(risk_score, 100),
        'summary': "تم تحليل العقد بنجاح. يرجى مراجعة النقاط الملونة بالأحمر للأهمية.",
        'issues': selected_issues
    }