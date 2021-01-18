from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from main.models import Product
from .cart import Cart
from cart.forms import CartAddProductForm
from main.forms import SearchForm
from coupons.forms import CouponApplyForm
import json


@require_POST
def cart_add(request, title):
    cart = Cart(request)
    product = get_object_or_404(Product, title=title)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 # quantity=cd['quantity'],
                 quantity=1,
                 update_quantity=cd['update'])
    response = {"data": "goes here"}
    return HttpResponse(json.dumps(response), content_type='application/json')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    categories = [{'name': 'iPhone', 'url': '/category/iphones/', 'count': 2},
                  {'name': 'iPad', 'url': '/category/ipads/', 'count': 2}]
    # return render(request, 'cart/detail.html', {'cart': cart})
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'],
                     'update': True})
    coupon_apply_form = CouponApplyForm()
    return render(request,
                  # 'cart/detail.html',
                  'cart/detail2.html',
                  {'cart': cart,
                   'coupon_apply_form': coupon_apply_form, 'categories': categories})


def cart_create(request):
    # cart = Cart(request)
    # product_id = request.GET.get('product_id')
    # print(product_id)
    # product = Product.objects.get(id=product_id)
    # print(product)
    # cart.add(product=product)
    #
    # return JsonResponse('', safe=False)
    cart = Cart(request)
    product = get_object_or_404(Product)
    if request.method == 'POST':
        cart.add(product=product)
    return JsonResponse('', safe=False)


@require_POST
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    quantity = data['quantity']
    cart = Cart(request)
    # quantity = cart.cart[productId]['quantity']
    # print(cart.cart[productId]['quantity'])
    product = Product.objects.get(id=productId)
    form = CartAddProductForm(request.POST)

    if action == 'remove':
        if cart.cart[productId]['quantity'] == 1:
            quantity = 0
        else:
            quantity -= 2
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=quantity,
                 update_quantity=cd['update'])
    return JsonResponse('Товар добавлен', safe=False)


def post_search(request):
    form = SearchForm()
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            results = SearchQuerySet().models(Post).filter(content=cd['query']).load_all()
            # count total results
            total_results = results.count()
    return render(request,
                  'blog/post/search.html',
                  {'form': form,
                   'cd': cd,
                   'results': results,
                   'total_results': total_results})
