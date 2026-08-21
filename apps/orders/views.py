from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.books.models import Book
from .models import Order, OrderItem

def get_cart(request):
    cart = request.session.get('cart', {})
    return cart

def cart_add(request, book_id):
    cart = get_cart(request)
    book = get_object_or_404(Book, id=book_id)
    book_type = request.POST.get('book_type', 'paperback') # 'paperback' or 'ebook'
    
    key = f"{book_id}_{book_type}"
    if key not in cart:
        price = float(book.paperback_price) if book_type == 'paperback' else float(book.ebook_price)
        cart[key] = {
            'book_id': book_id,
            'title': book.title,
            'type': book_type,
            'price': price,
            'quantity': 1,
            'cover_url': book.cover.url if book.cover else ''
        }
    else:
        cart[key]['quantity'] += 1
        
    request.session['cart'] = cart
    return redirect('orders:cart_detail')

def cart_remove(request, book_key):
    cart = get_cart(request)
    if book_key in cart:
        del cart[book_key]
        request.session['cart'] = cart
    return redirect('orders:cart_detail')

def cart_detail(request):
    cart = get_cart(request)
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    return render(request, 'orders/cart_detail.html', {'cart': cart, 'total': total})

@login_required
def checkout(request):
    cart = get_cart(request)
    if not cart:
        return redirect('orders:cart_detail')
        
    if request.method == 'POST':
        total = sum(item['price'] * item['quantity'] for item in cart.values())
        order = Order.objects.create(
            user=request.user,
            total_price=total,
            status='pending'
        )
        
        for key, item in cart.items():
            book = Book.objects.get(id=item['book_id'])
            OrderItem.objects.create(
                order=order,
                book=book,
                quantity=item['quantity'],
                price=item['price']
            )
            # Update stock if paperback
            if item['type'] == 'paperback':
                book.stock -= item['quantity']
                book.save()
                
        # Clear cart
        del request.session['cart']
        return redirect('orders:order_success')
        
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    return render(request, 'orders/checkout.html', {'cart': cart, 'total': total})

def order_success(request):
    return render(request, 'orders/success.html')
