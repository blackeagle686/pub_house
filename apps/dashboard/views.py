from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.db.models import Q
from apps.books.models import Book
from apps.orders.models import Order
from apps.authors.models import Author
from apps.manuscripts.models import Manuscript
from apps.core.models import Report
from django.db.models import Sum, Count, Q
import json
from django.contrib.messages.views import SuccessMessageMixin

class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = '/dashboard/login/'
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

class DashboardLoginView(LoginView):
    template_name = 'dashboard/auth/login.html'
    redirect_authenticated_user = True
    def get_success_url(self):
        return '/dashboard/'

class DashboardHomeView(AdminRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # General Counts
        context['total_books'] = Book.objects.count()
        context['total_orders'] = Order.objects.count()
        context['total_authors'] = Author.objects.count()
        context['total_users'] = User.objects.count()
        context['total_manuscripts'] = Manuscript.objects.count()
        context['total_reports'] = Report.objects.count()
        
        # Revenue and Financials
        completed_orders = Order.objects.filter(status='completed')
        total_revenue = completed_orders.aggregate(Sum('total_price'))['total_price__sum'] or 0
        context['total_revenue'] = total_revenue
        
        # Orders By Status (for Pie Chart)
        orders_by_status = list(Order.objects.values('status').annotate(count=Count('id')))
        status_labels = [dict(Order.STATUS_CHOICES).get(item['status'], item['status']) for item in orders_by_status]
        status_data = [item['count'] for item in orders_by_status]
        context['orders_status_labels'] = json.dumps(status_labels)
        context['orders_status_data'] = json.dumps(status_data)
        
        # Latest Orders
        context['recent_orders'] = Order.objects.order_by('-created_at')[:5]
        
        # Out of stock books
        context['out_of_stock_books'] = Book.objects.filter(stock=0).count()
        
        return context

class DashboardGlobalSearchView(AdminRequiredMixin, TemplateView):
    template_name = 'dashboard/search_results.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get('q', '').strip()
        context['q'] = q
        
        if not q:
            return context
            
        results = {}
        
        # Books
        book_qs = Book.objects.filter(Q(title__icontains=q) | Q(author__name__icontains=q) | Q(isbn__icontains=q))
        if q.isdigit():
            book_qs = book_qs | Book.objects.filter(id=q)
        results['books'] = book_qs.select_related('author').distinct()[:10]
        
        # Authors
        author_qs = Author.objects.filter(name__icontains=q)
        if q.isdigit():
            author_qs = author_qs | Author.objects.filter(id=q)
        results['authors'] = author_qs.distinct()[:10]
        
        # Users
        user_qs = User.objects.filter(Q(username__icontains=q) | Q(email__icontains=q) | Q(first_name__icontains=q) | Q(last_name__icontains=q))
        if q.isdigit():
            user_qs = user_qs | User.objects.filter(id=q)
        results['users'] = user_qs.distinct()[:10]
        
        # Orders
        order_qs = Order.objects.filter(user__username__icontains=q)
        if q.isdigit():
            order_qs = order_qs | Order.objects.filter(id=q)
        results['orders'] = order_qs.distinct()[:10]
        
        # Manuscripts (New books needing review)
        manuscript_qs = Manuscript.objects.filter(Q(title__icontains=q) | Q(author_name__icontains=q))
        if q.isdigit():
            manuscript_qs = manuscript_qs | Manuscript.objects.filter(id=q)
        results['manuscripts'] = manuscript_qs.distinct()[:10]
        
        # Reports
        report_qs = Report.objects.filter(Q(description__icontains=q) | Q(reason__icontains=q) | Q(reporter__username__icontains=q))
        if q.isdigit():
            report_qs = report_qs | Report.objects.filter(id=q)
        results['reports'] = report_qs.distinct()[:10]
        
        context['results'] = results
        # Check if any list has items
        context['has_results'] = any(len(qs) > 0 for qs in results.values())
        return context

# --- Books CRUD ---
class DashboardBooksView(AdminRequiredMixin, ListView):
    model = Book
    template_name = 'dashboard/books/list.html'
    context_object_name = 'books'
    paginate_by = 10
    
    def get_queryset(self):
        qs = super().get_queryset().select_related('author', 'category')
        q = self.request.GET.get('q')
        if q:
            if q.isdigit():
                qs = qs.filter(Q(id=q) | Q(title__icontains=q) | Q(author__name__icontains=q))
            else:
                qs = qs.filter(Q(title__icontains=q) | Q(author__name__icontains=q))
        return qs

class DashboardBookCreateView(AdminRequiredMixin, SuccessMessageMixin, CreateView):
    model = Book
    template_name = 'dashboard/shared/form.html'
    fields = ['title', 'slug', 'author', 'category', 'description', 'cover', 'isbn', 'publication_year', 'pages', 'language', 'paperback_price', 'ebook_price', 'stock', 'is_published', 'is_featured', 'featured_order']
    success_url = reverse_lazy('dashboard:books')
    success_message = "تم إضافة الكتاب بنجاح"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "إضافة كتاب جديد"
        return context

class DashboardBookUpdateView(AdminRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Book
    template_name = 'dashboard/shared/form.html'
    fields = ['title', 'slug', 'author', 'category', 'description', 'cover', 'isbn', 'publication_year', 'pages', 'language', 'paperback_price', 'ebook_price', 'stock', 'is_published', 'is_featured', 'featured_order']
    success_url = reverse_lazy('dashboard:books')
    success_message = "تم تعديل الكتاب بنجاح"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "تعديل الكتاب"
        return context

class DashboardBookDeleteView(AdminRequiredMixin, DeleteView):
    model = Book
    template_name = 'dashboard/shared/confirm_delete.html'
    success_url = reverse_lazy('dashboard:books')

from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.contrib import messages

class DashboardBookToggleFeaturedView(AdminRequiredMixin, View):
    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        if book.is_featured:
            book.is_featured = False
            book.save()
            messages.success(request, f"تم إزالة '{book.title}' من الصفحة الرئيسية.")
        else:
            featured_count = Book.objects.filter(is_featured=True).count()
            if featured_count >= 10:
                messages.error(request, "لا يمكن إضافة أكثر من 10 كتب للصفحة الرئيسية.")
            else:
                book.is_featured = True
                book.save()
                messages.success(request, f"تم إضافة '{book.title}' للصفحة الرئيسية.")
        return redirect('dashboard:books')

# --- Orders CRUD ---
class DashboardOrdersView(AdminRequiredMixin, ListView):
    model = Order
    template_name = 'dashboard/orders/list.html'
    context_object_name = 'orders'
    paginate_by = 10
    
    def get_queryset(self):
        qs = super().get_queryset().select_related('user')
        q = self.request.GET.get('q')
        if q:
            if q.isdigit():
                qs = qs.filter(Q(id=q) | Q(user__username__icontains=q))
            else:
                qs = qs.filter(user__username__icontains=q)
        return qs

class DashboardOrderUpdateView(AdminRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Order
    template_name = 'dashboard/shared/form.html'
    fields = ['status']
    success_url = reverse_lazy('dashboard:orders')
    success_message = "تم تحديث حالة الطلب بنجاح"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "تحديث حالة الطلب"
        return context

# --- Users CRUD ---
class DashboardUsersView(AdminRequiredMixin, ListView):
    model = User
    template_name = 'dashboard/users/list.html'
    context_object_name = 'users'
    paginate_by = 10
    
    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            if q.isdigit():
                qs = qs.filter(Q(id=q) | Q(username__icontains=q) | Q(first_name__icontains=q) | Q(email__icontains=q))
            else:
                qs = qs.filter(Q(username__icontains=q) | Q(first_name__icontains=q) | Q(email__icontains=q))
        return qs

class DashboardUserCreateView(AdminRequiredMixin, SuccessMessageMixin, CreateView):
    model = User
    template_name = 'dashboard/shared/form.html'
    fields = ['username', 'email', 'password', 'first_name', 'last_name', 'is_staff']
    success_url = reverse_lazy('dashboard:users')
    success_message = "تم إضافة المستخدم بنجاح"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "إضافة مستخدم جديد"
        return context
    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return super().form_valid(form)

class DashboardUserUpdateView(AdminRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    template_name = 'dashboard/shared/form.html'
    fields = ['username', 'email', 'first_name', 'last_name', 'is_staff']
    success_url = reverse_lazy('dashboard:users')
    success_message = "تم تعديل المستخدم بنجاح"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "تعديل المستخدم"
        return context

class DashboardUserDeleteView(AdminRequiredMixin, DeleteView):
    model = User
    template_name = 'dashboard/shared/confirm_delete.html'
    success_url = reverse_lazy('dashboard:users')

# --- Manuscripts CRUD ---
from apps.manuscripts.models import Manuscript

class DashboardManuscriptsView(AdminRequiredMixin, ListView):
    model = Manuscript
    template_name = 'dashboard/manuscripts/list.html'
    context_object_name = 'manuscripts'
    paginate_by = 10
    
    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            if q.isdigit():
                qs = qs.filter(Q(id=q) | Q(title__icontains=q) | Q(author_name__icontains=q))
            else:
                qs = qs.filter(Q(title__icontains=q) | Q(author_name__icontains=q))
        return qs

class DashboardManuscriptUpdateView(AdminRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Manuscript
    template_name = 'dashboard/manuscripts/review.html'
    fields = ['status']
    success_url = reverse_lazy('dashboard:manuscripts')
    success_message = "تم تحديث حالة المخطوطة بنجاح"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "تحديث حالة المخطوطة"
        return context

class DashboardManuscriptDeleteView(AdminRequiredMixin, DeleteView):
    model = Manuscript
    template_name = 'dashboard/shared/confirm_delete.html'
    success_url = reverse_lazy('dashboard:manuscripts')

# --- Authors CRUD ---
from apps.authors.models import Author
from django.shortcuts import get_object_or_404, redirect

class DashboardAuthorsView(AdminRequiredMixin, ListView):
    model = Author
    template_name = 'dashboard/authors/list.html'
    context_object_name = 'authors'
    paginate_by = 10
    
    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(name__icontains=q)
        return qs

class DashboardAuthorCreateView(AdminRequiredMixin, SuccessMessageMixin, CreateView):
    model = Author
    template_name = 'dashboard/shared/form.html'
    fields = ['name', 'slug', 'biography', 'photo', 'is_active']
    success_url = reverse_lazy('dashboard:authors')
    success_message = "تم إضافة المؤلف بنجاح"

class DashboardAuthorUpdateView(AdminRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Author
    template_name = 'dashboard/shared/form.html'
    fields = ['name', 'slug', 'biography', 'photo', 'is_active']
    success_url = reverse_lazy('dashboard:authors')
    success_message = "تم تحديث المؤلف بنجاح"

class DashboardAuthorDeleteView(AdminRequiredMixin, DeleteView):
    model = Author
    template_name = 'dashboard/shared/confirm_delete.html'
    success_url = reverse_lazy('dashboard:authors')

from django.views import View
class DashboardAuthorToggleStatusView(AdminRequiredMixin, View):
    def post(self, request, pk):
        author = get_object_or_404(Author, pk=pk)
        author.is_active = not author.is_active
        author.save()
        messages.success(request, f"تم {'تفعيل' if author.is_active else 'إيقاف'} المؤلف بنجاح")
        return redirect('dashboard:authors')

class DashboardUserToggleStatusView(AdminRequiredMixin, View):
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if not user.is_superuser: # Don't block superusers
            user.is_active = not user.is_active
            user.save()
            messages.success(request, f"تم {'تفعيل' if user.is_active else 'إيقاف/حظر'} المستخدم بنجاح")
        else:
            messages.error(request, "لا يمكن تغيير حالة المدير العام")
        return redirect('dashboard:users')

# --- Reports CRUD ---
from apps.core.models import Report

class DashboardReportsView(AdminRequiredMixin, ListView):
    model = Report
    template_name = 'dashboard/reports/list.html'
    context_object_name = 'reports'
    paginate_by = 10
    
    def get_queryset(self):
        qs = super().get_queryset().select_related('reporter', 'content_type')
        status = self.request.GET.get('status')
        if status:
            qs = qs.filter(status=status)
        return qs

class DashboardReportUpdateView(AdminRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Report
    template_name = 'dashboard/reports/form.html'
    fields = ['status', 'resolved_at']
    success_url = reverse_lazy('dashboard:reports')
    success_message = "تم تحديث حالة البلاغ بنجاح"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "تحديث حالة البلاغ"
        return context

class DashboardReportDeleteView(AdminRequiredMixin, DeleteView):
    model = Report
    template_name = 'dashboard/shared/confirm_delete.html'
    success_url = reverse_lazy('dashboard:reports')

from django.utils import timezone

class DashboardReportActionView(AdminRequiredMixin, View):
    def post(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
        action = request.POST.get('action')
        
        obj = report.content_object
        
        if not obj:
            messages.error(request, "المحتوى المُبلغ عنه غير موجود.")
            return redirect('dashboard:reports')
            
        try:
            if action == 'block_author' and hasattr(obj, 'is_active'):
                obj.is_active = False
                obj.save()
                messages.success(request, "تم حظر المؤلف بنجاح.")
                
            elif action == 'hide_book' and hasattr(obj, 'is_published'):
                obj.is_published = False
                obj.save()
                messages.success(request, "تم إخفاء الكتاب بنجاح لإعادة مراجعته.")
                
            elif action == 'delete_review':
                obj.delete()
                messages.success(request, "تم حذف التعليق/التقييم بنجاح.")
                
            elif action == 'block_user_and_delete_review':
                user_to_block = obj.user
                if not user_to_block.is_superuser:
                    user_to_block.is_active = False
                    user_to_block.save()
                obj.delete()
                messages.success(request, "تم حظر المستخدم وحذف التعليق بنجاح.")
            else:
                messages.error(request, "إجراء غير معروف.")
                return redirect('dashboard:reports')
                
            # Mark report as resolved
            report.status = 'resolved'
            report.resolved_at = timezone.now()
            report.save()
            
        except Exception as e:
            messages.error(request, f"حدث خطأ أثناء تنفيذ الإجراء: {str(e)}")
            
        return redirect('dashboard:reports')
