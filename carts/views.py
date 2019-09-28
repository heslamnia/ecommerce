from django.shortcuts import render
from carts.models import Cart
from products.models import Product
from django.shortcuts import redirect


def cart_home(request):
    # cart_obj, new_obj = Cart.objects.new_or_get(request)
    # products = cart_obj.products.all()
    # total = 0
    # for x in products:
    #     # print(x.price)
    #     total += x.price
    # cart_obj.total = total
    # cart_obj.save()
    return render(request, "carts/home.html", {})


def cart_update(request):
    product_id = 1
    product_obj = Product.objects.get(id=product_id)
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    if cart_obj in Cart.products.all():
        print('obj in cart')
    else:
        cart_obj.products.add(product_obj)
    # return redirect(product_obj.get_absolute_url())
    return redirect('carts:home')
