from django.shortcuts import render
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from main.models import Customer


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'admin/orders/order/detail.html',
                  {'order': order})


def order_create(request):
    global address
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
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # очистка корзины
            cart.clear()

            # запуск асинхронной задачи
            # order_created.delay(order.id)

            return render(request, 'orders/order/created.html',
                          {'order': order})
    else:
        # form = OrderCreateForm({'first_name': request.user})
        user = request.user
        customer = Customer.objects.filter(user__username=user)
        for i in customer:
            address = i.address
        if request.user.is_authenticated:
            data = {
                    'first_name': request.user.first_name,
                    'last_name': request.user.last_name,
                    'email': request.user.email,
                    'address': address,
                    'postal_code': 'TEST',
                    'city': 'TEST'
                    }
            form = OrderCreateForm(data)
        else:
            form = OrderCreateForm()

    # return render(request, 'orders/order/create.html',
    return render(request, 'orders/order/create2.html',
                  {'cart': cart, 'form': form})
