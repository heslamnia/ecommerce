from django.views.generic.list import ListView
from products.models import Product


class SearchProductView(ListView):
    template_name = 'search/view.html'

    def get_context_data(self, *args, **kwargs):
        context = super(SearchProductView, self).get_context_data(*args, **kwargs)
        print(self.request.GET)
        query = self.request.GET.get('q')
        context['query'] = query
        # SearchQuery.objects.create(query=query)
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        # request.GET returns a dictionary and you can call get on any dictionary to get value of a key.
        # alternatively you can use a bracket to look for a key. but this way returns an error if the key doesn't exist.
        query = request.GET.get('q', None)
        if query is not None:
            return Product.objects.search(query)
        return Product.objects.featured()
