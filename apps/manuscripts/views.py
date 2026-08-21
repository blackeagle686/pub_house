from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Manuscript
from .forms import ManuscriptForm

class SubmitManuscriptView(CreateView):
    model = Manuscript
    form_class = ManuscriptForm
    template_name = 'manuscripts/submit.html'
    success_url = reverse_lazy('manuscripts:submit_success')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Trigger Celery Task in the background
        from .tasks import send_manuscript_confirmation_email
        send_manuscript_confirmation_email.delay(self.object.id)
        
        messages.success(self.request, "تم استلام المخطوطة بنجاح وسيتم إرسال بريد إلكتروني لك قريباً.")
        return response
    
class SubmitSuccessView(CreateView):
    template_name = 'manuscripts/success.html'
    # Fallback to TemplateView logic
    def get(self, request, *args, **kwargs):
        from django.shortcuts import render
        return render(request, self.template_name)
