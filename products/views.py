from django.http import Http404
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.shortcuts import render, get_object_or_404
from .models import Product
from carts.models import Cart

# class ProductFeaturedListView(ListView):
#     template_name = 'products/list.html'
#
#     def get_queryset(self, *args, **kwargs):
#         request = self.request
#         return Product.objects.all().featured()
#
#
# class ProductFeaturedDetailView(DetailView):
#
#     template_name = 'products/detail-featured.html'
#
#     # method 1:
#     queryset = Product.objects.featured()
#
#     # method 2:
#     # def get_queryset(self, *args, **kwargs):
#     #     request = self.request
#     #     return Product.objects.featured()


class ProductListView(ListView):
    # queryset = Product.objects.all()
    template_name = 'products/list.html'

    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductListView, self).get_context_data(*args, **kwargs)
    #     print(context)
    #     return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all()


# def product_list_view(request):
#     queryset = Product.objects.all()
#     context = {
#         'object_list': queryset
#     }
#     return render(request, 'products/list.html', context)


class ProductDetailSlugView(DetailView):
    queryset = Product.objects.all()
    template_name = 'products/detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_object(self, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')

        try:
            instance = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise Http404('no such a product!')
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug)
            instance = qs.first()
        except:
            raise Http404('some issues')
        return instance


# class ProductDetailView(DetailView):
#     # queryset = Product.objects.all()
#     template_name = 'products/detail.html'
#
#     # def get_context_data(self, *args, **kwargs):
#     #     context = super(ProductListView, self).get_context_data(*args, **kwargs)
#     #     print(context)
#     #     return context
#
#     # method 1:
#     def get_object(self, **kwargs):
#         request = self.request
#         pk = self.kwargs.get('pk')
#         instance = Product.objects.get_by_id(pk)
#         if instance is None:
#             raise Http404('hey bro, searched wrong from class based view')
#         return instance
#
#     # method 2:
#     # def get_queryset(self, *args, **kwargs):
#     #     request = self.request
#     #     pk = self.kwargs.get('pk')
#     #     return Product.objects.filter(pk=pk)
#
#
#
# def product_detail_view(request, pk):
#     # # method 1:
#     # instance = get_object_or_404(Product, pk=pk)
#
#     # # method 2:
#     # try:
#     #     instance = Product.objects.get(pk=pk)
#     # except Product.DoesNotExist:
#     #     raise Http404("what you're looking for, isn't here bro")
#     # except:
#     #     print('something wrong')
#
#     # # method 3:
#     # qs = Product.objects.filter(pk=pk)
#     # if qs.exists() and qs.count() == 1:
#     #     instance = qs.first()
#     # else:
#     #     print("data doesn't exixt")
#
#     # method 4:
#     instance = Product.objects.get_by_id(pk)
#     if instance is None:
#         raise Http404('hey bro, search something else')
#
#     context = {
#         'object': instance
#     }
#     return render(request, 'products/detail.html', context)
