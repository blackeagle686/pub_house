from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from apps.orders.models import Order, OrderItem
from apps.books.models import Book
from django.db.models import Sum, Count

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('accounts:login')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'تم تحديث ملفك الشخصي بنجاح!')
            return redirect('accounts:profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    # Get last book ordered
    last_order = orders.first()
    last_book = None
    if last_order and last_order.items.exists():
        last_book = last_order.items.first().book

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'orders': orders,
        'last_book': last_book,
    }

    # Author specific logic
    if hasattr(request.user, 'author_profile') and request.user.author_profile is not None:
        author = request.user.author_profile
        author_books = author.books.all()
        # Analytics for author
        total_reviews = sum([book.review_count for book in author_books])
        total_sales = OrderItem.objects.filter(book__author=author, order__status='completed').aggregate(Sum('quantity'))['quantity__sum'] or 0
        
        context.update({
            'is_author': True,
            'author_books': author_books,
            'total_reviews': total_reviews,
            'total_sales': total_sales,
        })
    else:
        context['is_author'] = False

    return render(request, 'accounts/profile.html', context)
