import datetime

from django.http import JsonResponse
from django.shortcuts import render

from coupons.forms import CouponApplyForm
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from main.models import Customer
import json

@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'orders/order/detail.html',
                  {'order': order})


from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string


def order_create(request):
    global address, order
    coupon_apply_form = CouponApplyForm()
    categories = [{'name': 'iPhone', 'url': '/category/iphones/', 'count': 2},
                  {'name': 'iPad', 'url': '/category/ipads/', 'count': 2}]
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST or None)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.paid = True
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # очистка корзины
            cart.clear()

            # template = render_to_string('orders/order/email_template.html', {'name': request.user.first_name})
            template = render_to_string('orders/order/email_template.html', {'name': 'BORISBORIS'})
            email = EmailMessage(
                'Thanks',
                template,
                settings.EMAIL_HOST_USER,
                ['zakaraya2000@mail.ru'],
            )
            email.fail_silently = False
            email.send()


            # запуск асинхронной задачи
            # order_created.delay(order.id)
            return render(request, 'orders/order/created.html',
                          {'order': order, 'coupon_apply_form': coupon_apply_form, 'categories': categories})
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
        #     использую для передачи суммы заказа на paypal в js
        sum_order_after_discount = cart.get_total_price_after_discount()
        order = {'get_cart_total': sum_order_after_discount}

    # return render(request, 'orders/order/create.html',
    return render(request, 'orders/order/create3.html',
                  {'cart': cart, 'form': form, 'coupon_apply_form': coupon_apply_form, 'categories': categories,
                   'order': order})


# def payment_complete(request):
#     body = json.loads(request.body)
#     print('body-->', body)
#     return render('payment', payment_option='stripe')

def processOrder(request):
    coupon_apply_form = CouponApplyForm()
    categories = [{'name': 'iPhone', 'url': '/category/iphones/', 'count': 2},
                  {'name': 'iPad', 'url': '/category/ipads/', 'count': 2}]
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(json.loads(request.body))
        data = json.loads(request.body)
        order = form.save(commit=False)
        if cart.coupon:
            order.coupon = cart.coupon
            order.discount = cart.coupon.discount
        order.save()
        for item in cart:
            OrderItem.objects.create(
                                     product=item['product'],
                                     price=item['price'],
                                     quantity=item['quantity'])
        # очистка корзины
        cart.clear()

    return JsonResponse('Payment submitted..', safe=False)
