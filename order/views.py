from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse

from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
# Create your views here.


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'],
                price=item['price'],
                quantity=item['quantity'])
            # clear the cart
            cart.clear()
            # start asinc task
            order_created.delay(order.id)
            #order_created(order.id)
            # сохранение заказа в сессию
            request.session['order_id'] = order.id
            # перенаправление на страницу оплаты
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm
    return render(request, 'order/create.html', {'cart': cart, 'form': form})

@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/detail.html', {'order': order})
