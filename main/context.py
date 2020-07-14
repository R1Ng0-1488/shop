from .models import Category
from cart.cart import Cart

def proccesor_context(request):
    context = {}
    context['categories'] = Category.objects.all()
    context['cart'] = Cart(request)
    return context
