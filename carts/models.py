from django.db import models
from django.conf import settings
from products.models import Product
from django.db.models.signals import pre_save, m2m_changed

User = settings.AUTH_USER_MODEL


class CartManager(models.Manager):

    def new_or_get(self, request):
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated() and not cart_obj.user:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            new_obj = True
            cart_obj = Cart.objects.new(user=request.user)
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj

    def new(self, user=None, products=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated():
                user_obj = user
        return self.model.objects.create(user=user_obj)


class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    products = models.ManyToManyField(Product, blank=True)
    total = models.DecimalField(default=0.0, max_digits=100, decimal_places=2)
    subtotal = models.DecimalField(default=0.0, max_digits=100, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now_add=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)


def cart_m2m_changed_receiver(sender, instance, action, *args, **kwargs):

    if action == 'post_remove' or action == 'post_add' or action == 'post_clear':
        products = instance.products.all()

        subtotal = 0
        for x in products:
            # print(x.price)
            subtotal += x.price
        instance.subtotal = subtotal
        instance.save()


m2m_changed.connect(cart_m2m_changed_receiver, sender=Cart.products.through)


def cart_presave_receiver(sender, instance, *args, **kwargs):
    if instance.subtotal > 0:
        instance.total = instance.subtotal + 10
    else:
        instance.total = 0.


pre_save.connect(cart_presave_receiver, sender=Cart)