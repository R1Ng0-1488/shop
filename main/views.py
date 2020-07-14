from django.shortcuts import render, get_object_or_404

from cart.forms import CartAddPoductForm
from .models import Category, Product
# Create your views here.


def product_list(request, category_slug=None):
	category = None
	products = Product.objects.filter(available=True)
	if category_slug:
		category = get_object_or_404(Category, slug=category_slug)
		products = products.filter(category=category)
	context = {'category': category, 'products': products}
	return render(request, 'shop/product/list.html', context)

def product_detail(request, pk, slug):
	product = get_object_or_404(Product, pk=pk, slug=slug, available=True)
	form = CartAddPoductForm()
	context = {'product': product, 'form': form}
	return render(request, 'shop/product/detail.html', context)
