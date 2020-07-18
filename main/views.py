from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.views.generic import View, ListView
from django.db.models import Q

from cart.forms import CartAddPoductForm
from .models import Category, Product
from .forms import SearchForm
# Create your views here.

def product_list(request, category_slug=None):
	category = None
	products = Product.objects.filter(available=True)
	if category_slug:
		category = get_object_or_404(Category, slug=category_slug)
		products = products.filter(category=category)
	paginator = Paginator(products, 8)
	if 'page' in request.GET:
		page_num = request.GET['page']
	else:
		page_num = 1
	page = paginator.get_page(page_num)
	context = {'category': category, 'product_list': page.object_list, 'page_obj': page}
	return render(request, 'shop/product/list.html', context)


def product_detail(request, pk, slug):
	product = get_object_or_404(Product, pk=pk, slug=slug, available=True)
	form = CartAddPoductForm()
	context = {'product': product, 'form': form}
	return render(request, 'shop/product/detail.html', context)


class Search(ListView):
	template_name = 'shop/product/list.html'
	paginate_by = 8

	def get_queryset(self):
		print(self.request.GET)
		return Product.objects.filter(name__icontains=self.request.GET.get('q'))

	
	def get_context_data(self, *args, **kwargs):
		context  = super().get_context_data(*args, **kwargs)
		context['q'] = f"q={self.request.GET.get('q')}&"
		return context	

