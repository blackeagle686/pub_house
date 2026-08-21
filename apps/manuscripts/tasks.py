from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Manuscript

@shared_task
def send_manuscript_confirmation_email(manuscript_id):
    try:
        manuscript = Manuscript.objects.get(id=manuscript_id)
        
        subject = f"تأكيد استلام مخطوطتك: {manuscript.title}"
        message = f"""
مرحباً {manuscript.author_name}،

لقد استلمنا مخطوطتك بنجاح!
رقم التتبع: {manuscript.tracking_number}
العنوان: {manuscript.title}

سيقوم فريق التقييم لدينا بمراجعتها والتواصل معك في أقرب وقت.

شكراً لاختيارك دار الأديب.
        """
        
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [manuscript.email],
            fail_silently=False,
        )
        return f"Email sent successfully for Manuscript {manuscript_id}"
    except Manuscript.DoesNotExist:
        return f"Manuscript {manuscript_id} not found."
    except Exception as e:
        return f"Error sending email: {str(e)}"
