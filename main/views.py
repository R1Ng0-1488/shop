from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from cart.forms import CartAddPoductForm
from .models import Category, Product
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
	context = {'category': category, 'products': page.object_list, 'page_obj': page}
	return render(request, 'shop/product/list.html', context)


def product_detail(request, pk, slug):
	product = get_object_or_404(Product, pk=pk, slug=slug, available=True)
	form = CartAddPoductForm()
	context = {'product': product, 'form': form}
	return render(request, 'shop/product/detail.html', context)
